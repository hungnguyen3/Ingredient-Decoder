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
        import screens.LandingPage as lp
        import screens.RegularItems as ri
        import screens.CustomItems as ci
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

        for F in (lp.LandingPage, ri.RegularItems, ci.CustomItems):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(lp.LandingPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def google_vision(self, relativeImgPath, visionFunction):
        with open(workingDir + '/env.json') as f:
            data = json.load(f)
        key = data["api_key"]
        imgpath = relativeImgPath
        visionURL = 'https://vision.googleapis.com/v1/images:annotate'

        result = visionFunction(visionURL, key, imgpath)







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
