import win32con
import win32api



def main():
    _hwnd = 0x0025174A
    win32api.SendMessage(_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)



if __name__ == '__name__':
    main()

