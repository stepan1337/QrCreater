from tkinter import*

root = Tk()

root.title("Qr Creater")
root.geometry("400x500")
root.iconname()
root["bg"] = "silver"

def get():
    label1["text"] = e.get()

btn1 = Button(root, text= "Create", font=90,command=get)
btn1.pack(side=BOTTOM,padx=40)

label1 = Label(root,bg="silver",fg="black",font=120)
label1.pack(pady=5)

e = Entry(root,font=90,fg="black")
e.pack()

e.insert(0,"Введите текст")

root.mainloop()