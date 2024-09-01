from tkinter import Button,Canvas,Entry,IntVar,Label,OptionMenu,StringVar,Tk
from pickle import dump,load
from memory_profiler import profile
from os import path
from time import sleep
from plyer import notification
from random import shuffle,choice
from playsound import playsound


def age_water_chart(gender:str,age:int) -> int:
    '''It' a function which takes gender and age as argument and give you the target to drink water in ml if target is
    not specified'''
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
    drank = drank_ml.get()
    drank = int(drank.split()[0])
    
    temp_drank_ml = cache_mem["track"]
    temp_drank_ml += drank
    cache_mem["track"] = temp_drank_ml
    del temp_drank_ml
    
    dranked_ml = cache_mem["track"]
    total_target_ml = cache_mem["target"]
    cache_mem['percentage'] = int((dranked_ml/total_target_ml)*100)
    
    del dranked_ml,total_target_ml
    
    show_percentage.config(text=f"Percentage dranked: {cache_mem['percentage']}%")
    target_achieve_now.config(text=f"Water Dranked: {cache_mem['track']} ml")
    
    temp = cache_mem['glass_fill_cor']
    temp[3] = int((205)-((205)*(cache_mem['percentage']/100)))
    
    cache_mem['glass_fill_cor'] = temp
    
    drawing.create_rectangle(0,0,100,205,fill = "#005493")
    drawing.create_rectangle(*temp,fill = "#FFFAFA")
    
    del temp
    with open("info.dat","wb") as f:
        dump(cache_mem,f)


def gui(cache_mem:dict) -> None:
    '''Gui where you user will interact and tell how much water he had dranked.'''
    water_ml = ["100 ml","250 ml","500 ml","750 ml","1000 ml","1500 ml"]
    
    root = Tk()
    
    root.configure(bg="#282C35")
    root.geometry("500x500")
    
    Label(root,text=f"Target to drink water in a day: {cache_mem['target']} ml",font="Roboto 12 bold",
          bg="#282C35",fg="#F5F5F5").place(x=0,y=1.5)
    
    target_achieve_now = Label(root,text=f"Water Dranked: {cache_mem['track']} ml",font="Roboto 12 bold",
                               bg="#282C35",fg="#F5F5F5")
    target_achieve_now.place(x=0,y=32) 
    
    show_percentage = Label(root,text=f"Percentage dranked: {cache_mem['percentage']}%",
                            font="Roboto 12 bold",bg="#282C35",fg="#F5F5F5")
    show_percentage.place(x=0,y=62)
    
    
    drank_ml = StringVar()
    drank_ml.set(water_ml[0])
    
    OptionMenu(root,drank_ml,*water_ml).place(x=10,y=92)
    
    drawing = Canvas(root,width=97,height=200,bg="#005493")
    drawing.place(x=100,y=132)
    
    rect_cor = cache_mem["glass_fill_cor"]
    drawing.create_rectangle(*rect_cor,fill="#FFFAFA")
    
    Button(root,text="DRANKED!!",font="Roboto 14 bold",bg="#4CAF50",fg="#F1F1F1",
           command=lambda :track_water_intake(cache_mem,drawing,show_percentage,target_achieve_now,drank_ml)).place(x=5,y=365)
    root.mainloop()


def first_inte():
    gender_list = ["male","female","other"]
    
    def info_entry():
        import tkinter.messagebox as msgb
        
        try:
            if age.get()>0:
                if gender.get() in gender_list:
                    target = target_ml.get() if target_ml.get()>0 else age_water_chart(gender=gender.get()
                                                                                       ,age=age.get())
                    time = time_interval.get() if time_interval.get()>0 else 1
                    
                    cache = {"age":age.get(),"gender":gender.get(),"target":target,
                             "time interval":time,"track":0,"glass_fill_cor":[0,0,100,205],
                             "percentage":0}
                    
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


@profile(stream=open("memory.log","a"))
def main_exe() -> None:
    '''It is the fuction where main execution starts'''
    condition = True
    
    # to get facts for notification
    with open("facts.dat","rb") as f:
        data = load(f)
        title_list = list(data)
        
    # making cache
    cache_mem = {}
    if path.exists("info.dat"):
        with open("info.dat","rb") as f:
            cache_mem = load(f)
            if cache_mem['target']<=cache_mem['track']:  
                condition = False
    
    while condition:
        shuffle(title_list)
        title = choice(title_list)
        
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
        
        if cache_mem['target']<=cache_mem['track']: 
            condition = False
            break
        sleep(30)
    else:
        gui(cache_mem)


if __name__=="__main__":
    main_exe()