# Flood Image Tagger

A simple graphical user interface program that allows to classify images regarding the severity of floods, into four different classes:

 - None -----> ]-1e+100, 0] meters
 - Slight ----> ]0, 1] meters
 - Moderate -> ]1, 5] meters
 - Severe ----> ]5, 1e100] meters

To run the program simply execute:
 
```bash
python3 main.py 
    --images [path to a folder containing the images] 
    --result [path to a file to save the classifications (may not exist yet)]
```
