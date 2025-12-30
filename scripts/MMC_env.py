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

        # 한 스텝에서 바꿀 수 있는 최대 변화량 비율 (예: 전체 범위의 10%)
        self.dL_scale = 0.1 * (self.L_max - self.L_min)
        self.dC_scale = 0.1 * (self.C_max - self.C_min)

        # 상태: [L_norm, C_norm]
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0], dtype=np.float32),
            high=np.array([1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )

        # 행동: continuous (L, C 변화 명령) ∈ [-1, 1]^2
        # action[0] ~ dL 방향/크기, action[1] ~ dC 방향/크기
        self.action_space = spaces.Box(
            low=np.array([-1.0, -1.0], dtype=np.float32),
            high=np.array([ 1.0,  1.0], dtype=np.float32),
            dtype=np.float32
        )

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

        # 설계 최적화용 내부 변수
        self.prev_cost = None
        self.best_cost = np.inf
        self.best_L = None
        self.best_C = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # 운전 조건 (여기선 고정)
        self.V_in = 1.0
        self.I_in = 1.0
        self.V_out = 1.0
        self.I_out = 1.0
        self.P_out = 1.0
        self.pf = 1.0

        # L, C 초기값 (중간값)
        self.L_arm = (self.L_min + self.L_max) / 2.0
        self.C_arm = (self.C_min + self.C_max) / 2.0

        self.step_count = 0
        self.prev_cost = None
        self.best_cost = np.inf
        self.best_L = self.L_arm
        self.best_C = self.C_arm

        state = self._get_state()
        info = {}
        return state, info

    def step(self, action):
        # action: np.ndarray shape (2,)
        # 1) action -> L, C 업데이트
        self._apply_action(action)

        # 2) MMC 시뮬레이션
        I_circ_rms, I_ripple, eta = self._run_mmc_simulation(
            self.L_arm, self.C_arm,
            self.V_in, self.I_in, self.V_out, self.I_out
        )

        # 3) reward 계산 (개선량 기반)
        reward, cost = self._compute_reward(I_circ_rms, I_ripple, eta)

        # 4) state 업데이트
        self.step_count += 1
        terminated = False
        truncated = self.step_count >= self.max_steps

        state = self._get_state()
        info = {
            "L_arm": self.L_arm,
            "C_arm": self.C_arm,
            "I_circ_rms": I_circ_rms,
            "I_ripple": I_ripple,
            "eta": eta,
            "cost": cost,
            "best_cost": self.best_cost,
            "best_L": self.best_L,
            "best_C": self.best_C,
        }

        return state, reward, terminated, truncated, info

    def _get_state(self):
        L_norm = (self.L_arm - self.L_min) / (self.L_max - self.L_min)
        C_norm = (self.C_arm - self.C_min) / (self.C_max - self.C_min)
        state = np.array([L_norm, C_norm], dtype=np.float32)
        return state

    def _apply_action(self, action):
        # action ∈ [-1, 1]^2
        action = np.clip(action, -1.0, 1.0)

        dL = action[0] * self.dL_scale
        dC = action[1] * self.dC_scale

        self.L_arm = np.clip(self.L_arm + dL, self.L_min, self.L_max)
        self.C_arm = np.clip(self.C_arm + dC, self.C_min, self.C_max)

    def _run_mmc_simulation(self, L_arm, C_arm, V_in, I_in, V_out, I_out):
        # 더미 모델 (나중에 실제 MMC 시뮬레이터로 교체)
        I_circ_rms = 1.0 / (L_arm / self.L_min + 1e-3)
        I_ripple = 1.0 / (C_arm / self.C_min + 1e-3)
        eta = 0.9 - 0.05 * ((L_arm - (self.L_min + self.L_max)/2) / (self.L_max - self.L_min))**2 \
                  - 0.05 * ((C_arm - (self.C_min + self.C_max)/2) / (self.C_max - self.C_min))**2
        eta = np.clip(eta, 0.0, 1.0)
        return float(I_circ_rms), float(I_ripple), float(eta)

    def _compute_reward(self, I_circ_rms, I_ripple, eta):
        I_circ_norm = I_circ_rms
        I_ripple_norm = I_ripple

        w1, w2, w3 = 1.0, 1.0, 1.0
        cost = w1 * I_circ_norm + w2 * I_ripple_norm + w3 * (1 - eta)

        if self.prev_cost is None:
            reward = -cost
        else:
            reward = self.prev_cost - cost  # cost 감소량

        self.prev_cost = cost

        if cost < self.best_cost:
            self.best_cost = cost
            self.best_L = self.L_arm
            self.best_C = self.C_arm

        return reward, cost

    def render(self):
        if self.render_mode == "human":
            print(
                f"Step {self.step_count}, "
                f"L={self.L_arm:.6f}, C={self.C_arm:.6f}, "
                f"best_cost={self.best_cost:.4f}"
            )
