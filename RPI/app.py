import json
import tkinter as tk
import requests
from PIL import ImageTk, Image
import os
import interface
import renderingUtil
import database
import multiprocessing as mp
from functools import partial
import ctypes
import testyboi as testy
import time
import Camera.camera as camera
import cv2

# import functions and classes
import googleVision

# current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))
backgroundColour = "#263D42"

# global variables used between multiple processes
pictureExists = False
newPicture = False
acceptNextImage = True
objectImg = "/images/download.jpg"
buffer = None
imageQueue = mp.Queue()
ackQueue = mp.Queue()

# class app is an instantiation of the touchscreen app. 
# It contains several pages including Login Page, Landing Page, Regular Items Page and Custom Items page
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self, bg=backgroundColour)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set up Menu
        MainMenu(self)

        # Set up Frames for different pages
        container = tk.Frame(self.canvas)
        container.place(relwidth=0.75, relheight=0.85, relx=0.1, rely=0.1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # switch between different pages
        for F in (LandingPage, RegularItems, CustomItems, LoginPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

# class LoginPage is the login page of the touchscreen app
# from this page you can log in as a guest or log in using bluetooth functionality
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to Ingredients Decoder")
        label.config(font=('helvetica', 30))
        label.pack(padx=10, pady=10)

        guest_login = tk.Button(self, text="Log in as a guest", height = 2, font=('helvetica', 15), command= lambda: self.loginAsGuest())
        guest_login.pack()

        bt_login = tk.Button(self, text="Log in using bluetooth", height = 2, font=('helvetica', 15), command=lambda: self.loginBT())
        bt_login.pack()

        self.loginStatus = tk.Label(self, text="Please log in to continue", height = 2, font=('helvetica', 15))
        self.loginStatus.pack()
        self.continue_button = tk.Button()
        self.controllor = controller

    # log in as a guest
    def loginAsGuest(self):
        renderingUtil.refresh(self.loginStatus)
        self.loginStatus = tk.Label(self, text="You have successfully loged in as guest", height = 2, font=('helvetica', 15))
        self.loginStatus.pack()
        renderingUtil.refresh(self.continue_button)
        self.continue_button = tk.Button(self, text="Continue", height = 2, font=('helvetica', 15), command= lambda: self.continueToLanding())
        self.continue_button.pack()

    # start browsing for a bluetooth login
    def loginBT(self):
        textInput = "Browsing for a bluetooth login.... "
        renderingUtil.refresh(self.loginStatus)
        self.loginStatus = tk.Label(self, text=textInput, height = 2, font=('helvetica', 15))
        self.loginStatus.pack()
        renderingUtil.refresh(self.continue_button)

    # go to Landing page, reset the login status and delete the continue button
    def continueToLanding(self):
        self.controllor.show_frame(LandingPage)
        renderingUtil.refresh(self.loginStatus)
        self.loginStatus = tk.Label(self, text="Please log in to continue", height = 2, font=('helvetica', 15))
        self.loginStatus.pack()
        renderingUtil.refresh(self.continue_button)

# class LandingPage is the landing page of the touchscreen app after you're signed in
# from this page you can proceed to scan Regular Items, scan Custom Items or check out Personalized List
class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # welcome labels, buttons to navigate to different pages of the app
        label = tk.Label(self, text="You have successfully loged in")
        label.config(font=('helvetica', 30))
        label.pack(padx=10, pady=10)

        regular_page = tk.Button(self, text="Regular Items", height = 2, font=('helvetica', 15), command=lambda: controller.show_frame(RegularItems))
        regular_page.pack()

        custom_page = tk.Button(self, text="Custom Items", height = 2, font=('helvetica', 15), command=lambda: controller.show_frame(CustomItems))
        custom_page.pack()

        user_list = tk.Button(self, text="View personalized list", height = 2, font=('helvetica', 15),
                              command=lambda: self.show_plist(LandingPage, controller))
        user_list.pack()

        login_page = tk.Button(self, text="Log out", height = 2, font=('helvetica', 15), command=lambda: controller.show_frame(LoginPage))
        login_page.pack()

        self.user_list = tk.Label()

        # welcome image of a cute cat
        readImg = renderingUtil.resizeImage("/images/cat.gif")
        self.img = ImageTk.PhotoImage(readImg)
        welcomeImg = tk.Label(self, image=self.img)
        welcomeImg.pack()

    # API call to the backend to retrieve the personalized list of the customer
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

# class CommonDisplay is a common generic page
# both RegularItems and CustomItems classes would inherit from this class.
# it contains several buttons and labels displayed back to the users
class CommonDisplay:
    def __init__(self, controller, parent, message, scanFunction, *args, **kwargs):
        self.infoButtonList = []
        self.counter = 0
        self.itemList = [None]*20 #20 items max
        self.ingredientsList = [None]*20
        self.subcanvas = tk.Canvas()

        readImg = renderingUtil.resizeImage("/images/Capture.jpg")
        self.img = ImageTk.PhotoImage(readImg)
        self.alert = tk.Label()

        # buttons to check ingredients, go back to home page and instructions labels for the users
        label = tk.Label(self, text=message)
        label.config(font=('helvetica', 30))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text="Check Ingredients", height = 2, font=('helvetica', 15),
                               command=lambda: scanFunction("customer1"))

        scan_items.pack()
        start_page = tk.Button(self, text="Back to Home Page", height = 2, font=('helvetica', 15), command=lambda: self.backToHomePage(controller))
        start_page.pack()

        self.instruction = tk.Label(self, text="Place item inside box with ingredients list facing camera", font=('helvetica', 15))
        self.instruction.pack()

        self.promptLabel = tk.Label(self, image=self.img)
        self.promptLabel.pack()

    # navigate back to the homepage and clear the existing alerts
    def backToHomePage(self, controller):
        for i in self.itemList:
            if i != None:
                renderingUtil.refresh(i)
        for j in self.ingredientsList:
            if j != None:
                renderingUtil.refresh(j)
        renderingUtil.refresh(self.subcanvas)
        renderingUtil.refresh(self.alert)
        controller.show_frame(LandingPage)

    # print out the intersection between the ingredients received from google API and user's personal list
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

    # get the text from google OCR API and match it against users' lists
    def CheckIngredientsOCR(self, username):
        if self.noImg():
            return
        responseOCR = googleVision.requestOCR(objectImg)
        userList = database.Get_Personal_List(username)
        matchingArr = googleVision.getMatchingArr(responseOCR, userList)
        self.printIntersection("ingredients matching your personal list", matchingArr)

    # print out the ingredients of the corresponding custom item
    def printIngredients(self, subcanvas, itemIngredients, i):
        self.ingredientsList[i] = tk.Label(subcanvas, text=itemIngredients, borderwidth=2, relief="solid", height=2,
                                           font=('helvetica', 15))
        self.ingredientsList[i].grid(row=i, column=1)

    # get the tags array from google Recognition API and match it against the store custom items
    def CheckIngredientsRecognition(self, username):
        if self.noImg():
            return
        # get the text from OCR
        tags_array = googleVision.requestRecognition(objectImg)
        ingredients_array = database.Get_Custom_Ingredients(tags_array)

        self.subcanvas = tk.Canvas(app.canvas, height=100000000)
        self.subcanvas.pack(padx=(50, 50), pady=(550, 0))

        # display all the custom items relevant to the item
        max = 0
        for i in range(0, len(tags_array)):  # Rows
            if ingredients_array[i] != '0':
                ahoy = partial(self.printIngredients, self.subcanvas, ingredients_array[i], i)
                self.itemList[i] = tk.Button(self.subcanvas, text=tags_array[i], borderwidth=2, relief="solid", height = 2, font=('helvetica', 15),
                                            command=ahoy)
                self.itemList[i].grid(row=i, column=0, padx=10, sticky="W")
                if self.itemList[i].winfo_width() > max:
                    max = self.itemList[i].winfo_width()
                    
        userList = database.Get_Personal_List(username)
        # get the matching array
        matchingArr = googleVision.getMatchingArr(ingredients_array, userList)
        self.printIntersection("ingredients matching your personal list", matchingArr)

    # check out all the general harmful substances for store regular items
    def CheckHarmfulOCR(self):
        if self.noImg():
            return
        responseOCR = googleVision.requestOCR(objectImg)
        harmfulList = database.Get_Harmful_List()
        matchingArr = googleVision.getMatchingArr(responseOCR, harmfulList)
        self.printIntersection("generally harmful ingredients", matchingArr)

    # check out all the general harmful substances for store custom items
    def CheckHarmfulRecognition(self):
        if self.noImg():
            return
        responseRec = googleVision.requestRecognition(objectImg)
        responseRec = database.Get_Custom_Ingredients(responseRec)
        harmfulList = database.Get_Harmful_List()
        matchingArr = googleVision.getMatchingArr(responseRec, harmfulList)
        self.printIntersection("generally harmful ingredients", matchingArr)

    # accept incoming cropped image
    def MakeAcceptNextImage(self):
        global acceptNextImage
        acceptNextImage = True
        actualPoll()

    # alert users that no items detected
    def noImg(self):
        if objectImg is None:
            self.alert = tk.Label(self,
                                  text="No object detected, or image has not loaded yet. \n PLease wait for image of object to show up before attempting scan",
                                  font=('helvetica', 15))
            self.alert.pack()
            return True
        return False

# class RegularItems is the page in charge of scanning store Regular Items
class RegularItems(tk.Frame, CommonDisplay):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        CommonDisplay.__init__(self, message="Scan regular items here", scanFunction=self.CheckIngredientsOCR,
                               parent=parent, controller=controller)

# class RegularItems is the page in charge of scanning store Custom Items
class CustomItems(tk.Frame, CommonDisplay):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        CommonDisplay.__init__(self, message="Scan store custom items here",
                               scanFunction=self.CheckIngredientsRecognition, parent=parent, controller=controller)

# this class provides an exit button for the app
class MainMenu:
    def __init__(self, master):
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

app = App()

# this function will check whether the image has been generated and cropped
# it will display the newly processed image to the user
def loadProcessedImage(frame):
    # tell users to make google vision call or place an item based on the satus of the image
    global app
    renderingUtil.refresh(app.frames[frame].instruction)
    try:
        tryOpen = Image.open(workingDir + objectImg)
        app.frames[frame].instruction = tk.Label(app.frames[frame], text="Your item is ready to be scanned", font=('helvetica', 15))
    except OSError:
        print('cannot open')
        app.frames[frame].instruction = tk.Label(app.frames[frame], text="Please place an item in front of the camera", font=('helvetica', 15))
    app.frames[frame].instruction.pack()

    # update the image when a new image is generated and cropped
    renderingUtil.refresh(app.frames[frame].promptLabel)
    readImg = renderingUtil.resizeImage(objectImg)
    app.frames[frame].img = ImageTk.PhotoImage(readImg)
    app.frames[frame].promptLabel = tk.Label(app.frames[frame], image=app.frames[frame].img)
    app.frames[frame].promptLabel.pack()

# this function calls actualPoll() every 1 second
def pollPicture():
    actualPoll()
    app.after(1000, pollPicture)

# check if an image has been processed
# call loadProcessedImage() if an image is available
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

# main function called to instantiate the app main loop
# it also runs another process besides the mainlopp of the app
# this other process is the communication protocol between DE1-SoC and the Raspberry Pi
app.after(3000, pollPicture)
if __name__ == "__main__":
    producer = mp.Process(target=camera.run, args=(imageQueue, ackQueue))
    producer.start()
    ackQueue.put(True)
    app.mainloop()

app.mainloop()