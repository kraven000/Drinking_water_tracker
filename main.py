from tkinter import *

water_ml = ["100 ml","250 ml","500 ml","750 ml","100 ml","1500 ml"]

root = Tk()

root.geometry("500x500")
root.configure(bg="#151515")

string_var = StringVar()
string_var.set(water_ml[0])
OptionMenu(root,string_var,*water_ml).place(x=10,y=1)

drawing = Canvas(root,width=250,height=250)
drawing.place(x=100,y=50)


# a = [10,10,50,250,250,10,200,250,10,10,250,10,50,250,200,250]


drawing.create_line(10,10,50,250) #left line
drawing.create_line(250,10,200,250) #right line

drawing.create_line(10,10,250,10) #upper line

drawing.create_line(45,275,180,275) #upper line 

drawing.create_line(50,250,200,250) #lower line

# drawing.create_polygon(*a,fill="blue")

root.mainloop()
