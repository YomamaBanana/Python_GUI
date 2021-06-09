import cv2
import time
import datetime
import numpy as np
import tkinter as Tk
import PySimpleGUI as sg
from matplotlib import pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import imutils



sg.theme('Dark Blue 3')


s_button_13 = sg.Submit('Capture of convert image', size=(10, 5))
s_button_14 = sg.Submit('Capture of original image', size=(10, 5))
s_button_15 = sg.Submit('Capture of histgram', size=(10, 5))
s_button_16 = sg.Submit('Quit', size=(10, 5), button_color=('black', '#4adcd6'))

layout_3 = sg.Frame(layout=[[s_button_13],
                            [s_button_14],
                            [s_button_15],
                            [s_button_16]],
                          title='',
                          title_color='white',
                          font=('メイリオ', 8),
                          relief=sg.RELIEF_SUNKEN)


original_image = [[sg.Image(filename='', key='-orginal_img-')], [sg.Image(filename='', key='-modify_img-')]]
modify_image = [[sg.Image(filename='', key='-modify_img-')]]

#read 
read_layout = [[sg.Text("File"), sg.InputText(key='-input_file-', enable_events=True, ),
                sg.FileBrowse('Browse', key='-file-', target="-input_file-",), sg.Button('Read', key='-read_file-')],
                [sg.Button('Save',key='-save-'),sg.Cancel()],
                [sg.Slider((0, 255), 0, 1, orientation='h', key='-THRESH SLIDER-'),
                sg.InputText(default_text='0',size=(5,1),key='-thslid-')]]

# hist
hist_graph = [[sg.Image(filename='', key='-hist_img-')]]


layout_tot= [[sg.Frame(title='Read',layout=read_layout),sg.Frame(title='Histgram',layout=hist_graph),
             sg.Frame(title='Original',layout=original_image)],[layout_3]]


# flag
READ_File = False

sg.theme('Dark Blue 3')

window = sg.Window('Threshold', layout_tot,
                   location=(10, 10),alpha_channel=1.0,
                   no_titlebar=False,grab_anywhere=False).Finalize()



READ_File = False

while True:

    event, values = window.read(timeout=20)

    if event in (None, 'Cancel'):
        break

    elif event == '-read_file-':
        # print(values['-input_file-'])
        read_path = values["-input_file-"]
        read_img = cv2.imread(str(read_path), cv2.IMREAD_COLOR)
        read_img = imutils.resize(read_img, width=300)
        
        img_bytes = cv2.imencode('.png', read_img)[1].tobytes()
        
        window['-orginal_img-'].update(data=img_bytes)


        window['-modify_img-'].update(data=img_bytes)










exit()

# ウィンドウの色設定
sg.theme('Dark Blue 3')

### リアルタイムでヒストグラムを表示させるための関数 ###
def draw_plot(img_f):
        
    # プロットの初期化
    plt.clf()
        
    # RGBごとのヒストグラム計算とプロット
    for i, channel in enumerate(("r", "g", "b")):
            histgram = cv2.calcHist([img_f], [i], None, [256], [0, 256])
            plt.plot(histgram, color = channel)
            plt.xlim([0, 256])
                
    # プロットの更新間隔、カッコの中は時間(msec)
    # 表示が安定しない場合は時間をかえてみる
    plt.pause(0.01)

### PySimpleGUIでGUIを作成するための準備 ###
# ラジオボタン、スライダー設定
s_button_0 = sg.Radio('None', 'Radio', True, size=(10, 1))
s_button_1 = sg.Radio('Threshold', 'Radio', size=(10, 1), key='-THRESH-')
s_button_2 = sg.Slider((0, 255), 128, 1, orientation='h', size=(47, 15), key='-THRESH SLIDER-')
s_button_3 = sg.Radio('Canny', 'Radio', size=(10, 1), key='-CANNY-')
s_button_4 = sg.Slider((0, 255), 128, 1, orientation='h', size=(23, 15), key='-CANNY SLIDER A-')
s_button_5 = sg.Slider((0, 255), 128, 1, orientation='h', size=(23, 15), key='-CANNY SLIDER B-')
s_button_6 = sg.Radio('Blur', 'Radio', size=(10, 1), key='-BLUR-')
s_button_7 = sg.Slider((1, 11), 1, 1, orientation='h', size=(47, 15), key='-BLUR SLIDER-')
s_button_8 = sg.Radio('Hue', 'Radio', size=(10, 1), key='-HUE-')
s_button_9 = sg.Slider((0, 225), 0, 1, orientation='h', size=(47, 15), key='-HUE SLIDER-')
s_button_10 = sg.Radio('Enhance', 'Radio', size=(10, 1), key='-ENHANCE-')
s_button_11 = sg.Slider((1, 255), 128, 1, orientation='h', size=(47, 15), key='-ENHANCE SLIDER-')
s_button_12 = sg.Radio('Histgram', 'Radio', size=(10, 1), key='-hist-')

# 押しボタン設定
s_button_13 = sg.Submit('Capture of convert image', size=(30, 10))
s_button_14 = sg.Submit('Capture of original image', size=(30, 10))
s_button_15 = sg.Submit('Capture of histgram', size=(30, 10))
s_button_16 = sg.Submit('Quit', size=(30, 20), button_color=('black', '#4adcd6'))

# 映像定義
frame3 = sg.Image(filename='', key='-IMAGE-')    # 変換後の映像
frame4 = sg.Image(filename='', key='-IMAGE_2-')  # オリジナル映像
frame5 = sg.Canvas(size=(1, 1), key='canvas')    # ヒストグラムを別画面で表示させるのに必要

# オリジナル映像の画面設定
frame1 = sg.Frame(layout=[[frame4]],
                        title='original image',
                        title_color='white',
                        font=('メイリオ', 12),
                        relief=sg.RELIEF_SUNKEN,
                        element_justification='left')

# ラジオボタンとスライダーの画面設定
frame2 = sg.Frame(layout=[[s_button_0],
                          [s_button_1, s_button_2],
                          [s_button_3, s_button_4, s_button_5],
                          [s_button_6, s_button_7],
                          [s_button_8, s_button_9],
                          [s_button_10, s_button_11],
                          [s_button_12]],
                        title='parameter',
                        title_color='white',
                        font=('メイリオ', 12),
                        relief=sg.RELIEF_SUNKEN,
                        element_justification='left')

# オリジナル映像とラジオボタンとスライダー類を一つのレイアウトにまとめる
layout_1 = sg.Frame(layout=[[frame1],
                            [frame2],
                            [frame5]],
                          title='',
                          title_color='white',
                          font=('メイリオ', 10),
                          relief=sg.RELIEF_SUNKEN)

# 変換後の映像の画面設定 
layout_2 = sg.Frame(layout=[[frame3]],
                          title='',
                          title_color='white',
                          font=('メイリオ', 10),
                          relief=sg.RELIEF_SUNKEN)

# 押しボタンのレイアウト設定
layout_3 = sg.Frame(layout=[[s_button_13],
                            [s_button_14],
                            [s_button_15],
                            [s_button_16]],
                          title='',
                          title_color='white',
                          font=('メイリオ', 10),
                          relief=sg.RELIEF_SUNKEN)

### レイアウトまとめ ###
layout = [
          [layout_2, layout_1, layout_3],
         ]

### 画面表示の設定 ###
window = sg.Window('tomo viewer 2', layout,
                                    location=(30, 30),
                                    alpha_channel=1.0,
                                    no_titlebar=False,
                                    grab_anywhere=False).Finalize()

# ヒストグラム表示の設定
canvas_elem = window['canvas']
canvas = canvas_elem.TKCanvas

### キャプチャ設定 ###
cap = cv2.VideoCapture(0)

cap.set(3, 1920)
cap.set(4, 1080)
cap.set(5, 30)

# 初期値
fps = ""

while True:

    # 時間測定開始(FPS計算のため)
    t1 = time.perf_counter()

    event, values = window.read(timeout=20)

    if event == 'Quit' or event == sg.WIN_CLOSED:
        break

    _, img = cap.read()

    # 映像をトリミング
    img_1 = img[90:990, 510:1410]
    img_2 = img[90:990, 510:1410]

    # オリジナル映像をリサイズ
    img_3 = cv2.resize(img_2, (550, 550), cv2.INTER_LANCZOS4)
        
    ### 変換後の画像 ###
    if values['-THRESH-']:
        img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2LAB)[:, :, 0]
        img_1 = cv2.threshold(img_1, values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)[1]

    elif values['-CANNY-']:
        img_1 = cv2.Canny(img_1, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])

    elif values['-BLUR-']:
        img_1 = cv2.GaussianBlur(img_1, (21, 21), values['-BLUR SLIDER-'])

    elif values['-HUE-']:
        img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
        img_1[:, :, 0] += int(values['-HUE SLIDER-'])
        img_1 = cv2.cvtColor(img_1, cv2.COLOR_HSV2BGR)

    elif values['-ENHANCE-']:
        enh_val = values['-ENHANCE SLIDER-'] / 40
        clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
        lab = cv2.cvtColor(img_1, cv2.COLOR_BGR2LAB)
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        img_1 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    if values['-hist-']:
        # ヒストグラムは別画面で表示
        canvas.create_image(300, 300, image=draw_plot(img_1))

    ### 各種画像保存 ###
    # 日付の取得(ファイル名に使用する準備)
    d_today = datetime.date.today()
    dt_now = datetime.datetime.now()

    # ヒストグラム画像
    if event == 'Capture of histgram':
        plt.savefig('./cnn_act/capture/' +
                       str(d_today) + str("_") +
                       str(dt_now.hour) + str("_") +
                       str(dt_now.minute) + str("_") +
                       str(dt_now.second) + '.png')
        
    # 変換後の画像
    if event == 'Capture of convert image':   
        cv2.imwrite('./cnn_act/capture/' +
                       str(d_today) + str("_") +
                       str(dt_now.hour) + str("_") +
                       str(dt_now.minute) + str("_") +
                       str(dt_now.second) + '.jpg', img_1)

    # オリジナル画像
    if event == 'Capture of original image':
        cv2.imwrite('./cnn_act/capture/' +
                       str(d_today) + str("_") +
                       str(dt_now.hour) + str("_") +
                       str(dt_now.minute) + str("_") +
                       str(dt_now.second) + '.jpg', img_2)

    ### FPS 計算 ###
    elapsedTime = time.perf_counter() - t1
    fps = "{:.0f}FPS".format(1/elapsedTime)

    ### 画面にFPS表示 ###
    frame_1 = cv2.putText(img_1, fps, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv2.LINE_AA)

    ### 画面更新 ###
    imgbytes = cv2.imencode('.png', img_1)[1].tobytes()
    window['-IMAGE-'].update(data=imgbytes)

    imgbytes_2 = cv2.imencode('.png', img_3)[1].tobytes()
    window['-IMAGE_2-'].update(data=imgbytes_2)

window.close()