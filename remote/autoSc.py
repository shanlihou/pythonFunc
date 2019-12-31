from PIL import ImageGrab
import time


def save():
    try:
        pic = ImageGrab.grab()
        pic.save(r'F:\shonedrive\OneDrive\screen.jpg')
    except Exception as e:
        pass


if __name__ == '__main__':
    while True:
        save()
        time.sleep(120)
