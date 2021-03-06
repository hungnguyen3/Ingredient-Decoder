import tkinter as tk
import requests
from PIL import ImageTk, Image
from tkinter import Text
import os

root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, bg = "#263D42")
canvas.pack(fill = tk.BOTH, expand = True)

frame = tk.Frame(root, bg = "white")
frame.place(relwidth=0.75, relheight=0.75, relx = 0.1, rely = 0.1)

label = tk.Label(frame, bg = "white", text = "Ingredients Decoder")
label.config(font=('helvetica', 25))
label.pack()

# get user's list
URL = "http://52.138.39.36:3000/plist"
userName = 'customer1'
PARAMS = {'username': 'customer1'}
userList = requests.post(url = URL, json = PARAMS)
print(userList.json())

yourList = tk.Button(frame, text = "Your personalized list", padx = 10, pady = 5, fg = "white", bg = "black")
yourList.pack()

takePic = tk.Button(frame, text = "Check ingredients", padx = 10, pady = 5, fg = "white", bg = "black")
takePic.pack()

img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/CPEN-391-Ingredient-Decoder/RPI/cat.gif"))
panel = tk.Label(frame, image = img)
panel.pack()

root.mainloop()