import tkinter as tk
import requests
from PIL import ImageTk, Image
import os

#current working directory
workingDir = os.path.dirname(os.path.abspath(__file__))

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen', True)

        canvas = tk.Canvas(self, bg = "#263D42")
        canvas.pack(fill = tk.BOTH, expand = True)

        #Set up Menu
        MainMenu(self)
        #Set up Frames
        container = tk.Frame(canvas)
        container.place(relwidth=0.75, relheight=0.75, relx = 0.1, rely = 0.1)
        #container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (LandingPage, RegularItems, CustomItems):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0,sticky="nsew")

        self.show_frame(LandingPage)
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
    def show_plist(self, context):
        URL = "http://52.138.39.36:3000/plist"
        userName = 'customer1'
        PARAMS = {'username': 'customer1'}
        response = requests.post(url = URL, json = PARAMS)
        resJson = response.json()
        userList = []

        for element in resJson['message']:
            userList.append(element['p'])
        str1 = ""
        for element in userList:
            str1 += element
            str1 += " "
        user_list = tk.Label(self.frames[context], text = 'Here is your list: ' + str1)
        user_list.pack(padx=10, pady=10)

class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Welcome to Ingredients Decoder")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)
        regular_page = tk.Button(self, text="Regular Items", command=lambda:controller.show_frame(RegularItems))
        regular_page.pack()
        custom_page = tk.Button(self, text="Custom Items", command=lambda:controller.show_frame(CustomItems))
        custom_page.pack()
        user_list = tk.Button(self, text="View personalized list", command=lambda:controller.show_plist(LandingPage))
        user_list.pack()

class RegularItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Scan regular items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)

        scan_items = tk.Button(self, text = "Check Ingredients =>")
        scan_items.pack()
        start_page = tk.Button(self, text = "Back to Home Page", command=lambda:controller.show_frame(LandingPage))
        start_page.pack()
        img = ImageTk.PhotoImage(Image.open(workingDir + "/images/cat.gif"))
        print(workingDir + "/images/cat.gif")
        panel = tk.Label(self, image = img)
        panel.pack()

class CustomItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Scan store custom items here")
        label.config(font=('helvetica', 25))
        label.pack(padx=10, pady=10)
        scan_items = tk.Button(self, text = "Check Ingredients")
        scan_items.pack()
        start_page = tk.Button(self, text = "Back to Home Page", command=lambda:controller.show_frame(LandingPage))
        start_page.pack()

class MainMenu:
    def __init__(self, master):
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

app = App()
app.mainloop()