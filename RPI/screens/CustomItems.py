import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import math
import interface
from googleVision import *
# from pageTransition import *

class CustomItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Scan store custom items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text="Check Ingredients")
        scan_items.pack()
        import LandingPage as lp
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(lp.LandingPage))
        start_page.pack()

        readImg = Image.open("images/sushi.bmp")
        width = readImg.width
        height = readImg.height
        while height > 500 or width > 500:
            height = height * 0.9
            width = width * 0.9
        width = math.floor(width)
        height = math.floor(height)
        readImg = readImg.resize((width, height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(readImg)
        panel = tk.Label(self, image=self.img)
        panel.pack()