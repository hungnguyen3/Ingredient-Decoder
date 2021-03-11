import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import math
import interface
from googleVision import *
# from pageTransition import *


class RegularItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Scan regular items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)

        scan_items = tk.Button(self, text="Check Ingredients =>")
        scan_items.pack()
        import LandingPage as lp
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(lp.LandingPage))
        start_page.pack()

        label = tk.Label(self, text="Place item inside box with ingredients list facing camera")
        label.pack()
        promptImg = Image.open("images/Capture.jpg")
        self.promptImg = ImageTk.PhotoImage(promptImg)
        promptLabel = tk.Label(self, image=self.promptImg)
        promptLabel.pack()

        # display the cropped image
        readImg = Image.open("images/download.jpg")
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
