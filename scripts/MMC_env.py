import gym
from gym import spaces
import numpy as np
import subprocess


class MMCTuningEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None, mmc_exec="./mmc_sim_server"):
        super().__init__()

        # ----- 파라미터 범위 설정 -----
        self.L_min, self.L_max = 1e-3, 10e-3
        self.C_min, self.C_max = 1e-3, 10e-3

        self.dL_scale = 0.1 * (self.L_max - self.L_min)
        self.dC_scale = 0.1 * (self.C_max - self.C_min)

        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0], dtype=np.float32),
            high=np.array([1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=np.array([-1.0, -1.0], dtype=np.float32),
            high=np.array([1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )

        self.render_mode = render_mode
        self.max_steps = 20
        self.step_count = 0

        self.L_arm = None
        self.C_arm = None
        self.V_in = None
        self.I_in = None
        self.V_out = None
        self.I_out = None
        self.P_out = None
        self.pf = None

        self.prev_cost = None
        self.best_cost = np.inf
        self.best_L = None
        self.best_C = None

        # ---- C 시뮬레이터 프로세스 실행 (★한 번만 띄우고 계속 사용) ----
        self.mmc_exec = mmc_exec
        self.proc = subprocess.Popen(
            [self.mmc_exec],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # 디버깅용 (원하면 PIPE 말고 None)
            text=True,
            bufsize=1  # line-buffered 느낌 (환경에 따라 다를 수 있음)
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.V_in = 1.0
        self.I_in = 1.0
        self.V_out = 1.0
        self.I_out = 1.0
        self.P_out = 1.0
        self.pf = 1.0

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
        self._apply_action(action)

        I_circ_rms, I_ripple, eta = self._run_mmc_simulation(
            self.L_arm, self.C_arm,
            self.V_in, self.I_in, self.V_out, self.I_out
        )

        reward, cost = self._compute_reward(I_circ_rms, I_ripple, eta)

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
        return np.array([L_norm, C_norm], dtype=np.float32)

    def _apply_action(self, action):
        action = np.clip(action, -1.0, 1.0)
        dL = float(action[0]) * self.dL_scale
        dC = float(action[1]) * self.dC_scale
        self.L_arm = float(np.clip(self.L_arm + dL, self.L_min, self.L_max))
        self.C_arm = float(np.clip(self.C_arm + dC, self.C_min, self.C_max))

    def _run_mmc_simulation(self, L_arm, C_arm, V_in, I_in, V_out, I_out):
        """
        Python -> C 로 한 줄 보내고
        C -> Python 으로 한 줄 받을 때까지 기다리는(블로킹) 구조
        """
        if self.proc.poll() is not None:
            # C 프로세스가 죽어있으면 에러
            err = ""
            try:
                if self.proc.stderr:
                    err = self.proc.stderr.read()
            except Exception:
                pass
            raise RuntimeError(f"MMC simulator process terminated. stderr:\n{err}")

        # 1) 한 줄 전송 (공백 구분)
        line_out = f"{L_arm} {C_arm} {V_in} {I_in} {V_out} {I_out}\n"
        self.proc.stdin.write(line_out)
        self.proc.stdin.flush()

        # 2) 한 줄 수신 (응답 올 때까지 여기서 기다림)
        line_in = self.proc.stdout.readline()
        if not line_in:
            err = ""
            try:
                if self.proc.stderr:
                    err = self.proc.stderr.read()
            except Exception:
                pass
            raise RuntimeError(f"No response from MMC simulator. stderr:\n{err}")

        parts = line_in.strip().split()
        if len(parts) != 3:
            raise RuntimeError(f"Bad response format from MMC simulator: '{line_in.strip()}'")

        I_circ_rms, I_ripple, eta = map(float, parts)
        return I_circ_rms, I_ripple, eta

    def _compute_reward(self, I_circ_rms, I_ripple, eta):
        I_circ_norm = I_circ_rms
        I_ripple_norm = I_ripple

        w1, w2, w3 = 1.0, 1.0, 1.0
        cost = w1 * I_circ_norm + w2 * I_ripple_norm + w3 * (1 - eta)

        if self.prev_cost is None:
            reward = -cost
        else:
            reward = self.prev_cost - cost

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

    def close(self):
        # Gym에서 env.close() 부르면 프로세스 정리
        if hasattr(self, "proc") and self.proc is not None:
            try:
                if self.proc.stdin:
                    self.proc.stdin.close()
            except Exception:
                pass
            try:
                self.proc.terminate()
            except Exception:
                pass
            self.proc = None
