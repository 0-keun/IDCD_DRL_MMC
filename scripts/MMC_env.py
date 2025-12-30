import gym
from gym import spaces
import numpy as np

class MMCTuningEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None):
        super().__init__()

        # ----- 파라미터 범위 설정 -----
        self.L_min, self.L_max = 1e-3, 10e-3   # 예시 값
        self.C_min, self.C_max = 1e-3, 10e-3
        self.dL = 0.5e-3
        self.dC = 0.5e-3

        # 상태: [L_norm, C_norm, Vin_norm, Iin_norm, Vout_norm, Iout_norm, P_norm, pf]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, 0, -1], dtype=np.float32),
            high=np.array([1, 1, 1, 1, 1, 1, 1,  1], dtype=np.float32),
            dtype=np.float32
        )

        # 행동: L/C up/down/no-change 등 몇 가지
        self.action_space = spaces.Discrete(5)

        self.render_mode = render_mode

        self.max_steps = 20
        self.step_count = 0

        # 현재 운전 조건 / 파라미터
        self.L_arm = None
        self.C_arm = None
        self.V_in = None
        self.I_in = None
        self.V_out = None
        self.I_out = None
        self.P_out = None
        self.pf = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # 운전 조건 샘플링 (예: 고정하거나 random)
        self.V_in = 1.0  # p.u. 기준
        self.I_in = 1.0
        self.V_out = 1.0
        self.I_out = 1.0
        self.P_out = 1.0
        self.pf = 1.0

        # L, C 초기값
        self.L_arm = (self.L_min + self.L_max) / 2
        self.C_arm = (self.C_min + self.C_max) / 2

        self.step_count = 0

        state = self._get_state()
        info = {}
        return state, info

    def step(self, action):
        # 1) action -> L, C 업데이트
        self._apply_action(action)

        # 2) MMC 시뮬레이션 돌려서 성능 지표 계산 (여기는 네가 구현)
        I_circ_rms, I_ripple, eta = self._run_mmc_simulation(
            self.L_arm, self.C_arm,
            self.V_in, self.I_in, self.V_out, self.I_out
        )

        # 3) reward 계산
        reward = self._compute_reward(I_circ_rms, I_ripple, eta)

        # 4) state 업데이트
        # (운전 조건을 바꾸고 싶으면 여기서 변경)
        self.step_count += 1
        terminated = False  # 이 환경에선 특별한 성공조건이 없다면 False
        truncated = self.step_count >= self.max_steps

        state = self._get_state()
        info = {
            "L_arm": self.L_arm,
            "C_arm": self.C_arm,
            "I_circ_rms": I_circ_rms,
            "I_ripple": I_ripple,
            "eta": eta
        }

        return state, reward, terminated, truncated, info

    def _get_state(self):
        # p.u. 또는 0~1로 스케일링
        L_norm = (self.L_arm - self.L_min) / (self.L_max - self.L_min)
        C_norm = (self.C_arm - self.C_min) / (self.C_max - self.C_min)

        # 여기선 입력/출력은 1.0 p.u.로 가정 (필요시 갱신)
        state = np.array([
            L_norm,
            C_norm,
            self.V_in,
            self.I_in,
            self.V_out,
            self.I_out,
            self.P_out,
            self.pf
        ], dtype=np.float32)

        return state

    def _apply_action(self, action):
        if action == 0:
            dL, dC = 0.0, 0.0
        elif action == 1:
            dL, dC = +self.dL, 0.0
        elif action == 2:
            dL, dC = -self.dL, 0.0
        elif action == 3:
            dL, dC = 0.0, +self.dC
        elif action == 4:
            dL, dC = 0.0, -self.dC
        else:
            dL, dC = 0.0, 0.0

        self.L_arm = np.clip(self.L_arm + dL, self.L_min, self.L_max)
        self.C_arm = np.clip(self.C_arm + dC, self.C_min, self.C_max)

    def _run_mmc_simulation(self, L_arm, C_arm, V_in, I_in, V_out, I_out):
        """
        여기서 실제 MMC 시뮬레이션(PSIM, MATLAB, 자체 모델 등)을 호출해서
        I_circ_rms, I_ripple, eta를 계산하면 됨.
        지금은 placeholder로 대충 만든 더미 코드.
        """
        # 예시: L이 커지면 I_circ 감소, C가 커지면 ripple 감소, eta는 어느 중간에서 최대라고 가정
        I_circ_rms = 1.0 / (L_arm / self.L_min + 1e-3)
        I_ripple = 1.0 / (C_arm / self.C_min + 1e-3)
        eta = 0.9 - 0.05 * ((L_arm - (self.L_min + self.L_max)/2) / (self.L_max - self.L_min))**2 \
                  - 0.05 * ((C_arm - (self.C_min + self.C_max)/2) / (self.C_max - self.C_min))**2
        eta = np.clip(eta, 0.0, 1.0)
        return float(I_circ_rms), float(I_ripple), float(eta)

    def _compute_reward(self, I_circ_rms, I_ripple, eta):
        I_circ_norm = I_circ_rms  # ref로 나눌 수 있으면 나누기
        I_ripple_norm = I_ripple

        w1, w2, w3 = 1.0, 1.0, 1.0
        cost = w1 * I_circ_norm + w2 * I_ripple_norm + w3 * (1 - eta)
        return -cost

    def render(self):
        if self.render_mode == "human":
            print(f"Step {self.step_count}, L={self.L_arm}, C={self.C_arm}")
