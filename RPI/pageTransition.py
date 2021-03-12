import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import interface
import renderingUtil
import database

# import functions and classes
import googleVision

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))
backgroundColour = "#263D42"


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
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

        # testy = tk.Button(self, text="Testy boi",
        #                   command=lambda: controller.google_vision("/images/download.jpg", googleVision.requestRecognition))
        # testy.pack()

    def show_plist(self, context, controller):
        URL = "http://52.138.39.36:3000/plist"
        userName = 'customer1'
        PARAMS = {'username': 'customer1'}
        response = requests.post(url=URL, json=PARAMS)
        resJson = response.json()
        userList = []

        renderingUtil.refresh(self.user_list)
        for element in resJson['message']:
            userList.append(element["p"])
        str1 = ""
        for element in userList:
            str1 += element.lower()
            str1 += " "
        self.user_list = tk.Label(controller.frames[context], text='Here is your list: ' + str1)
        self.user_list.pack(padx=10, pady=10)


class CommonDisplay:
    def __init__(self, *args, **kwargs):
        readImg = renderingUtil.resizeImage("/images/Capture.jpg")
        self.img = ImageTk.PhotoImage(readImg)
        self.alert = tk.Label()

    def printIntersection(self, warning, matchingArr):
        if not matchingArr:
            self.alert = tk.Label(self, text="No harmful ingredients detected")
            self.alert.pack()
        else:
            renderingUtil.refresh(self.alert)
            warning = "We found the following " + warning + " that you might not want: \n "
            for element in matchingArr:
                warning += element + ", "
            warning = warning[:-2]
            self.alert = tk.Label(self, text=warning)
            self.alert.pack()

    def CheckIngredientsOCR(self, username):
        # get the text from OCR
        responseOCR = googleVision.requestOCR("/images/download.jpg")
        # get user plist
        userList = database.Get_Personal_List(username)
        # get the matching array
        matchingArr = googleVision.getMatchingArr(responseOCR, userList)
        self.printIntersection("ingredients matching your personal list", matchingArr)

    def CheckIngredientsRecognition(self, username):
        # get the text from OCR
        responseRec = googleVision.requestRecognition("/images/download.jpg")
        responseRec = database.Get_Custom_Ingredients(responseRec)
        # get user plist
        userList = database.Get_Personal_List(username)
        # get the matching array
        matchingArr = googleVision.getMatchingArr(responseRec, userList)
        self.printIntersection("ingredients matching your personal list", matchingArr)

    def CheckHarmfulOCR(self):
        responseOCR = googleVision.requestOCR("/images/download.jpg")
        harmfulList = database.Get_Harmful_List()
        matchingArr = googleVision.getMatchingArr(responseOCR, harmfulList)
        self.printIntersection("generally harmful ingredients", matchingArr)

    def CheckHarmfulRecognition(self):
        responseRec = googleVision.requestRecognition("/images/download.jpg")
        responseRec = database.Get_Custom_Ingredients(responseRec)
        harmfulList = database.Get_Harmful_List()
        matchingArr = googleVision.getMatchingArr(responseRec, harmfulList)
        self.printIntersection("generally harmful ingredients", matchingArr)


class RegularItems(tk.Frame, CommonDisplay):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        CommonDisplay.__init__(self)

        label = tk.Label(self, text="Scan regular items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)

        scan_items = tk.Button(self, text="Check Ingredients =>",
                               command=lambda: self.CheckIngredientsOCR("customer1"))
        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(LandingPage))
        start_page.pack()

        self.instruction = tk.Label(self, text="Place item inside box with ingredients list facing camera")
        self.instruction.pack()

        self.promptLabel = tk.Label(self, image=self.img)
        self.promptLabel.pack()

        self.alert = tk.Label(self, text="")


class CustomItems(tk.Frame, CommonDisplay):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        CommonDisplay.__init__(self)

        label = tk.Label(self, text="Scan store custom items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text="Check Ingredients",
                               command=lambda: self.CheckIngredientsOCR("customer1"))

        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(LandingPage))
        start_page.pack()

        self.instruction = tk.Label(self, text="Place item inside box with ingredients list facing camera")
        self.instruction.pack()

        self.promptLabel = tk.Label(self, image=self.img)
        self.promptLabel.pack()


class MainMenu:
    def __init__(self, master):
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)


app = App()


def loadProcessedImage(frame):
    # tell users to make google vision call
    renderingUtil.refresh(app.frames[frame].instruction)
    app.frames[frame].instruction = tk.Label(app.frames[frame], text="Your item is ready to be scanned")
    app.frames[frame].instruction.pack()

    # change the image
    renderingUtil.refresh(app.frames[frame].promptLabel)
    readImg = renderingUtil.resizeImage("/images/download.jpg")
    app.frames[frame].img = ImageTk.PhotoImage(readImg)
    app.frames[frame].promptLabel = tk.Label(app.frames[frame], image=app.frames[frame].img)
    app.frames[frame].promptLabel.pack()


def pollPicture():
    app.after(1000, pollPicture)
    pictureExists, img = interface.takeImage(workingDir)
    if pictureExists:
        # change the image for regular items
        loadProcessedImage(RegularItems)

        # change the image for custom items
        loadProcessedImage(CustomItems)


app.after(3000, pollPicture())

app.mainloop()
