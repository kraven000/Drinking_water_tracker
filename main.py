from tkinter import Button,Canvas,Entry,IntVar,Label,OptionMenu,StringVar,Tk
from pickle import dump,load
from memory_profiler import profile,memory_usage
from os import path


cache = {}
if path.exists("info.bin"):
    with open("info.bin","rb") as f:
        cache = load(f)


def age_water_chart(gender,age):
    
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


def track_water_intake():
        '''Incomplete '''
        global cache
        drank = drank_ml.get()
        drank = int(drank.split()[0])
        print(drank)
        
        temp_drank_ml = cache["track"]
        temp_drank_ml += drank
        cache["track"] = temp_drank_ml
        del temp_drank_ml
            
        dranked_ml = cache["track"]
        total_target_ml = cache["target"]
        cache['percentage'] = int((dranked_ml/total_target_ml)*100)
            
        print(f"{cache['percentage']} %") 
        show_percentage.config(text=f"Percentage dranked: {cache['percentage']}%")
            
        temp = cache['glass_fill_cor']
        temp[3] = int((205)-((205)*(cache['percentage']/100)))
            
        cache['glass_fill_cor'] = temp
            
        drawing.create_rectangle(0,0,100,205,fill = "#005493")
        drawing.create_rectangle(*temp,fill = "#FFFAFA")
        
        with open("info.bin","wb") as f:
            dump(cache,f)
            
            # time.sleep(1)
            # root.destroy()


def gui():
    global drawing,drank_ml,root,show_percentage,cache
    print(cache)
    water_ml = ["100 ml","250 ml","500 ml","750 ml","1000 ml","1500 ml"]
    
    root = Tk()

    root.configure(bg="#151515")
    root.geometry("500x500")

    drank_ml = StringVar()
    drank_ml.set(water_ml[0])
    
    OptionMenu(root,drank_ml,*water_ml).place(x=10,y=1)

    drawing = Canvas(root,width=97,height=200,bg="#005493")
    drawing.place(x=100,y=50)


    rect_cor = cache["glass_fill_cor"]
    drawing.create_rectangle(*rect_cor,fill="#FFFAFA")
    
    show_percentage = Label(root,text=f"Percentage dranked: {cache['percentage']}%",font="Roboto 12 bold",bg="#282C35",fg="#f5f5f5")
    show_percentage.place(x=160,y=1)
    
    Button(root,text="DRANKED!!",font="Roboto 14 bold",bg="#4CAF50",fg="#F1F1F1",command=track_water_intake).place(x=5,y=305)
    root.mainloop()


def first_inte():
    global age,gender,cache
    gender_list = {"male","female","other"}
    
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
                    
                    with open("info.bin","wb") as f:
                        dump(cache,f)
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
    
    Button(root,text="submit",font="Aerial 13 bold",bg="#4CAF50", fg="#FFFFFF",command=info_entry).place(x=1,y=163)
    root.mainloop()


@profile
def main_exe():
    global cache
    while True:
        if cache:
            gui()
        else:
            first_inte()
            with open("info.bin","rb") as f:
                cache = load(f)
            gui()
        break

if __name__=="__main__":
    main_exe()