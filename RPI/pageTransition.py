import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import interface
import renderingUtil
import database
import multiprocessing as mp
import testyboi as testy
import time
# import Camera.camera as camera
import cv2

#cap = cv2.VideoCapture(0)

# import functions and classes
import googleVision

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))
backgroundColour = "#263D42"

pictureExists = False
newPicture = False
acceptNextImage = True
objectImg = "/images/download.jpg"
buffer = None
imageQueue = mp.Queue()
ackQueue = mp.Queue()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self, bg=backgroundColour)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set up Menu
        MainMenu(self)

        # Set up Frames
        container = tk.Frame(self.canvas)
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
        label.config(font=('helvetica', 30))
        label.pack(padx=10, pady=10)

        regular_page = tk.Button(self, text="Regular Items", height = 2, font=('helvetica', 15), command=lambda: controller.show_frame(RegularItems))
        regular_page.pack()

        custom_page = tk.Button(self, text="Custom Items", height = 2, font=('helvetica', 15), command=lambda: controller.show_frame(CustomItems))
        custom_page.pack()

        user_list = tk.Button(self, text="View personalized list", height = 2, font=('helvetica', 15),
                              command=lambda: self.show_plist(LandingPage, controller))
        user_list.pack()
        self.user_list = tk.Label()

        # why gif not running~
        self.img = ImageTk.PhotoImage(Image.open(workingDir + "/images/cat.gif"))
        welcomeImg = tk.Label(self, image=self.img)
        welcomeImg.pack()
        # testy = tk.Button(self, text="Testy boi",
        #                   command=lambda: controller.google_vision("/images/sushiOut.bmp", googleVision.requestRecognition))
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
        self.user_list = tk.Label(controller.frames[context], text='Here is your list: ' + str1, font=('helvetica', 15))
        self.user_list.pack(padx=10, pady=10)


class CommonDisplay:
    def __init__(self, controller, parent, message, scanFunction, *args, **kwargs):
        self.infoButtonList = []
        self.counter = 0

        readImg = renderingUtil.resizeImage("/images/Capture.jpg")
        self.img = ImageTk.PhotoImage(readImg)
        self.alert = tk.Label()

        # CommonDisplay.__init__(self)

        label = tk.Label(self, text=message)
        label.config(font=('helvetica', 30))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text="Check Ingredients", height = 2, font=('helvetica', 15),
                               command=lambda: scanFunction("customer1"))

        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", height = 2, font=('helvetica', 15), command=lambda: controller.show_frame(LandingPage))
        start_page.pack()

        self.instruction = tk.Label(self, text="Place item inside box with ingredients list facing camera", font=('helvetica', 15))
        self.instruction.pack()

        self.promptLabel = tk.Label(self, image=self.img)
        self.promptLabel.pack()

        self.checkNewItem = tk.Button(self, text="Click here to check another item", height = 2, font=('helvetica', 15),
                                      command=lambda: self.MakeAcceptNextImage())
        self.checkNewItem.pack()

    def printIntersection(self, warning, matchingArr):
        renderingUtil.refresh(self.alert)
        if matchingArr == "notOCR":
            self.alert = tk.Label(self, text="No ingredients text detected", font=('helvetica', 15))
            self.alert.pack()
            return
        if matchingArr == "notRecognition":
            self.alert = tk.Label(self, text="Not recognized as a store custom item. Maybe try regular item instead?", font=('helvetica', 15))
            self.alert.pack()
            return
        if not matchingArr:
            self.alert = tk.Label(self, text="No harmful ingredients detected", font=('helvetica', 15))
            self.alert.pack()
        else:
            warning = "We found the following " + warning + " that you might not want: \n "
            for element in matchingArr:
                warning += element + ", "
            warning = warning[:-2]
            self.alert = tk.Label(self, text=warning, font=('helvetica', 15))
            self.alert.pack()

    def printIngredients(self, arg):
        # list = tk.Label(self,
        #          text=arg,
        #          font=('helvetica', 15))
        # list.pack()

        height = 5
        width = 5
        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(app.canvas, text="")
                b.grid(row=i, column=j)


    def customItemEntry(self, itemName, itemIngredients):
        # print('making items')
        # print(itemName)
        # print(itemIngredients)

        infoButton = tk.Button(self, text=itemName, font=('helvetica', 15), command=lambda: self.printIngredients(itemIngredients))
        infoButton.pack()
        self.infoButtonList.append(infoButton)


    def CheckIngredientsOCR(self, username):
        if self.noImg():
            return
        # get the text from OCR
        responseOCR = googleVision.requestOCR(objectImg)
        # get user plist
        userList = database.Get_Personal_List(username)
        # get the matching array
        matchingArr = googleVision.getMatchingArr(responseOCR, userList)
        self.printIntersection("ingredients matching your personal list", matchingArr)

    def CheckIngredientsRecognition(self, username):
        if self.noImg():
            return
        # get the text from OCR
        tags_array = googleVision.requestRecognition(objectImg)
        ingredients_array = database.Get_Custom_Ingredients(tags_array)
        print("uwu")
        print(tags_array)
        print(ingredients_array)

        for i in self.infoButtonList:
            renderingUtil.refresh(i)
        self.infoButtonList.clear()
        for i in range(0, len(tags_array)):
            if ingredients_array[i] != '0':
                self.customItemEntry(itemName=tags_array[i], itemIngredients=ingredients_array[i])
                print("make custom items here")

        userList = database.Get_Personal_List(username)
        # get the matching array
        matchingArr = googleVision.getMatchingArr(ingredients_array, userList)
        self.printIntersection("ingredients matching your personal list", matchingArr)

    def CheckHarmfulOCR(self):
        if self.noImg():
            return
        responseOCR = googleVision.requestOCR(objectImg)
        harmfulList = database.Get_Harmful_List()
        matchingArr = googleVision.getMatchingArr(responseOCR, harmfulList)
        self.printIntersection("generally harmful ingredients", matchingArr)

    def CheckHarmfulRecognition(self):
        if self.noImg():
            return
        responseRec = googleVision.requestRecognition(objectImg)
        responseRec = database.Get_Custom_Ingredients(responseRec)
        harmfulList = database.Get_Harmful_List()
        matchingArr = googleVision.getMatchingArr(responseRec, harmfulList)
        self.printIntersection("generally harmful ingredients", matchingArr)

    def MakeAcceptNextImage(self):
        global acceptNextImage
        acceptNextImage = True
        actualPoll()

    def noImg(self):
        if objectImg is None:
            self.alert = tk.Label(self,
                                  text="No object detected, or image has not loaded yet. \n PLease wait for image of object to show up before attempting scan",
                                  font=('helvetica', 15))
            self.alert.pack()
            return True
        return False


class RegularItems(tk.Frame, CommonDisplay):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        CommonDisplay.__init__(self, message="Scan regular items here", scanFunction=self.CheckIngredientsOCR,
                               parent=parent, controller=controller)


class CustomItems(tk.Frame, CommonDisplay):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        CommonDisplay.__init__(self, message="Scan store custom items here",
                               scanFunction=self.CheckIngredientsRecognition, parent=parent, controller=controller)


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
    global app
    renderingUtil.refresh(app.frames[frame].instruction)
    try:
        tryOpen = Image.open(workingDir + objectImg)
        app.frames[frame].instruction = tk.Label(app.frames[frame], text="Your item is ready to be scanned", font=('helvetica', 15))
    except OSError:
        print('cannot open')
        app.frames[frame].instruction = tk.Label(app.frames[frame], text="Please place an item in front of the camera", font=('helvetica', 15))
    app.frames[frame].instruction.pack()

    # change the image
    renderingUtil.refresh(app.frames[frame].promptLabel)
    readImg = renderingUtil.resizeImage(objectImg)
    app.frames[frame].img = ImageTk.PhotoImage(readImg)
    app.frames[frame].promptLabel = tk.Label(app.frames[frame], image=app.frames[frame].img)
    app.frames[frame].promptLabel.pack()


def pollPicture():
    app.after(1000, pollPicture)

    global pictureExists
    global newPicture
    global buffer
    global acceptNextImage
    global objectImg
    pictureExists, img, newPicture = interface.takeImage()  # sets newPicture to false after first call

    if pictureExists and newPicture:
        buffer = img

        if acceptNextImage:
            objectImg = buffer
            print(objectImg)
            loadProcessedImage(RegularItems)
            loadProcessedImage(CustomItems)
            acceptNextImage = False
#
# def pollPicture():
#     actualPoll()
#     app.after(1000, pollPicture)


def actualPoll():
    global acceptNextImage
    global objectImg
    global imageQueue
    global ackQueue
    if not imageQueue.empty():
        print("not empty")
        imageQueue.get()
        if acceptNextImage:
            loadProcessedImage(RegularItems)
            loadProcessedImage(CustomItems)
            # acceptNextImage = False
        ackQueue.put(True)


# def pollPicture():
#     app.after(1000, pollPicture)
#     print("uwu")

app.after(3000, pollPicture)
# if __name__ == "__main__":
#     producer = mp.Process(target=camera.run, args=(imageQueue, ackQueue))
#     producer.start()
#     ackQueue.put(True)
#     app.mainloop()

app.mainloop()