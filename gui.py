import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

window = tk.Tk()

window.title("USCIS Case Status Crawler")


Label(window, text="Enter Case Number: ").grid(row=1, column=0, sticky=W)
text_entry = Entry(window,width=20).grid(row=1, column=1, sticky=W)
Button(window, text="SUBMIT",width=6).grid(row=2, column=1, sticky=W)
window.mainloop()