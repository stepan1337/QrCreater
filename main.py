import qrcode

text = input("Your Text: ")
img = qrcode.make(text)

print("Name Qr Code: ")
img.save(input()+ ".png")
