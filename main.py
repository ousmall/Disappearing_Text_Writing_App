from time import time
import threading
from tkinter import *
import ttkbootstrap as ttk

# Define the time interval (in milliseconds) for checking user activity
CHECK_INTERVAL = 5000
WAITING_TIME = 5000
FADE_OUT_INTERVAL = 100
SAVE_FILE_PATH = "saved_text.txt"


# timestamp
last_activity_time = time()
disappear_start_time = None
fade_rectangle = None
remaining_time = CHECK_INTERVAL / 1000


# Function to check user activity
def check_activity(main_root):
    global last_activity_time
    global disappear_start_time
    current_time = time()

    if current_time - last_activity_time >= CHECK_INTERVAL / 1000:
        update_remaining_time()
        # Clear the text if the disappearing time has elapsed
        if disappear_start_time is not None and current_time - disappear_start_time >= WAITING_TIME / 1000:
            fade_out_text()
            disappear_start_time = None
        else:
            disappear_start_time = current_time
    main_root.after(CHECK_INTERVAL, check_activity, main_root)


# Function to count down
def update_remaining_time():
    global remaining_time

    if remaining_time >= 0:
        count_label.config(text=f"Remaining time: {int(remaining_time)} s")
        remaining_time -= 1
        root.after(1000, update_remaining_time)


# Function to handle user input
def handle_input(event):
    global last_activity_time
    last_activity_time = time()
    if event.keysym == "Return":
        text.insert(END, '\n')
        return "break"  # Stop further processing of this event
    return None  # Continue default event processing


# Function to save user typing content
def save_text():
    user_input = text.get(1.0, END)
    with open(SAVE_FILE_PATH, 'a') as f:
        f.write(user_input + '\n')


# Function to fade out the text
def fade_out_text():
    def change_color():
        nonlocal alpha
        if alpha > 0:
            alpha -= 0.1
            text.config(fg=f"#{int(255 * (1 - alpha)):02x}"
                           f"{int(255 * (1 - alpha)):02x}"
                           f"{int(255 * (1 - alpha)):02x}")
            text.after(FADE_OUT_INTERVAL, change_color)
        else:
            text.delete(1.0, END)

    alpha = 1.0
    change_color()


# ------------- Create the main Tkinter window ----------------
root = ttk.Window()
style = ttk.Style("pulse")
root.config(padx=50, pady=50)
root.title("The Most Dangerous Writing App")

# Create widgets
text_label = Label(text="Please start your writing today:")
text_label.grid(column=1, row=1, sticky=W)

count_label = Label(text="")
count_label.grid(column=2, row=1, sticky=E)

text = Text(wrap=WORD)
text.grid(column=1, row=2, columnspan=2)
text.focus()

save_button = Button(text='Save', command=save_text, width=10)
save_button.grid(column=1, row=3, columnspan=2, pady=10)

# Bind any key to handle user input
text.bind("<Key>", handle_input)
# -------------------------------------------------------------


# Start the activity checking thread
activity_thread = threading.Thread(target=check_activity, args=(root,))
activity_thread.daemon = True
activity_thread.start()

# Run the Tkinter event loop
root.mainloop()
