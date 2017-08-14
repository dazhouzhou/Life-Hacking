# -*- coding: cp936 -*-
# author: zhou da bao
import win32gui
import sys
import win32con
import win32api
import pyscreenshot as ImageGrab
import time


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
    #time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
def get_red_rgb_counts(im):
    #209 61 75
    width = im.width
    height = im.height

    im = im.load()
    count = 0
    for i in range(0,width):
        for j in range(0,height):
            if im[i,j][0] == 209 and im[i,j][1] == 61 and im[i,j][2] == 75:
                count = count + 1

    return count
    
    
if __name__=="__main__":
    threshold = 11000
    
    hwnd = win32gui.FindWindow("TXGuiFoundation","okok")#

    if hwnd == 0:
        print 'FindWindow error!'
        sys.exit(0)

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


    #(536, 197, 1385, 844)
    win32gui.MoveWindow(hwnd, 536,197,1385-536,844-197,True)

    rect = win32gui.GetWindowRect(hwnd)

    l = rect[2] - rect[0]
    h = rect[3] - rect[1]
    
    # x的坐标 310*414
    m_x = rect[0] + l/2
    m_y = rect[1] + h/2
    
    X_x = m_x + (310/2 - 5)
    X_y = m_y - (414/2 - 5)

    
    while 1:
        # 红包的坐标
        x1 = rect[0]+l*60/842
        y1 = rect[1]+h*320/650

        x2 = rect[2]-l*660/842
        y2 = rect[3]-h*187/650
        im=ImageGrab.grab((x1,y1,x2,y2))

        red_counts = get_red_rgb_counts(im)
        
        # print red_counts
        if  red_counts > threshold:
            rl = x2 - x1
            rh = y2 - y1
            #print rl
            #print rh
            
            x_click = x1 + rl/2
            y_click = y1 + rh/2
            #抢红包
            click(x_click, y_click)
            time.sleep(0.8)
            #关闭红包窗口
            click(X_x, X_y)
            
        else:
            print 'no red'
        

        #break
    
    
        
