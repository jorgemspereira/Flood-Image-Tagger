import argparse
from tkinter import Tk

from models.Window import Window


def start_window(args):
    root = Tk()
    root.geometry("970x550")
    root.resizable(False, False)
    root.iconbitmap(default='./icon/ist_logo.ico')
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    app = Window(args.path_to_csv, args.path_to_dataset, root)
    app.mainloop()


def parse_args():
    parser = argparse.ArgumentParser(description="Flood image tagger.")
    parser.add_argument("--images", dest="path_to_dataset", action="store_const", const=None,
                        default="C:\\Users\\jorge\\Desktop\\Thesis\\datasets\\EuropeanFlood2013\\imgs_small",
                        help="Path for fold with the images.")
    parser.add_argument("--result", dest="path_to_csv", action="store_const",
                        default=".\\results\\dataset_european_flood_2013.csv", const=None,
                        help="Path for the .csv file containing the classification.")
    return parser.parse_args()


if __name__ == "__main__":
    start_window(parse_args())
