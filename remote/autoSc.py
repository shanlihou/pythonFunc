from PIL import ImageGrab
import time


def save():
    pic = ImageGrab.grab()
    pic.save(r'F:\shonedrive\OneDrive\screen.jpg')


if __name__ == '__main__':
    while True:
        save()
        time.sleep(1200)
