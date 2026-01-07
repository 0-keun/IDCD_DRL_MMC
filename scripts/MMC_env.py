import gym
from gym import spaces
import numpy as np
import subprocess


t_end = 1.5
dt = 1e-7
t = 0:dt:t_end




class MMCTuningEnv(gym.Env):
    mvoutdata = {"render_modes": ["human"]}

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
        self.H = self.update_H()

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

    def update_H(self, L=20e-3, C=10e-3):
        E = 2000
        R = 1
        Coff = 25e-9 
        G_s = Coff/dt
        G_r = 1/R
        f_sw = 100e3
        T_sw = 1/f_sw

        G_L = dt/L
        G_c = C/dt

        H_LIST =   [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [G_s, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, G_c, -G_c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [G_s, 0, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0],
                    [0, 0, G_s, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, G_c, -G_c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, G_s, 0, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, G_L, -G_L, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, G_r, -G_r, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, G_r, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, G_r, -G_r, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, G_L, -G_L, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, -1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, G_s, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, G_c, -G_c, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, G_s, 0, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, -1, -1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, G_s, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, G_c, -G_c, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, G_s, 0, -G_s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                    
        return H_LIST

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

        self.H = self.update_H(self.L_arm, self.C_arm)

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

        I_circ_rms, I_ripple, vout = self._run_mmc_simulation(
            self.H
        )

        reward, cost = self._compute_reward(I_circ_rms, I_ripple, vout)

        self.step_count += 1
        terminated = False
        truncated = self.step_count >= self.max_steps

        state = self._get_state()
        info = {
            "L_arm": self.L_arm,
            "C_arm": self.C_arm,
            "I_circ_rms": I_circ_rms,
            "I_ripple": I_ripple,
            "vout": vout,
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

        self.H = self.update_H(self.L_arm, self.C_arm)

    def _send_H_once(self, H):
        """
        Python -> C 로 H(24x24=576개)를 딱 1번 전송.
        C는 이걸 읽고 LU factor를 준비한 뒤, mna_solver1을 실행하게 됨.
        """
        if gvoutttr(self, "_H_sent", False):
            return  # 이미 보냈으면 재전송하지 않음

        if self.proc.poll() is not None:
            err = ""
            try:
                if self.proc.stderr:
                    err = self.proc.stderr.read()
            except Exception:
                pass
            raise RuntimeError(f"MMC simulator process terminated before sending H. stderr:\n{err}")

        H = np.asarray(H, dtype=float)

        # H가 (24,24)면 576으로 펼치기
        if H.shape == (24, 24):
            # C 코드의 b_A/H는 column-major 기반이었음.
            # Python에서 2D를 넘긴다면 column-major로 flatten('F') 해주는 게 안전함.
            H_flat = H.flatten(order="F")
        elif H.size == 576:
            H_flat = H.reshape(-1)
        else:
            raise ValueError(f"H must be shape (24,24) or have 576 elements. Got {H.shape}")

        # 576개를 한 줄로 전송
        line_out = " ".join(f"{v:.17g}" for v in H_flat.tolist()) + "\n"
        self.proc.stdin.write(line_out)
        self.proc.stdin.flush()

        self._H_sent = True


    def _run_mmc_simulation(self, H):
        """
        (변경됨)
        - 입력: H (24x24 또는 576개)
        - 동작: H를 한 번만 보내고, C가 시뮬레이션 끝내고 내는 vout[last] 한 줄을 받음
        - 출력: vout_last (float)
        """
        # 0) H를 딱 1번만 전송
        self._send_H_once(H)

        # 1) 이제는 파라미터 6개를 보내지 않는다 (C가 읽지 않음)
        #    그냥 결과 한 줄을 기다린다.
        line_in = self.proc.stdout.readline()
        if not line_in:
            err = ""
            try:
                if self.proc.stderr:
                    err = self.proc.stderr.read()
            except Exception:
                pass
            raise RuntimeError(f"No response from MMC simulator. stderr:\n{err}")

        # 2) 출력은 vout[last] 숫자 1개라고 했으니 1개만 파싱
        parts = line_in.strip().split()
        if len(parts) != 3:
            raise RuntimeError(f"Bad response format from MMC simulator (expected 3 numbers): '{line_in.strip()}'")

        icc, deltai, vout = map(float, parts)
        return icc, deltai, vout

    # def _run_mmc_simulation(self, L_arm, C_arm, V_in, I_in, V_out, I_out):
    #     """
    #     Python -> C 로 한 줄 보내고
    #     C -> Python 으로 한 줄 받을 때까지 기다리는(블로킹) 구조
    #     """
    #     if self.proc.poll() is not None:
    #         # C 프로세스가 죽어있으면 에러
    #         err = ""
    #         try:
    #             if self.proc.stderr:
    #                 err = self.proc.stderr.read()
    #         except Exception:
    #             pass
    #         raise RuntimeError(f"MMC simulator process terminated. stderr:\n{err}")

    #     # 1) 한 줄 전송 (공백 구분)
    #     line_out = f"{L_arm} {C_arm} {V_in} {I_in} {V_out} {I_out}\n"
    #     self.proc.stdin.write(line_out)
    #     self.proc.stdin.flush()

    #     # 2) 한 줄 수신 (응답 올 때까지 여기서 기다림)
    #     line_in = self.proc.stdout.readline()
    #     if not line_in:
    #         err = ""
    #         try:
    #             if self.proc.stderr:
    #                 err = self.proc.stderr.read()
    #         except Exception:
    #             pass
    #         raise RuntimeError(f"No response from MMC simulator. stderr:\n{err}")

    #     parts = line_in.strip().split()
    #     if len(parts) != 3:
    #         raise RuntimeError(f"Bad response format from MMC simulator: '{line_in.strip()}'")

    #     I_circ_rms, I_ripple, vout = map(float, parts)
    #     return I_circ_rms, I_ripple, vout

    def _compute_reward(self, I_circ_rms, I_ripple, vout):
        I_circ_norm = I_circ_rms
        I_ripple_norm = I_ripple

        w1, w2, w3 = 1.0, 1.0, 1.0
        cost = w1 * I_circ_norm + w2 * I_ripple_norm + w3 * (1 - vout)

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
