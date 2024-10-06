from tkinter import Button, Canvas, Entry, IntVar, Label, OptionMenu, StringVar, Tk
from pickle import dump, load
from os import path
from datetime import datetime
from time import sleep
from plyer import notification
from random import shuffle, choice
from playsound import playsound

# Constants for default values
CANVAS_WIDTH, CANVAS_HEIGHT = 97, 200
WATER_INTAKE_FACTS_FILE = "facts.dat"
USER_DATA_FILE = "info.dat"
NOTIFICATION_ICON = 'water_icon.ico'
SOUND_FILE = 'notification_sound.mp3'

class WaterTracker:
    def __init__(self):
        self.cache_mem = self.load_cache()

    def age_water_chart(self, gender: str, age: int) -> int:
        '''Calculates the target water intake based on gender and age.'''
        if gender in ["male", "other"]:
            if 1 <= age <= 3:
                return 1000
            elif 4 <= age <= 8:
                return 1200
            elif 9 <= age <= 13:
                return 1600
            elif 14 <= age <= 18:
                return 1900
            elif age >= 19:
                return 2600
        elif gender == "female":
            if 1 <= age <= 3:
                return 1000
            elif 4 <= age <= 8:
                return 1200
            elif 9 <= age <= 13:
                return 1400
            elif 14 <= age <= 18:
                return 1600
            elif age >= 19:
                return 2100

    def track_water_intake(self, drawing: Canvas, show_percentage: Label, target_achieve_now: Label, drank_ml: StringVar):
        '''Tracks the amount of water drank and updates the GUI.'''
        try:
            drank = int(drank_ml.get().split()[0])
        except ValueError:
            return  # Invalid input, ignore
        
        # Update the cache with new water intake
        self.cache_mem["track"] += drank
        dranked_ml = self.cache_mem["track"]
        total_target_ml = self.cache_mem["target"]
        self.cache_mem['percentage'] = int((dranked_ml / total_target_ml) * 100)

        # Update UI labels
        show_percentage.config(text=f"Percentage drank: {self.cache_mem['percentage']}%")
        target_achieve_now.config(text=f"Water Drank: {self.cache_mem['track']} ml")

        # Update the canvas
        glass_fill_cor = self.cache_mem['glass_fill_cor']
        glass_fill_cor[3] = int(205 - (205 * (self.cache_mem['percentage'] / 100)))
        drawing.create_rectangle(0, 0, 100, 205, fill="#005493")
        drawing.create_rectangle(*glass_fill_cor, fill="#FFFAFA")

        # Save data to file
        self.save_cache()

    def load_cache(self):
        '''Loads user data from cache or initializes a new cache.'''
        if path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "rb") as f:
                cache_mem = load(f)
        else:
            cache_mem = self.initialize_cache()
        return cache_mem

    def initialize_cache(self):
        '''Initializes a new cache structure.'''
        current_date = datetime.now().date()
        return {
            "age": 0,
            "gender": "male",
            "target": 2000,
            "time_interval": 1,
            "track": 0,
            "glass_fill_cor": [0, 0, 100, 205],
            "percentage": 0,
            "date": current_date
        }

    def save_cache(self):
        '''Saves the current cache to the file.'''
        with open(USER_DATA_FILE, "wb") as f:
            dump(self.cache_mem, f)

    def gui(self):
        '''Creates the main GUI where users can input the amount of water drank.'''
        water_ml_options = ["100 ml", "250 ml", "500 ml", "750 ml", "1000 ml", "1500 ml"]

        # Create root window
        root = Tk()
        root.configure(bg="#282C35")
        root.geometry("500x500")

        # Add labels for water target and progress
        Label(root, text=f"Target to drink water in a day: {self.cache_mem['target']} ml", font="Roboto 12 bold", bg="#282C35", fg="#F5F5F5").place(x=0, y=1.5)
        target_achieve_now = Label(root, text=f"Water Drank: {self.cache_mem['track']} ml", font="Roboto 12 bold", bg="#282C35", fg="#F5F5F5")
        target_achieve_now.place(x=0, y=32)

        # Show percentage of water intake
        show_percentage = Label(root, text=f"Percentage drank: {self.cache_mem['percentage']}%", font="Roboto 12 bold", bg="#282C35", fg="#F5F5F5")
        show_percentage.place(x=0, y=62)

        # Water amount option menu
        drank_ml = StringVar()
        drank_ml.set(water_ml_options[0])
        OptionMenu(root, drank_ml, *water_ml_options).place(x=10, y=92)

        # Canvas for visual representation of water intake
        drawing = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#005493")
        drawing.place(x=100, y=132)
        rect_cor = self.cache_mem["glass_fill_cor"]
        drawing.create_rectangle(*rect_cor, fill="#FFFAFA")

        # "Drank" button to log water intake
        Button(root, text="DRANK!", font="Roboto 14 bold", bg="#4CAF50", fg="#F1F1F1", 
               command=lambda: self.track_water_intake(drawing, show_percentage, target_achieve_now, drank_ml)).place(x=5, y=365)
        
        root.mainloop()

    def first_interaction(self):
        '''First interaction to collect age, gender, and target intake.'''
        gender_list = ["male", "female", "other"]

        def info_entry():
            '''Handles data input and cache initialization.'''
            import tkinter.messagebox as msgb
            try:
                if age.get() > 0 and gender.get() in gender_list:
                    target = target_ml.get() if target_ml.get() > 0 else self.age_water_chart(gender=gender.get(), age=age.get())
                    time_interval = time_interval_var.get() if time_interval_var.get() > 0 else 1
                    self.cache_mem = {
                        "age": age.get(),
                        "gender": gender.get(),
                        "target": target,
                        "time_interval": time_interval,
                        "track": 0,
                        "glass_fill_cor": [0, 0, 100, 205],
                        "percentage": 0,
                        "date": datetime.now().date()
                    }
                    self.save_cache()
                    root.destroy()
                    self.main_exe()
                else:
                    msgb.showerror(title="Error", message="Please enter valid age and gender!")
            except Exception as e:
                msgb.showerror(title="Error", message=f"An error occurred: {e}")

        # GUI for first interaction
        root = Tk()
        root.geometry("500x500")
        root.configure(bg="#282C35")
        root.protocol("WM_DELETE_WINDOW", exit)

        target_ml = IntVar()
        time_interval_var = IntVar()
        age = IntVar()
        gender = StringVar()
        gender.set("choose gender")

        # Input fields for age, gender, and target intake
        Label(root, text="Enter your Age *: ", font="Helvetica 14 bold", bg="#282C35", fg="#F1F1F1").place(x=1, y=1)
        Entry(root, textvariable=age, width=30).place(x=180, y=3)

        Label(root, text="Your Gender *: ", font="Helvetica 14 bold", bg="#282C35", fg="#F1F1F1").place(x=1, y=30)
        OptionMenu(root, gender, *gender_list).place(x=180, y=32)

        Label(root, text="Time interval for notification (in Hrs): ", font="Helvetica 14 bold", bg="#282C35", fg="#F1F1F1").place(x=1, y=60)
        Entry(root, textvariable=time_interval_var, width=10).place(x=360, y=64)

        Label(root, text="Enter Your Target in ml: ", font="Helvetica 14 bold", bg="#282C35", fg="#F1F1F1").place(x=1, y=90)
        Entry(root, textvariable=target_ml, width=10).place(x=230, y=93)

        Label(root, text="'*': It means it is compulsory to give information!!", font="Roboto 16 bold", fg="#FD0709", bg="#282C35").place(x=1, y=123)

        Button(root, text="Submit", font="Aerial 13 bold", bg="#4CAF50", fg="#FFFFFF", command=info_entry).place(x=1, y=163)
        root.mainloop()

    def main_exe(self):
        '''Main execution of the water tracking program.'''
        current_date = datetime.now().date()
        condition = True

        # Load facts for notifications
        if path.exists(WATER_INTAKE_FACTS_FILE):
            with open(WATER_INTAKE_FACTS_FILE, "rb") as f:
                facts_data = load(f)
                title_list = list(facts_data.keys())
        else:
            facts_data = {}
            title_list = []

        if path.exists(USER_DATA_FILE):
            self.cache_mem = self.load_cache()

            # Reset for a new day
            if self.cache_mem["date"] != current_date:
                self.cache_mem["date"] = current_date
                self.cache_mem["glass_fill_cor"] = [0, 0, 100, 205]
                self.cache_mem['track'] = 0
                self.save_cache()

            elif self.cache_mem['target'] <= self.cache_mem['track']:
                condition = False

            while condition:
                # Notification loop for reminders
                shuffle(title_list)
                title = choice(title_list) if title_list else "Stay Hydrated!"
                if self.cache_mem:
                    notification.notify(title=title, message=facts_data.get(title, ""), app_name='Water Tracker', 
                                        app_icon=NOTIFICATION_ICON, timeout=5)

                    try:
                        playsound(SOUND_FILE)
                    except:
                        pass

                    self.gui()
                else:
                    self.first_interaction()

                # Stop if target is reached
                if self.cache_mem['target'] <= self.cache_mem['track']:
                    condition = False
                    break

                sleep(self.cache_mem["time_interval"] * 60 * 60)
        else:
            self.first_interaction()


if __name__ == "__main__":
    tracker = WaterTracker()
    tracker.main_exe()
