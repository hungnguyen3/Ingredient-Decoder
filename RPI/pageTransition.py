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

# import functions and classes
import googleVision

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))
backgroundColour = "#263D42"

pictureExists = False
newPicture = False
acceptNextImage = True
objectImg = "/images/testyboi.jpg"
buffer = None
imageAltBit = 0
queue = mp.Queue()


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
        self.user_list = tk.Label(controller.frames[context], text='Here is your list: ' + str1)
        self.user_list.pack(padx=10, pady=10)


class CommonDisplay:
    def __init__(self, controller, parent, message, scanFunction, *args, **kwargs):
        readImg = renderingUtil.resizeImage("/images/Capture.jpg")
        self.img = ImageTk.PhotoImage(readImg)
        self.alert = tk.Label()

        # CommonDisplay.__init__(self)

        label = tk.Label(self, text=message)
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text="Check Ingredients",
                               command=lambda: scanFunction("customer1"))

        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(LandingPage))
        start_page.pack()

        self.instruction = tk.Label(self, text="Place item inside box with ingredients list facing camera")
        self.instruction.pack()

        self.promptLabel = tk.Label(self, image=self.img)
        self.promptLabel.pack()

        self.checkNewItem = tk.Button(self, text="CLick here to check another item",
                                      command=lambda: self.MakeAcceptNextImage())
        self.checkNewItem.pack()

    def printIntersection(self, warning, matchingArr):
        renderingUtil.refresh(self.alert)
        if matchingArr == "notOCR":
            self.alert = tk.Label(self, text="No ingredients text detected")
            self.alert.pack()
            return
        if matchingArr == "notRecognition":
            self.alert = tk.Label(self, text="Not recognized as a store custom item. Maybe try regular item instead?")
            self.alert.pack()
            return
        if not matchingArr:
            self.alert = tk.Label(self, text="No harmful ingredients detected")
            self.alert.pack()
        else:
            warning = "We found the following " + warning + " that you might not want: \n "
            for element in matchingArr:
                warning += element + ", "
            warning = warning[:-2]
            self.alert = tk.Label(self, text=warning)
            self.alert.pack()

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
        responseRec = googleVision.requestRecognition(objectImg)
        responseRec = database.Get_Custom_Ingredients(responseRec)
        # get user plist
        userList = database.Get_Personal_List(username)
        # get the matching array
        matchingArr = googleVision.getMatchingArr(responseRec, userList)
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

    def noImg(self):
        if objectImg is None:
            self.alert = tk.Label(self,
                                  text="No object detected, or image has not loaded yet. \n PLease wait for image of object to show up before attempting scan")
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
    app.frames[frame].instruction = tk.Label(app.frames[frame], text="Your item is ready to be scanned")
    app.frames[frame].instruction.pack()

    # change the image
    renderingUtil.refresh(app.frames[frame].promptLabel)
    readImg = renderingUtil.resizeImage(objectImg)
    app.frames[frame].img = ImageTk.PhotoImage(readImg)
    app.frames[frame].promptLabel = tk.Label(app.frames[frame], image=app.frames[frame].img)
    app.frames[frame].promptLabel.pack()


# def pollPicture():
#     app.after(1000, pollPicture)
#
#     global pictureExists
#     global newPicture
#     global buffer
#     global acceptNextImage
#     global objectImg
#     pictureExists, img, newPicture = interface.takeImage()  # sets newPicture to false after first call
#
#     if pictureExists and newPicture:
#         buffer = img
#
#         if acceptNextImage:
#             objectImg = buffer
#             print(objectImg)
#             loadProcessedImage(RegularItems)
#             loadProcessedImage(CustomItems)
#             acceptNextImage = False

def pollPicture():
    global acceptNextImage
    global objectImg
    global imageAltBit
    global queue
    if not queue.empty():
        print("not empty")
        newAltBit = queue.get()
        if newAltBit != imageAltBit and newAltBit != 0:
            print("actual image!")
            imageAltBit = newAltBit

            if acceptNextImage:
                loadProcessedImage(RegularItems)
                loadProcessedImage(CustomItems)
                acceptNextImage = False
    app.after(1, pollPicture)

# def pollPicture():
#     app.after(1000, pollPicture)
#     print("uwu")

app.after(3000, pollPicture)
if __name__ == "__main__":
    producer = mp.Process(target=testy.produceImage, args=(queue,))
    producer.start()
    app.mainloop()



#
