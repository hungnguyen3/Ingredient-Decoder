import tkinter as tk

#extend the Tk of tkinter
class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		#Setup Menu
		MainMenu(self)
		#Setup Frame
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (LandingPage, RegularItem, CustomItems):
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

		label = tk.Label(self, text="Please pick types of items to scan")
		label.pack(padx=10, pady=10)
		page_one = tk.Button(self, text="Regular Items", command=lambda:controller.show_frame(RegularItem))
		page_one.pack()
		page_two = tk.Button(self, text="Store Custom Items", command=lambda:controller.show_frame(CustomItems))
		page_two.pack()


class RegularItem(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Scan regular items here")
		label.pack(padx=10, pady=10)
        start_page = tk.Button(self, text="Back to Home Page", command=lambda:controller.show_frame(LandingPage))
        start_page.pack()
        page_two = tk.Button(self, text="Check Ingredients", command=lambda:controller.show_frame(CustomItems))
        page_two.pack()

class CustomItems(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Page Two")
		label.pack(padx=10, pady=10)
		start_page = tk.Button(self, text="Start Page", command=lambda:controller.show_frame(LandingPage))
		start_page.pack()
		page_one = tk.Button(self, text="Page One", command=lambda:controller.show_frame(RegularItem))
		page_one.pack()

class MainMenu:
	def __init__(self, master):
		menubar = tk.Menu(master)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		master.config(menu=menubar)


app = App()
app.mainloop()