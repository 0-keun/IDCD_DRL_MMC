import pandas as pd
from utils.utils import plot_multiple_yk, plot_yk

df = pd.read_csv("./results.csv")

time = df['t']

vout = df['vout']
deltai = df['deltai']
deltavc = df['deltavc']
icc_ac = df['icc_ac']

# print(vout[3])
# print(max(time))
# idx = list(time).index(max(time))
# print(idx)

time_list = [time, time, time, time.iloc[4500000:]]
values_list = [vout, deltai, deltavc, icc_ac.iloc[4500000:]]
name_list = ['vout', 'deltai', 'deltavc', 'icc_ac']

plot_multiple_yk(time_list, values_list, name_list)
