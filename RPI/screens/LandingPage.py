import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import math
import interface
from googleVision import *
# from pageTransition import *


class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        import RegularItems as ri
        import CustomItems as ci
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to Ingredients Decoder")
        label.config(font=('comic-sans', 25))
        label.pack(padx=10, pady=10)

        regular_page = tk.Button(self, text="Regular Items", command=lambda: controller.show_frame(ri.RegularItems))
        regular_page.pack()

        custom_page = tk.Button(self, text="Custom Items", command=lambda: controller.show_frame(ci.CustomItems))
        custom_page.pack()

        user_list = tk.Button(self, text="View personalized list",
                              command=lambda: self.show_plist(LandingPage, controller))
        user_list.pack()

        testy = tk.Button(self, text="Testy boi",
                          command=lambda: controller.google_vision("images/download.jpg", requestRecognition))
        testy.pack()

    def show_plist(self, context, controller):
        URL = "http://52.138.39.36:3000/plist"
        userName = 'customer1'
        PARAMS = {'username': 'customer1'}
        response = requests.post(url=URL, json=PARAMS)
        resJson = response.json()
        userList = []

        for element in resJson['message']:
            userList.append(element['p'])
        str1 = ""
        for element in userList:
            str1 += element
            str1 += " "
        user_list = tk.Label(controller.frames[context], text='Here is your list: ' + str1)
        user_list.pack(padx=10, pady=10)
