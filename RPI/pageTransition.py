import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import math
import interface

# import functions and classes
from googleVision import requestRecognition

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))
backgroundColour = "#263D42"


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        print("uwu " + os.path.realpath(__file__))
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen', True)

        canvas = tk.Canvas(self, bg=backgroundColour)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Set up Menu
        MainMenu(self)

        # Set up Frames
        container = tk.Frame(canvas)
        container.place(relwidth=0.75, relheight=0.75, relx=0.1, rely=0.1)
        # container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LandingPage, RegularItems, CustomItems):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LandingPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def google_vision(self, relativeImgPath, visionFunction):
        with open(workingDir + '/env.json') as f:
            data = json.load(f)
        key = data["api_key"]
        imgpath = workingDir + relativeImgPath
        visionURL = 'https://vision.googleapis.com/v1/images:annotate'

        result = visionFunction(visionURL, key, imgpath)


class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to Ingredients Decoder")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)

        regular_page = tk.Button(self, text="Regular Items", command=lambda: controller.show_frame(RegularItems))
        regular_page.pack()

        custom_page = tk.Button(self, text="Custom Items", command=lambda: controller.show_frame(CustomItems))
        custom_page.pack()

        user_list = tk.Button(self, text="View personalized list",
                              command=lambda: self.show_plist(LandingPage, controller))
        user_list.pack()
        self.user_list = tk.Label()

        testy = tk.Button(self, text="Testy boi",
                          command=lambda: controller.google_vision("/images/download.jpg", requestRecognition))
        testy.pack()

    def refresh(self, label):
        label.destroy()

    def show_plist(self, context, controller):
        URL = "http://52.138.39.36:3000/plist"
        userName = 'customer1'
        PARAMS = {'username': 'customer1'}
        response = requests.post(url=URL, json=PARAMS)
        resJson = response.json()
        userList = []

        self.refresh(self.user_list)
        for element in resJson['message']:
            userList.append(element['p'])
        str1 = ""
        for element in userList:
            str1 += element
            str1 += " "
        self.user_list = tk.Label(controller.frames[context], text='Here is your list: ' + str1)
        self.user_list.pack(padx=10, pady=10)


class RegularItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Scan regular items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)

        scan_items = tk.Button(self, text="Check Ingredients =>")
        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(LandingPage))
        start_page.pack()

        label = tk.Label(self, text="Place item inside box with ingredients list facing camera")
        label.pack()
        promptImg = Image.open(workingDir + "/images/Capture.jpg")
        self.promptImg = ImageTk.PhotoImage(promptImg)
        promptLabel = tk.Label(self, image=self.promptImg)
        promptLabel.pack()

        # display the cropped image
        readImg = Image.open(workingDir + "/images/download.jpg")
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


class CustomItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Scan store custom items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text="Check Ingredients")
        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(LandingPage))
        start_page.pack()

        readImg = Image.open(workingDir + "/images/sushi.bmp")
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


class MainMenu:
    def __init__(self, master):
        print("hello")
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)


app = App()

def pollPicture():
    app.after(3000, pollPicture)
    pictureExists, img = interface.takeImage(workingDir)
    print(pictureExists, img)

pollPicture()

app.mainloop()