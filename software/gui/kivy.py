from tkinter import *
import PIL
from PIL import ImageTk, Image

from tkinter.ttk import *

import PySimpleGUI as sg

import tk_tools

#root = Tk()


# 'n' and 'Classifier' should be replaced with feed from real input from Raspi Camera
#accuracy sample input n = 70
n = 70
#Classifier sample input feed : Recyclable
classifier = "Recyclable"
name = "Plastic Bottle"

yourData1 = ("Recylable or Trash:", classifier)
yourData2 = ("Probability of Object Accuracy:" , n, "%")
yourData3 = ("Object Identified:", name)
#Specifies window and its GUI console name

window = Tk()
window.title("Classification Results")
window.configure(background="light gray")

cond = 'plasticbottleimg'

image = Image.open(str(cond) + '.png')
canvas=Canvas(window, height=200, width=200,highlightthickness=0)
basewidth = 150
wpercent = (basewidth / float(image.size[0]))
hsize = int((float(image.size[1]) * float(wpercent)))
image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
item4 = canvas.create_image(80, 80, image=photo)
canvas.pack(side = TOP, expand=True, fill=BOTH)


#LED to indicate the result - green or red

led = tk_tools.Led(window, size=50)
led.pack()

led.to_red(on=True)
led.to_green()


# Gauge to show percentage Accuracy

gauge = tk_tools.Gauge(window, max_value=100.0,
                       label='Accuracy', unit='%',divisions=8, red_low=50, yellow_low=75, yellow = 100)
gauge.pack()
gauge.set_value(n)


#window.mainloop()

#Specify window size for popup
frame = Frame(window, width=100, height=100)
frame.pack()

#add Ecobin Logo in popup window
#photo1 = PhotoImage(file="ecobin.png")
#Label(window, image=photo1, bg="black") .grid(row=0, column=0, sticky=W)

#name of object Output
lab3 = Label(window,text=yourData3,borderwidth=0)
lab3.pack()

#Classification output
lab1 = Label(window,text=yourData1,borderwidth=0)
lab1.pack()

#Accuracy Output
lab2 = Label(window,text=yourData2,borderwidth=0)
lab2.pack()


window.mainloop()
