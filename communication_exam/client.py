import subprocess

p = subprocess.Popen(
    ["./echo_server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# 1) 한 줄 보내기
msg = 123
p.stdin.write(str(msg) + "\n")
p.stdin.flush()

# 2) 한 줄 받기
reply = p.stdout.readline().rstrip("\n")
print("got:", reply)

# 종료(정리)
p.stdin.close()
p.terminate()
