import argparse
from tkinter import Tk

from helpers.Window import Window

EUROPEAN_FLOODS_2013_TAGS = ".\\results\\dataset_european_flood_2013.csv"
EUROPEAN_FLOODS_2013_IMAGES = "C:\\Users\\jorge\\Desktop\\Thesis\\datasets\\EuropeanFlood2013\\imgs_small"

MEDIAEVAL_2017_TEST_SPLIT_TAGS = ".\\results\\dataset_test_mediaeval_2017.csv"
MEDIAEVAL_2017_TEST_SPLIT_IMAGES = "C:\\Users\\jorge\\Desktop\\Thesis\\datasets" \
                                   "\\MediaEval2017\\Classification\\test_set\\testset_images"

MEDIAEVAL_2017_TRAIN_SPLIT_TAGS = ".\\results\\dataset_train_mediaeval_2017.csv"
MEDIAEVAL_2017_TRAIN_SPLIT_IMAGES = "C:\\Users\\jorge\\Desktop\\Thesis\\datasets" \
                                    "\\MediaEval2017\\Classification\\development_set\\devset_images"

MEDIAEVAL_2018_TEST_SPLIT_TAGS = ".\\results\\dataset_test_mediaeval_2018.csv"
MEDIAEVAL_2018_TEST_SPLIT_IMAGES = "C:\\Users\\jorge\\Desktop\\Thesis\\datasets" \
                                   "\\MediaEval2018\\Classification\\test_set\\testset_images"

MEDIAEVAL_2018_TRAIN_SPLIT_TAGS = ".\\results\\dataset_train_mediaeval_2018.csv"
MEDIAEVAL_2018_TRAIN_SPLIT_IMAGES = "C:\\Users\\jorge\\Desktop\\Thesis\\datasets" \
                                    "\\MediaEval2018\\Classification\\development_set\\devset_images"


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
                        default=MEDIAEVAL_2018_TEST_SPLIT_IMAGES, help="Path for fold with the images.")
    parser.add_argument("--result", dest="path_to_csv", action="store_const",
                        default=MEDIAEVAL_2018_TEST_SPLIT_TAGS, const=None,
                        help="Path for the .csv file containing the classification.")
    return parser.parse_args()


if __name__ == "__main__":
    start_window(parse_args())
