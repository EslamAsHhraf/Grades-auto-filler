import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from main import *
import sys
import time

my_w = tk.Tk()
my_w.geometry("710x400")  # Size of the window 
my_w.title('Grades sheet')
my_font1=('times', 20, 'bold')
l1 = tk.Label(my_w,text='Upload your Sheet 😀',width=35,font=my_font1)  
l1.grid(row=1,column=1,columnspan=4)
b1 = tk.Button(my_w, text='Upload image',
   width=20,command = lambda:upload_file())
b1.grid(row=2,column=1,columnspan=4)



def upload_file():
    f_types = [('Jpg Files', '*.jpg')]   # type of files to select 
    filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
    col=1 # start from column 1
    row=4 # start from row 3 
    for f in filename:
        img=Image.open(f) # read the image file
        img=img.resize((200,200)) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =tk.Label(my_w)
        e1.grid(row=row,column=col)
        e1.image = img # keep a reference! by attaching it to a widget attribute
        e1['image']=img # Show Image
        GradesSheet(path=f)
        l1 = tk.Label(my_w,text='Check Results✅',width=35,font=my_font1)
        
        l1.grid(row=5,column=8)
my_w.mainloop()  # Keep the window open