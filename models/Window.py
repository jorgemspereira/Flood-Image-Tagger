import os
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

        self.init_buttons = []
        self.non_saved = []

        self.current_image = 0
        self.init_label = None
        self.image_label = None
        self.save_button = None
        self.quit_button = None

        self.init_window()

    def init_window(self):
        self.master.title("Image Tagger")
        self.pack(fill=BOTH, expand=1)

        self.init_label = Label(self, text="Hey there good lookin!")
        self.init_label.grid(row=0, column=0, columnspan=2)

        start_from_existing = Button(self, text="Start From Existing", command=self.start_existing)
        start_begin = Button(self, text="Start From Begin", command=self.start_begin)
        self.init_buttons = [start_from_existing, start_begin]

        if not self.results_exists():
            start_from_existing.config(state="disabled")

        for idx, button in enumerate(self.init_buttons):
            button.config(height=3, width=20)
            button.grid(row=1, column=(idx + 1), sticky=W)

    def clean_init_elements(self):
        for button in self.init_buttons:
            button.grid_forget()
        self.init_label.grid_forget()

    def start_existing(self):
        # TODO
        print("lol")

    def start_begin(self):
        self.clean_init_elements()
        self.show_buttons()
        self.show_img()

    def show_buttons(self):
        none = Button(self, text="None", command=lambda: self.show_next_image(FloodClass.none))
        slight = Button(self, text="Slight", command=lambda: self.show_next_image(FloodClass.slight))
        moderate = Button(self, text="Moderate", command=lambda: self.show_next_image(FloodClass.moderate))
        severe = Button(self, text="Severe", command=lambda: self.show_next_image(FloodClass.severe))
        buttons = [none, slight, moderate, severe]

        for idx, button in enumerate(buttons):
            button.config(height=3, width=20)
            button.grid(row=idx, column=1, columnspan=2, sticky=W)

        self.quit_button = Button(self, text="Quit", command=self.exit_client, height=3, width=9)
        self.save_button = Button(self, text="Save", command=self.save_client, state="disabled", height=3, width=9)

        self.save_button.grid(row=4, column=2)
        self.quit_button.grid(row=4, column=1)


    def exit_client(self):
        exit()

    def save_client(self):
        # TODO: Check if exists
        df = pd.DataFrame(self.non_saved, columns=['image', 'class'])
        df.to_csv(self.path_to_csv, index=False)
        self.save_button.config(state="disable")
        self.non_saved = []

    def show_img(self):
        image = Image.open(os.path.join(self.path_to_dataset, self.images[self.current_image]))
        image = image.resize((640, 360), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        self.image_label = Label(self) if self.image_label is None else self.image_label
        self.image_label.image = render
        self.image_label.grid(row=0, column=0, rowspan=5, sticky=W+E+N+S, padx=5, pady=5)
        self.image_label.config(image=render)

    def show_next_image(self, flood_class):
        current_image = self.images[self.current_image]
        current_image = current_image.split(".")[0]
        self.save_button.config(state="active")
        self.non_saved.append((current_image, flood_class.value))
        self.current_image += 1
        self.show_img()

    def results_exists(self):
        return Path(self.path_to_csv).is_file()
