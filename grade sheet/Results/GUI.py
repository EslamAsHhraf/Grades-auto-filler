import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from main import *


def upload_file():
        f_types = [('Jpg Files', '*.jpg')]   # type of files to select 
        filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
        col=1 # start from column 1
        row=9 # start from row 7
        l1_Bubble.config(text='Wait Results....')
        for f in filename:
            img=Image.open(f) # read the image file
            img=img.resize((200,200)) # new width & height
            img=ImageTk.PhotoImage(img)
            e1 =tk.Label(my_w)
            e1.grid(row=row,column=col)
            e1.image = img # keep a reference! by attaching it to a widget attribute
            e1['image']=img # Show Image
            
            flag=False
            if toggle_btn.config('relief')[-1] == 'raised':
                flag=True
            GradesSheet(path=f,OCR_flag=flag)
        
        l1_Bubble.config(text='Results Done ✅')

def toggle():
    if toggle_btn.config('relief')[-1] == 'raised':
        toggle_btn.config(relief="sunken",background='#e94235',text='Classifier')
    else:
        toggle_btn.config(relief="raised",background='#4285f4',text='OCR')

def GradesSheet_Window():
    global l1,toggle_btn,my_w,l1_Bubble
    my_w = tk.Toplevel()
    my_w.geometry("710x400")  # Size of the window
    my_w.title('Grades sheet')
    my_font1=('times', 20, 'bold')
    my_font2=('times', 12, 'bold')
    l1 = tk.Label(my_w,text='Upload your Sheet 😀',font=my_font1,background='white')
    l1.grid(row=1,column=10)
    b1 = tk.Button(my_w, text='Upload image',background='#e2d3e4',
    width=20,command = lambda:upload_file())
    b1.grid(row=2,column=10)
    toggle_btn = tk.Button(my_w,text="OCR", width=12, relief="raised" ,fg='white',background='#4285f4',command=lambda:toggle())
    toggle_btn.grid(row=4,column=10)
    my_w['bg']='#2a5289'
    l1_Bubble = tk.Label(my_w,text='Wait Results....',font=my_font2,background='white')
    l1_Bubble.grid(row=5,column=10)

    my_w.mainloop()

    

def upload_file_Button():
        f_types = [('Jpg Files', '*.jpg')]   # type of files to select 
        filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
        col=1 # start from column 1
        row=9 # start from row 7
        l1_Bubble.config(text='Wait Results....')
        for f in filename:
            img=Image.open(f) # read the image file
            img=img.resize((200,200)) # new width & height
            img=ImageTk.PhotoImage(img)
            e1 =tk.Label(my_w_Bubble)
            e1.grid(row=row,column=col)
            e1.image = img # keep a reference! by attaching it to a widget attribute
            e1['image']=img # Show Image

            Run_one_bubble_sheet(path=f)
        
        l1_Bubble.config(text='Results Done ✅')

def upload_ALL_file_Button():
        folder = tk.filedialog.askdirectory()
        print("cas",folder)
        run_all_bubble_sheets(path=folder+'/')
        



def Bubble_Window():
    try:
        global l1_Bubble,my_w_Bubble
        my_w_Bubble = tk.Toplevel()
        my_w_Bubble.geometry("710x400")  # Size of the window
        my_w_Bubble.title('Bubble sheet')
        my_font1=('times', 20, 'bold')
        my_font2=('times', 12, 'bold')
        l1_Bubble = tk.Label(my_w_Bubble,text='Upload your Sheet 😀',font=my_font1,background='white')
        l1_Bubble.grid(row=1,column=10)
        b1_Bubble = tk.Button(my_w_Bubble, text='Upload image',background='#e2d3e4',
        width=20,command = lambda:upload_file_Button())
        b1_Bubble.grid(row=2,column=10)
        my_w_Bubble['bg']='#2a5289'
        l2_Bubble = tk.Label(my_w_Bubble,text='Wait Results....',font=my_font2,background='white')
        l2_Bubble.grid(row=5,column=10)
        b2_Bubble = tk.Button(my_w_Bubble, text='run all bubble sheets',background='#e2d3e4',
        width=20,command = lambda:upload_ALL_file_Button())
        b2_Bubble.grid(row=3,column=10)
        my_w_Bubble.mainloop()
    except:
        print("error")


def main():
    main_window = tk.Tk()
    main_window.geometry("700x500")  # Size of the window
    main_window.title('Grades auto-filler')
    GradesSheet_button= tk.Button(main_window, text='GradesSheet Window',background='#e2d3e4',
    width=20,command = lambda:GradesSheet_Window())
    GradesSheet_button.grid(row=1,column=1)
    Bubble_button= tk.Button(main_window, text='Bubble Window',background='#e2d3e4',
    width=20,command = lambda:Bubble_Window())
    Bubble_button.grid(row=2,column=1)
    main_window['bg']='#2a5289'
    img = ImageTk.PhotoImage(Image.open("panel.jpg"))
    panel = Label(main_window, image=img)
    panel.grid(row=4,column=1,pady=7,padx=100)
    main_window.mainloop()

if __name__ == '__main__':
    main()