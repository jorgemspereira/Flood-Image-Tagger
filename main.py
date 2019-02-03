import argparse
from tkinter import Tk

from models.Window import Window


def start_window(args):
    root = Tk()
    root.geometry("810x375")
    root.resizable(False, False)
    app = Window(args.path_to_csv, args.path_to_dataset, root)
    app.mainloop()


def parse_args():
    parser = argparse.ArgumentParser(description="Flood image tagger.")
    parser.add_argument("--images", dest="path_to_dataset", action="store_const", const=None,
                        default="C:\\Users\\jorge\\Desktop\\Thesis\\datasets\\MediaEval2017"
                                "\\Classification\\development_set\\devset_images",
                        help="path for the MediaEval 2017 dataset")
    parser.add_argument("--result", dest="path_to_csv", action="store_const",
                        default="C:\\Users\\jorge\\Desktop\\lol.csv", const=None,
                        help="path for the .csv file containing the classification")
    return parser.parse_args()


if __name__ == "__main__":
    start_window(parse_args())
