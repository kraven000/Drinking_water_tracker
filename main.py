from tkinter import *

water_ml = ["100 ml","250 ml","500 ml","750 ml","100 ml","1500 ml"]


def age_water_chart():
    gender = gender.get().lower()
    age = age.get()
    
    target_ml = None
    if gender=="male" or gender=="other":
        if age>=1 and age<=3:
            target_ml = 1000
        elif age>=4 and age<=8:
            target_ml = 1200
        elif age>=9 and age<=13:
            target_ml = 1600
        elif age>=14 and age<=18:
            target_ml = 1900
        elif age>=19:
            target_ml = 2600
    
    elif gender=="female":
        if age>=1 and age<=3:
            target_ml = 1000
        elif age>=4 and age<=8:
            target_ml = 1200
        elif age>=9 and age<=13:
            target_ml = 1400
        elif age>=14 and age<=18:
            target_ml = 1600
        elif age>=19:
            target_ml = 2100
    
    return target_ml


def gui():
    root = Tk()

    root.configure(bg="#151515")
    root.geometry("500x500")

    string_var = StringVar()
    string_var.set(water_ml[0])
    OptionMenu(root,string_var,*water_ml).place(x=10,y=1)

    drawing = Canvas(root,width=97,height=200,bg="#151515")
    drawing.place(x=100,y=50)


    rect_cor = [0,0,100,205]

    rect_cor1 = [0,0,100,184.5] 
    #variable with percentage of water drank specifically: rect_cor1[3] index is variable

    drawing.create_rectangle(*rect_cor,fill="#005493")
    drawing.create_rectangle(*rect_cor1,fill="#FFFAFA")

    root.mainloop()


def first_inte():
    global age,gender
    gender_list = ["male","female","other"]
    
    root = Tk()
    root.geometry("500x500")
    root.configure(bg="#282C35")
    
    target_ml = IntVar()
    time_interval = IntVar()
    age = IntVar()
    gender = StringVar()
    gender.set("choose gender")
    
    Label(root,text="Enter your Age *: ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=1)
    Entry(root,textvariable=age,width=30).place(x=180,y=3)
    
    Label(root,text="Your Gender *: ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=30)
    OptionMenu(root,gender,*gender_list).place(x=180,y=32)
    
    Label(root,text="Enter The time interval for notificaton(in Hrs): ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=60)
    Entry(root,textvariable=time_interval,width=10).place(x=430,y=63)
    
    Label(root,text="Enter Your Target in ml: ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=90)
    Entry(root,textvariable=target_ml,width=10).place(x=230,y=93)
    
    Label(root,text="'*': It means it is compulsory to give information!!",font="Roboto 16 bold",fg="#FD0709",bg="#282C35").place(x=1,y=123)
    
    Button(root,text="submit",font="Aerial 13 bold").place(x=1,y=163)
    root.mainloop()


first_inte()