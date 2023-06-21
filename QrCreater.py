import qrcode
from plyer import notification
import time
import sys

text = input("Your Text: ")
img = qrcode.make(text)

print("Name Qr Code: ")
img.save(input()+ ".png")

notification.notify(message="Qr Code находится в папке с программой",
                          app_name="Qr Creater",
                          title="Qr code создан!",
                          app_icon="C:/Users/stepan/Desktop/qr Generated/venv/ico.ico")

print("Нажмите любую клавишу для закрытия")
input()
