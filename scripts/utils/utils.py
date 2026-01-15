import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

from types import SimpleNamespace
import json

import os

##########################################
##                 json                 ##
##########################################
def load_json(file_name='./params.json'):
    with open(file_name, 'r') as f:
        data = json.load(f)
        data = SimpleNamespace(**data)

    return data

##########################################
##                 PLOT                 ##
##########################################

def save_loss_plot(history, loss_filename='loss.png', time_flag=False):
    """
    Given a Keras History object, plot & save loss curves.

    Args:
        history: keras.callbacks.History returned by model.fit()
        loss_filepath (str): where to save the loss plot (PNG).
    """
    loss_filepath = name_to_dir(name='graph',time_flag=time_flag)+name_time(default_name=loss_filename)
    plt.figure()
    plt.plot(history.history['loss'], label='train loss')
    if 'val_loss' in history.history:
        plt.plot(history.history['val_loss'], label='val loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(loss_filepath, dpi=150, bbox_inches='tight')
    plt.close()

def save_acc_plot(history, acc_filename='accuracy.png', time_flag=False):
    '''
    Given a Keras History object, plot & save accuracy curves.

    Args:
        history: keras.callbacks.History returned by model.fit()
        acc_filepath (str): where to save the accuracy plot (PNG).
    '''
    acc_filepath = name_to_dir(name='graph',time_flag=time_flag)+name_time(default_name=acc_filename)
    acc_key = 'accuracy' if 'accuracy' in history.history else 'acc'
    val_acc_key = 'val_' + acc_key
    plt.figure()
    plt.plot(history.history[acc_key], label='train acc')
    if val_acc_key in history.history:
        plt.plot(history.history[val_acc_key], label='val acc')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    plt.savefig(acc_filepath, dpi=150, bbox_inches='tight')
    plt.close()

def get_confusion_mat(y_true, y_pred, name='confusion_matrix', tested_model=None, trained_data='trained_data', tested_data='tested_data', time_flag=False , save_csv=True, save_png=True):
    if tested_model:
        dirname = name_to_dir(name=name)+tested_model+'_'+trained_data+'/'
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        csv_filepath = dirname+tested_data+'.csv'
        png_filepath = dirname+tested_data+'.png'
    else:
        csv_filepath = name_to_filepath(name_ext=name+'.csv',time_flag=time_flag)
        png_filepath = name_to_filepath(name_ext=name+'.png',time_flag=time_flag)

    cm=confusion_matrix(y_true, y_pred)
    if save_png:
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap='Blues')
        plt.title('Confusion Matrix')
        plt.savefig(png_filepath)
    if save_csv:
        np.savetxt(csv_filepath, cm, fmt='%d', delimiter=',')

def get_confusion_mat_size(y_true, y_pred, name='confusion_matrix', tested_model=None, trained_data='trained_data', tested_data='tested_data', time_flag=False , save_csv=True, save_png=True, figsize=(5, 4), fontsize=15):
    if tested_model:
        dirname = name_to_dir(name=name)+tested_model+'_'+trained_data+'/'
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        csv_filepath = dirname+tested_data+'.csv'
        png_filepath = dirname+tested_data+'.png'
    else:
        csv_filepath = name_to_filepath(name_ext=name+'.csv',time_flag=time_flag)
        png_filepath = name_to_filepath(name_ext=name+'.png',time_flag=time_flag)

    cm = confusion_matrix(y_true, y_pred)

    if save_png:
        fig, ax = plt.subplots(figsize=figsize)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap='Blues', ax=ax, colorbar=False)
        
        # 글꼴 크기 조절
        ax.set_title('Confusion Matrix', fontsize=fontsize+2)
        ax.set_xlabel('Predicted label', fontsize=fontsize)
        ax.set_ylabel('True label', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)

        # 안에 있는 숫자(font size 조정)
        for text in disp.ax_.texts:
            text.set_fontsize(fontsize)

        plt.tight_layout()
        plt.savefig(png_filepath)
        plt.close()

    if save_csv:
        np.savetxt(csv_filepath, cm, fmt='%d', delimiter=',')

##############################
##           NAME           ##
##############################

def name_date(default_name,ext=None):
    now = datetime.now()
    time_str = now.strftime('%y%m%d')

    if ext == None:
        if '.' in default_name:
            name, ext = default_name.split('.')
            ext = '.'+ext
            name = name+'_'+time_str+ext
        else:
            name = default_name+'_'+time_str
    else:
        name = default_name+'_'+time_str+ext

    return name

def name_time(default_name,ext=None):
    now = datetime.now()
    time_str = now.strftime('%H%M%S')
    if ext == None:
        if '.' in default_name:
            name, ext = default_name.split('.')
            ext = '.'+ext
            name = name+'_'+time_str+ext
        else:
            name = default_name+'_'+time_str
    else:
        name = default_name+'_'+time_str+ext
    
    return name

def name_to_filepath(name_ext, time_flag=False):
    '''
    return dirname+filename using name_ext
    '''
    if '.' in name_ext:
        name, ext = name_ext.split('.')

    if not time_flag:
        dirname = './'+name+'/'
        filename = name+'.'+ext
    else:
        dirname = './'+name+'/'+name_date(name)+'/'
        filename = name_time(name)+'.'+ext
    
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    
    return dirname+filename

def name_to_dir(name, time_flag=False):
    if not time_flag:
        dirname = './'+name+'/'
    else:
        dirname = './'+name+'/'+name_date(name)+'/'
    
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    
    return dirname

def add_dir_end(dir_path, end_str):
    if not dir_path.endswith('/'):
        dir_path += '/'
    dir_path += end_str
    if not dir_path.endswith('/'):
        dir_path += '/'

    if not os.path.exists(dir_path+end_str):
        os.makedirs(dir_path, exist_ok=True)
    
    return dir_path

##################################
#          Custom Plot           #
##################################
def plot_yk(time, values, x_axis='X', y_axis='Y', show_f=True, save_path=False):
    '''
    plot & save or show.

    Args:
        time (list): x-axis values
        values (list): y-axis values.
        x_axis (str):
        y_axis (str):
        show_f (bool):
        save_path (str):
    '''

    # 그래프
    plt.figure()
    plt.plot(time, values)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(f"{x_axis} vs {y_axis}")
    plt.grid(True)
    if show_f:
        plt.show()
    if save_path:
        plt.savefig(save_path)

def plot_multiple_yk(time_list, values_list, save_name_list=None):
    if save_name_list is not None:
        for time, values, name in zip(time_list, values_list, save_name_list):
            plot_yk(time, values, show_f=False, save_path=f'./data_{name}')
    else:
        for time, values in zip(time_list, values_list):
            plot_yk(time, values, show_f=False)

def plot_sub(i, time, Vo, I_L, Vin, axs, x_lim):
    row = i % 3
    col = i // 3
    ax = axs[row, col]

    # 세 개 데이터 그리기
    ax.plot(time, Vo, label='Vo [V]', color='blue', linewidth=1.5)
    ax.plot(time, I_L, label='I_L [A]', color='green', linewidth=1.5)
    ax.plot(time, Vin, label='Vin [V]', color='red', linewidth=1.5)

    ax.set_title(f"Plot {i+1}", fontsize=14)
    ax.grid(ls=":")
    ax.set_xlim((time[0],time[-1]))

    if row == 2:
        ax.set_xlabel("Time [s]", fontsize=12)

    if col == 0:
        ax.set_ylabel("Voltage / Current\n[V], [A]", fontsize=12)

    ax.legend(loc='best', frameon=False, fontsize=10)
    # 저장하려면 아래 라인 추가
    fig.savefig("multi_plot_voltage_current.png", dpi=600, bbox_inches='tight')

def plot_custom(time, Vo, I_L, Vin, Vo_n, I_L_n, Vin_n, Vo_g, I_L_g, Vin_g, s_time, s_Vo, s_I_L, s_Vin, s_Vo_n, s_I_L_n, s_Vin_n, s_Vo_g, s_I_L_g, s_Vin_g):
    fig, axs = plt.subplots(3, 2, figsize=(10, 10), constrained_layout=True, sharex=True)

    plot_sub(0, time, Vo, I_L, Vin, axs, x_lim=(time[0],time[-1]))
    plot_sub(1, time, Vo_n, I_L_n, Vin_n, axs, x_lim=(time[0],time[-1]))
    plot_sub(2, time, Vo_g, I_L_g, Vin_g, axs, x_lim=(time[0],time[-1]))
    plot_sub(3, s_time, s_Vo, s_I_L, s_Vin, axs, x_lim=(s_time[0],s_time[-1]))
    plot_sub(4, s_time, s_Vo_n, s_I_L_n, s_Vin_n, axs, x_lim=(s_time[0],s_time[-1]))
    plot_sub(5, s_time, s_Vo_g, s_I_L_g, s_Vin_g, axs, x_lim=(s_time[0],s_time[-1]))

    plt.show()

    # 저장하려면 아래 라인 추가
    fig.savefig("multi_plot_voltage_current.png", dpi=600, bbox_inches='tight')

# if __name__ == "__main__":
#     # 예시용 더미 데이터 생성 (실제 데이터로 교체하세요)
#     time = np.linspace(0, 10, 100)  # 시간: 0~10초, 100개 포인트
#     Vo = np.sin(time) * 100 + 300   # Vo: [V]
#     I_L = np.cos(time) * 5 + 10     # I_L: [A]
#     Vin = np.sin(2*time) * 50 + 400  # Vin: [V]

#     plot_custom():

# 각각 subplot으로 따로 그림
def draw_single_subplot(time, Vo, I_L, Vin, title):
    plt.figure(figsize=(15, 7))
    plt.rc('font',size=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(time, Vo, label='Vo [V]', color='blue', linewidth=1.5)
    plt.plot(time, I_L, label='I_L [A]', color='green', linewidth=1.5)
    # plt.plot(time, Vin, label='Vin [V]', color='red', linewidth=1.5)
    plt.grid(ls=':')
    # plt.title(title, fontsize=30)
    plt.xlabel("Time [s]", fontsize=30)
    plt.ylabel("Voltage / Current\n[V], [A]", fontsize=30)
    plt.legend(loc='best', frameon=False, fontsize=20)
    plt.tight_layout()
    # plt.show()
    plt.savefig('./plots/'+title, dpi=1200, bbox_inches='tight')

def draw_fault_subplot(time, true, pred, title):
    plt.figure(figsize=(15, 7))
    plt.rc('font',size=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(time, true, label='true', color='blue', linewidth=1.5)
    plt.plot(time, pred, label='predicted', color='green', linewidth=1.5)
    plt.grid(ls=':')
    # plt.title(title, fontsize=30)
    plt.xlabel("Time [s]", fontsize=30)
    plt.ylabel("Signal", fontsize=30)
    plt.legend(loc='best', frameon=False, fontsize=20)
    plt.tight_layout()
    # plt.show()
    plt.savefig('./plots/'+title, dpi=1200, bbox_inches='tight')

# 각각 subplot으로 따로 그림
def draw_line_subplot(time, Vo, I_L, Vin, title):
    plt.figure(figsize=(15, 7))
    plt.rc('font',size=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.plot(time, Vo, label='Vo [V]', marker='o', linestyle='-',color='blue', linewidth=1.5)
    plt.plot(time, I_L, label='I_L [A]', marker='o', linestyle='-',color='green', linewidth=1.5)
    plt.plot(time, Vin, label='Vin [V]', marker='o', linestyle='-',color='red', linewidth=1.5)
    plt.grid(ls=':')
    plt.title(title, fontsize=30)
    plt.xlabel("Time [s]", fontsize=30)
    plt.ylabel("Voltage / Current\n[V], [A]", fontsize=30)
    plt.legend(loc='best', frameon=False, fontsize=20)
    plt.tight_layout()
    # plt.show()
    plt.savefig('./plots/'+title, dpi=1200, bbox_inches='tight')