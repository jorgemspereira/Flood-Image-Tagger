import os
import random
from pathlib import Path
from tkinter import *

import pandas as pd
from PIL import ImageTk, Image

from models.FloodClass import FloodClass


class Window(Frame):

    def __init__(self, path_to_csv, path_to_dataset, master=None):
        Frame.__init__(self, master)
        self.images = os.listdir(path_to_dataset)
        self.path_to_dataset = path_to_dataset
        self.path_to_csv = path_to_csv
        self.master = master

        self.classification_buttons = []
        self.init_buttons = []
        self.non_saved = []

        self.current_image_idx = 0
        self.has_updates = False

        self.current_data_frame = None
        self.init_image_label = None
        self.previous_button = None
        self.image_label = None
        self.save_button = None
        self.quit_button = None
        self.next_button = None
        self.orig_color = None
        self.init_label_1 = None
        self.init_label_2 = None

        self.init_window()

    def init_window(self):
        self.master.title("Image Tagger")
        self.pack(fill=BOTH, expand=1)

        self.init_label_1 = Label(self, text="Welcome to Flood Image Tagger")
        self.init_label_1.config(width=20, wraplengt=150, font=("Courier", 8))
        self.init_label_1.grid(row=0, column=1, columnspan=1)

        self.init_label_2 = Label(self, text="by: Jorge Pereira")
        self.init_label_2.config(width=20, wraplengt=150, font=("Courier", 8))
        self.init_label_2.grid(row=4, column=1, columnspan=1)

        init_image = random.choice(self.images)
        init_image = Image.open(os.path.join(self.path_to_dataset, init_image))
        init_image = init_image.resize((640, 360), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(init_image)

        self.init_image_label = Label(self, image=render)
        self.init_image_label.image = render
        self.init_image_label.grid(row=0, column=0, rowspan=5, sticky=W + E + N + S, padx=5, pady=5)

        start_from_existing = Button(self, text="Classify from the last", command=self.start_existing)
        start_begin = Button(self, text="Verify already classified", command=self.start_begin)

        self.orig_color = start_begin.cget("background")
        self.init_buttons = [start_from_existing, start_begin]

        if not self.results_exists():
            start_from_existing.config(state="disabled")
            start_begin.config(text="Start from the beginning")

        for idx, button in enumerate(self.init_buttons):
            button.config(height=3, width=20)
            button.grid(row=(1 + idx), column=1, sticky=W)

    def clean_init_elements(self):
        for button in self.init_buttons:
            button.grid_forget()
        self.init_image_label.grid_forget()
        self.init_label_1.grid_forget()
        self.init_label_2.grid_forget()

    def get_dataset(self):
        if self.current_data_frame is None:
            return pd.read_csv(self.path_to_csv, header=None)

        if self.current_data_frame is not None and self.has_updates:
            self.has_updates = False
            return pd.read_csv(self.path_to_csv, header=None)

        if self.current_data_frame is not None and not self.has_updates:
            return self.current_data_frame

    def get_first_index(self):
        values = self.get_dataset().iloc[:, 0].tolist()
        values = list(map(str, values))

        for count, image in enumerate(self.images):
            if image.split(".")[0] not in values:
                return count

    def start_existing(self):
        self.current_image_idx = self.get_first_index()
        self.start_begin()

    def start_begin(self):
        self.clean_init_elements()
        self.show_buttons_classes()
        self.update_buttons_classes()
        self.show_img()

    def show_buttons_classes(self):
        none = Button(self, text="None", command=lambda: self.show_next_image(FloodClass.none), fg="green")
        slight = Button(self, text="Slight", command=lambda: self.show_next_image(FloodClass.slight), fg="sandy brown")
        moderate = Button(self, text="Moderate", command=lambda: self.show_next_image(FloodClass.moderate), fg="orange")
        severe = Button(self, text="Severe", command=lambda: self.show_next_image(FloodClass.severe), fg="red")

        none.bind("<Enter>", lambda event: event.widget.configure(text="]-1e+100, 0.00] meters"))
        none.bind("<Leave>", lambda event: event.widget.configure(text="None"))

        slight.bind("<Enter>", lambda event: event.widget.configure(text="]0.00, 1.00] meters"))
        slight.bind("<Leave>", lambda event: event.widget.configure(text="Slight"))

        moderate.bind("<Enter>", lambda event: event.widget.configure(text="]1.00, 5.00] meters"))
        moderate.bind("<Leave>", lambda event: event.widget.configure(text="Moderate"))

        severe.bind("<Enter>", lambda event: event.widget.configure(text="]5.00, 1e+100] meters"))
        severe.bind("<Leave>", lambda event: event.widget.configure(text="Severe"))

        self.classification_buttons = [none, slight, moderate, severe]

        for idx, button in enumerate(self.classification_buttons):
            button.config(height=3, width=20)
            button.grid(row=idx, column=1, columnspan=2, sticky=W)

        self.quit_button = Button(self, text="Quit", command=self.exit_client, height=3, width=9)
        self.save_button = Button(self, text="Save", command=self.save_client, state="disabled", height=3, width=9)

        self.save_button.grid(row=4, column=2)
        self.quit_button.grid(row=4, column=1)

    def save_client(self):
        if not self.results_exists():
            df = pd.DataFrame(self.non_saved)
        else:
            df = self.get_dataset()
            for index, row in df.iterrows():
                for element in self.non_saved:
                    if str(row[0]) == str(element[0]):
                        row[1] = element[1]
                        self.non_saved.remove(element)
                        break

            if len(self.non_saved) != 0:
                df = df.append(pd.DataFrame(self.non_saved), ignore_index=True)
                self.has_updates = True

        df.to_csv(self.path_to_csv, index=False, header=False)
        self.save_button.config(state="disable")
        self.non_saved = []

    def exit_client(self):
        if len(self.non_saved) == 0:
            exit()
        self.popup_leave()

    def popup_leave(self):
        win = Toplevel(self)
        win.wm_title("Are you sure?")
        win.resizable(False, False)

        label = Label(win, text="Some results are not saved. Are you sure you want to leave?")
        label.grid(row=0, column=0, columnspan=2)

        yes_button = Button(win, text="Yes", command=exit, width=25)
        no_button = Button(win, text="No", command=win.destroy, width=25)
        yes_button.grid(row=1, column=1)
        no_button.grid(row=1, column=0)

    def show_img(self):
        image = Image.open(os.path.join(self.path_to_dataset, self.images[self.current_image_idx]))
        image = image.resize((640, 360), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)

        canvas = Canvas(self, width=640, height=360)
        canvas.grid(row=0, column=0, rowspan=5, sticky=W + E + N + S, padx=5, pady=5)
        canvas.create_image(0, 0, image=render, anchor=NW)

        self.previous_button = Button(self, text="Previous", command=self.previous_image_button_handler, width=10)
        self.next_button = Button(self, text="Next", command=self.next_image_button_handler, width=10)
        self.verify_directional_buttons()

        canvas.create_window(270, 340, anchor=S, window=self.previous_button)
        canvas.create_window(370, 340, anchor=S, window=self.next_button)
        canvas.mainloop()

    def show_next_image(self, flood_class=None, next_img=True):
        current_image = self.images[self.current_image_idx]
        current_image = current_image.split(".")[0]

        if flood_class is not None:
            for item in self.non_saved:
                if item[0] == current_image:
                    self.non_saved.remove(item)
                    break

            self.non_saved.append((current_image, flood_class.value))

        if len(self.non_saved):
            self.save_button.config(state="active")

        self.current_image_idx = self.current_image_idx + 1 if next_img else self.current_image_idx - 1
        self.update_buttons_classes()
        self.show_img()

    def update_buttons_classes(self):
        self.clean_color_buttons()
        classification = self.get_classification_for_image()
        if classification is not None:
            button = self.classification_buttons[classification.value]
            button.config(bg="sky blue")

    def clean_color_buttons(self):
        for button in self.classification_buttons:
            button.config(bg=self.orig_color)

    def previous_image_button_handler(self):
        self.show_next_image(next_img=False)

    def next_image_button_handler(self):
        self.show_next_image()

    def verify_directional_buttons(self):
        self.verify_previous_button_state()
        self.verify_next_button_state()

    def verify_previous_button_state(self):
        if self.current_image_idx == 0:
            self.previous_button.config(state="disabled")
        else:
            self.previous_button.config(state="active")

    def verify_next_button_state(self):
        classification_next = self.get_classification_for_image()
        if self.current_image_idx == (len(self.images) - 1) or classification_next is None:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="active")

    def get_classification_for_image(self):
        non_saved = self.classification_from_non_saved()
        if non_saved is not None:
            return non_saved

        from_file = self.classification_from_file()
        if from_file is not None:
            return from_file

        return None

    def classification_from_non_saved(self):
        for non_saved in self.non_saved:
            if self.images[self.current_image_idx].startswith(non_saved[0]):
                return FloodClass(non_saved[1])

        return None

    def classification_from_file(self):
        if self.results_exists():
            current_img = self.images[self.current_image_idx].split(".")[0]
            for index, row in self.get_dataset().iterrows():
                if str(row[0]) == current_img:
                    return FloodClass(row[1])

        return None

    def results_exists(self):
        return Path(self.path_to_csv).is_file()
