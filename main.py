from tkinter import Button,Canvas,Entry,IntVar,Label,OptionMenu,StringVar,Tk
from pickle import dump,load
from os import path
from datetime import datetime
from time import sleep
from plyer import notification
from random import shuffle,choice
from playsound import playsound


def age_water_chart(gender:str,age:int) -> int:
    '''It' a function which takes gender and age as argument and give you the target to drink water in ml if target is
    not specified'''
    
    
    # This block of code is a function called `age_water_chart` that calculates the target amount of
    # water to drink based on the gender and age of the person.
    if gender in ["male","other"]:
        if age>=1 and age<=3:
            return 1000
        elif age>=4 and age<=8:
            return 1200
        elif age>=9 and age<=13:
            return 1600
        elif age>=14 and age<=18:
            return 1900
        elif age>=19:
            return 2600
    
    elif gender=="female":
        if age>=1 and age<=3:
            return 1000
        elif age>=4 and age<=8:
            return 1200
        elif age>=9 and age<=13:
            return 1400
        elif age>=14 and age<=18:
            return 1600
        elif age>=19:
            return 2100


def track_water_intake(cache_mem:dict,drawing:Canvas,show_percentage:int,target_achieve_now:int,drank_ml:int) -> None:
    '''It's the function which tracks the how much water you have dranked'''
    
    # This block of code is responsible for updating and displaying the progress of water intake in
    # the GUI interface. Here's a breakdown of what each step does:
    
    
    # This block of code is responsible for updating the amount of water that has been drank by the
    # user. Here's a breakdown of what each step does:
    drank = drank_ml.get()
    drank = int(drank.split()[0])
    
    temp_drank_ml = cache_mem["track"]
    temp_drank_ml += drank
    cache_mem["track"] = temp_drank_ml
    del temp_drank_ml
    
    
    # This block of code is calculating the percentage of water drank by the user and updating the GUI
    # interface to display this information. Here's a breakdown of what each step does:
    dranked_ml = cache_mem["track"]
    total_target_ml = cache_mem["target"]
    cache_mem['percentage'] = int((dranked_ml/total_target_ml)*100)
    
    del dranked_ml,total_target_ml
    
    show_percentage.config(text=f"Percentage dranked: {cache_mem['percentage']}%")
    target_achieve_now.config(text=f"Water Dranked: {cache_mem['track']} ml")
    
    
    # This block of code is responsible for updating the visual representation of the water intake
    # progress in the GUI interface. Here's a breakdown of what each step does:
    temp = cache_mem['glass_fill_cor']
    temp[3] = int((205)-((205)*(cache_mem['percentage']/100)))
    
    cache_mem['glass_fill_cor'] = temp
    
    drawing.create_rectangle(0,0,100,205,fill = "#005493")
    drawing.create_rectangle(*temp,fill = "#FFFAFA")
    
    del temp
    
    
    # This block of code is responsible for managing the date information in the program. Here's a
    # breakdown of what it does:
    # The code snippet you provided is performing the following actions:
    current_date = str(datetime.now().date()).split("-")
    current_date = {"day":int(current_date[-1]),"month":int(current_date[-2]),
                    "year":int(current_date[-3])}
    
    if current_date==cache_mem['date']:
        with open("info.dat","wb") as f:
            dump(cache_mem,f)
    
    
    # This block of code is part of the `main_exe` function and is executed when the current date does
    # not match the date stored in the cache memory. Here's what each line is doing:
    else:
        cache_mem['date'] = current_date
        cache_mem["percentage"] = 0
        cache_mem['glass_fill_cor'] = [0,0,100,205]


def gui(cache_mem:dict) -> None:
    '''Gui where you user will interact and tell how much water he had dranked.'''
    water_ml = ["100 ml","250 ml","500 ml","750 ml","1000 ml","1500 ml"]
    
    # This block of code is creating a graphical user interface (GUI) window using the Tkinter library
    # in Python. Here's a breakdown of what each part of the code is doing:
    
    
    # This block of code is creating a graphical user interface (GUI) window using the Tkinter library
    # in Python. Here's a breakdown of what each part of the code is doing:
    root = Tk()
    
    root.configure(bg="#282C35")
    root.geometry("500x500")
    
    Label(root,text=f"Target to drink water in a day: {cache_mem['target']} ml",font="Roboto 12 bold",
          bg="#282C35",fg="#F5F5F5").place(x=0,y=1.5)
    
    target_achieve_now = Label(root,text=f"Water Dranked: {cache_mem['track']} ml",font="Roboto 12 bold",
                               bg="#282C35",fg="#F5F5F5")
    target_achieve_now.place(x=0,y=32) 
    
    
    # The code snippet you provided is part of a graphical user interface (GUI) created using the
    # Tkinter library in Python. Here's a breakdown of what each part of the code is doing:
    show_percentage = Label(root,text=f"Percentage dranked: {cache_mem['percentage']}%",
                            font="Roboto 12 bold",bg="#282C35",fg="#F5F5F5")
    show_percentage.place(x=0,y=62)
    
    
    drank_ml = StringVar()
    drank_ml.set(water_ml[0])
    
    OptionMenu(root,drank_ml,*water_ml).place(x=10,y=92)
    
    drawing = Canvas(root,width=97,height=200,bg="#005493")
    drawing.place(x=100,y=132)
    
    
    # The code snippet you provided is part of a graphical user interface (GUI) created using the
    # Tkinter library in Python. Here's a breakdown of what each part of the code is doing:
    rect_cor = cache_mem["glass_fill_cor"]
    drawing.create_rectangle(*rect_cor,fill="#FFFAFA")
    
    Button(root,text="DRANKED!!",font="Roboto 14 bold",bg="#4CAF50",fg="#F1F1F1",
           command=lambda :track_water_intake(cache_mem,drawing,show_percentage,target_achieve_now,drank_ml)).place(x=5,y=365)
    root.mainloop()


def first_inte():
    """
    This Python script creates a GUI for users to enter their age, gender, target water intake, and
    time interval for notifications, saving the information to a file upon submission.
    """
    gender_list = ["male","female","other"]
    
    def info_entry():
        # The below code snippet is a Python script that seems to be a part of a GUI application using
        # tkinter library. Here is a brief explanation of what the code is doing:
        import tkinter.messagebox as msgb
        
        try:
            
            # The below Python code snippet is performing the following actions:
            if age.get()>0:
                if gender.get() in gender_list:
                    target = target_ml.get() if target_ml.get()>0 else age_water_chart(gender=gender.get()
                                                                                       ,age=age.get())
                    time = time_interval.get() if time_interval.get()>0 else 1
                    
                    current_date = str(datetime.now().date()).split("-")
                    current_date = {"day":int(current_date[-1]),"month":int(current_date[-2]),
                                    "year":int(current_date[-3])}
                    
                    cache = {"age":age.get(),"gender":gender.get(),"target":target,
                             "time_interval":time,"track":0,"glass_fill_cor":[0,0,100,205],
                             "percentage":0,"date":current_date}
                    
                    with open("info.dat","wb") as f:
                        dump(cache,f)
                        del cache
                        root.destroy()
                else:
                    msgb.showerror(title="Enter Gender",message="Please Enter Your Gender!")
            else:
                msgb.showerror(title="Enter Age",message="Please Enter Your Age!")
        
        except: 
            msgb.showerror(title="Enter Age",message="Please Enter Your Age!")
            
    
    
    # The below code is creating a GUI (Graphical User Interface) using the Tkinter library in Python.
    # It creates a window with specific dimensions and background color. It defines variables for age,
    # gender, time interval, and target ml. It provides input fields for the user to enter their age,
    # gender, time interval, and target ml. It also includes a message indicating that certain
    # information is compulsory. Finally, it includes a submit button that triggers a function called
    # `info_entry` when clicked. The GUI will continue running until the user closes the window.
    root = Tk()
    root.geometry("500x500")
    root.configure(bg="#282C35")
    root.protocol("WM_DELETE_WINDOW",exit)
    
    target_ml = IntVar()
    time_interval = IntVar()
    age = IntVar()
    gender = StringVar()
    gender.set("choose gender")
    
    Label(root,text="Enter your Age *: ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=1)
    Entry(root,textvariable=age,width=30).place(x=180,y=3)
    
    Label(root,text="Your Gender *: ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=30)
    OptionMenu(root,gender,*gender_list).place(x=180,y=32)
    
    Label(root,text="Enter The time interval for notificaton(in Hrs): ",font="Helvetica 14 bold",
          bg="#282C35",fg="#F1F1F1").place(x=1,y=60)
    Entry(root,textvariable=time_interval,width=10).place(x=430,y=63)
    
    Label(root,text="Enter Your Target in ml: ",font="Helvetica 14 bold",bg="#282C35",fg="#F1F1F1").place(x=1,y=90)
    Entry(root,textvariable=target_ml,width=10).place(x=230,y=93)
    
    Label(root,text="'*': It means it is compulsory to give information!!",font="Roboto 16 bold",
          fg="#FD0709",bg="#282C35").place(x=1,y=123)
    
    Button(root,text="submit",font="Aerial 13 bold",bg="#4CAF50", fg="#FFFFFF",command=info_entry).place(x=1,y=163)
    root.mainloop()


def main_exe() -> None:
    '''It is the fuction where main execution starts'''
    current_date = str(datetime.now().date()).split("-")
    current_date = {"day":int(current_date[-1]),"month":int(current_date[-2]),
                    "year":int(current_date[-3])}
    
    condition = True
    
    # to get facts for notification
    with open("facts.dat","rb") as f:
        data = load(f)
        title_list = list(data)
    
    
    # making cache
    cache_mem = {}
    if path.exists("info.dat"):
        with open("info.dat","rb+") as f:
            cache_mem = load(f)
            if cache_mem!=current_date:
                cache_mem["date"] = current_date
                cache_mem["glass_fill_cor"] = [0,0,100,205]
                cache_mem['track'] = 0
            
            elif cache_mem['target']<=cache_mem['track']:  
                condition = False
            
            f.seek(0)
            dump(cache_mem,f)
    
    # This Python code snippet is implementing a while loop that runs as long as a certain condition
    # is met. Within the loop, it checks if the "date" in the cache memory is equal to the current
    # date. If they match, it shuffles a list of titles and selects one randomly.
    while condition:
        
        # This Python code snippet is performing the following actions:
        if cache_mem["date"] == current_date:
            shuffle(title_list)
            title = choice(title_list)
            
            
            # The above Python code snippet is checking if the variable `cache_mem` is truthy. If it
            # is, it sends a notification with a title and message, plays a sound using the
            # `playsound` library, and then displays a GUI using the `gui` function. If an exception
            # occurs during the sound playing, it falls back to displaying the GUI. If `cache_mem` is
            # not truthy, it calls the `first_inte` function, loads data from a file named "info.dat"
            # into `cache_mem`, and then displays the GUI.
            if cache_mem:
                notification.notify(title=title,message=data[title],app_name='water drink',app_icon='water_icon.ico',timeout=5)
                try:
                    playsound("saahil.mp3")
                    sleep(1)
                except:
                    gui(cache_mem)
                else:
                    gui(cache_mem)
            else:
                first_inte()
                with open("info.dat","rb") as f:
                    cache_mem = load(f)
                gui(cache_mem)
            
            
            # The code snippet provided is written in Python and it seems to be part of a conditional
            # statement.
            if cache_mem['target']<=cache_mem['track']: 
                condition = False
                break
            sleep(cache_mem["time_interval"]*60*60)
        # else:
            
        #     # The above Python code snippet is updating a dictionary `cache_mem` with key-value pairs.
        #     # It sets the key "date" to the value `current_date`, the key "glass_fill_cor" to the list
        #     # `[0, 0, 100, 205]`, and the key "track" to the integer 0.
        #     print("I am In else block")
        #     cache_mem["date"] = current_date
        #     cache_mem["glass_fill_cor"] = [0,0,100,205]
        #     cache_mem['track'] = 0
            
        #     with open("info.dat","wb+") as file:
        #         dump(cache_mem,file)
        #         cache_mem = load(cache_mem)
            
        #     print(cache_mem)
        #     gui(cache_mem=cache_mem)
    
    else:
        gui(cache_mem)


if __name__=="__main__":
    main_exe()