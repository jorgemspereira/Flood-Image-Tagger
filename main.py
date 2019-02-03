from tkinter import Tk

from models.Window import Window


def main():
    path_to_csv = "C:\\Users\\jorge\\Desktop\\lol.csv"
    path_to_dataset = "C:\\Users\\jorge\\Desktop\\Thesis\\datasets\\" \
                      "MediaEval2017\\Classification\\development_set\\devset_images"

    root = Tk()
    root.geometry("810x375")
    root.resizable(False, False)
    app = Window(path_to_csv, path_to_dataset, root)
    root.mainloop()


if __name__ == "__main__":
    main()
