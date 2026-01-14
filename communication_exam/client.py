import subprocess
import numpy as np
import time

dt = 1e-7

p = subprocess.Popen(
    ["./main"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

def update_H(L=20e-3, C=10e-3):
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
    
    # print(H_LIST)
                
    return H_LIST

def _send_H_once(H):
    """
    Python -> C 로 H(24x24=576개)를 딱 1번 전송.
    C는 이걸 읽고 LU factor를 준비한 뒤, mna_solver1을 실행하게 됨.
    """
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
    line_out = " ".join(f"{v:.17g}" for v in H_flat.tolist()) 
    line_out = line_out.replace("e","E") + "\n"
    # print(line_out)
    p.stdin.write(line_out)
    p.stdin.flush()

# 1) 한 줄 보내기
msg = 123
start_time = time.perf_counter()
H_list = update_H()
end_time = time.perf_counter()
second_time = time.time()
_send_H_once(H_list)
third_time = time.time()
# p.stdin.write(str(msg) + "\n")
# p.stdin.flush()

# 2) 받기
reply = p.stdout.readline().rstrip("\n")
fourth_time = time.time()
print("got:", reply)
print(f'Update, Send: {(end_time - start_time)*10e6}[us]')
# print(f'Update, Send: {third_time-first_time}[s]')
print(f'Simulation, Receive: {fourth_time-third_time}[s]')


# 종료(정리)
p.stdin.close()
p.terminate()
