from webbrowser import open as browseropen
import customtkinter as ct
from tkintermapview import TkinterMapView
# import gmaps
from customtkinter import *
from tkinter import messagebox
from firebase import firebase

# Phone Tracker - Android / Desktop App
# Phone coordinates saved in the Firebase DB via the android app designed by one of my Uni colleagues

# --------------------
location = None
longitude, latitude = None, None

# App theme
ct.set_appearance_mode("Dark")

basedir = os.path.curdir

root = ct.windows.CTk()

# ---------------

# App icon
try:
    root.iconbitmap(os.path.join(basedir, "phone.ico"))
except:
    print(".ico image not found")

root.title("Phone Tracker")
root.geometry('600x600')

# ------------------

try:

    # Fetching the coordinates from the Firebase DB
    # Firebase address marked out for privacy reasons
    firebase = firebase.FirebaseApplication("https://**********-default-rtdb.europe-west1.firebasedatabase.app/")
    location = firebase.get("/location", '').split(',')

except Exception:
    messagebox.showerror("Error", "Couldn't fetch firebase data! Tracking option disabled.")

# ---------------------

def track():

    # map_window = ct.windows.CTk()

    global longitude, latitude

    try:
        longitude = float(location[0])
        latitude = float(location[1])

        longitude_box.configure(placeholder_text=longitude)
        latitude_box.configure(placeholder_text=latitude)

        map_widget.forget()

        # Plotting
        map_widget.set_position(longitude, latitude, marker=True)
        map_widget.set_zoom(5)
        map_widget.grid(row=4, column=1, columnspan=3, pady=15)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")

        # "Open in browser" button enabled if the coordinates are valid
        open_browser_button.configure(state=NORMAL)

    except Exception:
        messagebox.showerror("Invalid Coordinates!", "Enter valid coordinates!")
        open_browser_button.configure(state=DISABLED)



def enter_coord():

    # [manually] "Enter coordinates" button

    global longitude, latitude

    map_widget.forget()

    try:
        longitude = float(longitude_box.get())
        latitude = float(latitude_box.get())

        map_widget.set_position(longitude, latitude, marker=True)
        map_widget.set_zoom(5)
        map_widget.grid(row=4, column=1, columnspan=3, pady=15)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")

        open_browser_button.configure(state=NORMAL)

    except Exception:
        messagebox.showerror("Invalid Coordinates!", "Enter valid coordinates!")
        open_browser_button.configure(state=DISABLED)


def open_maps():

    # Search coordinates via Google Maps

    global longitude, latitude

    try:
        browseropen(f"https://www.google.com/maps/place/{longitude}, {latitude}")
        open_browser_button.configure(state=DISABLED)

    except Exception:
        messagebox.showerror("Error", "Couldn't open browser")


def close():

    # Closing prompt

    messagebox.showinfo(title='Phone Tracker App', message='Made by Bilici Razvan\n©2023')
    root.destroy()


# Exit app via the close() function
root.protocol('WM_DELETE_WINDOW', close)

# ------------------------

# Buttons and labels

longitude_label = ct.CTkLabel(root, font=("Castellar", 20), text='Longitude')
longitude_label.grid(row=0, column=0, pady=30, ipadx=15)
longitude_box = ct.CTkEntry(root)
longitude_box.grid(row=0, column=1, pady=30)

latitude_label = ct.CTkLabel(root, font=("Castellar", 20), text='Latitude')
latitude_label.grid(row=1, column=0, pady=30)
latitude_box = ct.CTkEntry(root)
latitude_box.grid(row=1, column=1, pady=30)

track_button = ct.CTkButton(root, command=track, text="Track Device", border_width=2, border_color='Gray')
track_button.grid(row=2, column=1, padx=7, pady=7)

or_label = ct.CTkLabel(root, text="OR")
or_label.grid(row=2, column=2)

enter_button = ct.CTkButton(root, command=enter_coord, text="Enter Coordinates", border_width=2, border_color='Gray')
enter_button.grid(row=2, column=3, padx=7, pady=7)

open_browser_button = ct.CTkButton(root, command=open_maps, text="Open in browser", border_width=2,
                                   border_color='Gray', state=DISABLED)
open_browser_button.grid(row=3, column=1, padx=7, pady=7)

# Plotting the coordinates using the TK map widget
map_widget = TkinterMapView(root, height=400, width=400)

if location is None:
    track_button.configure(state=DISABLED)

root.mainloop()
