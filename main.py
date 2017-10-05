from PIL import Image, ImageTk
import tkinter as tk
import os
import json




if __name__ == "__main__":
    try:
        settings = json.load(open("settings.json"))
        gotw = settings["gotw"]
        ssotw = settings["ssotw"]
        image_directory = "images"
        try:
            infile = os.path.join(image_directory, ssotw)
        except IOError:
            print("Screenshot not found, recreating settings file.")
            raise IOError
    except IOError:
        gotw = input("Please enter the game of the week: ")
        ssotw = input("Please enter the filename for the game of the week's screenshot: ")
        settings = {"gotw": gotw, "ssotw": ssotw}
        json.dump(settings, open("settings.json","w"))

    root = tk.Tk()

    width = 800
    height = 400

    size = width, height
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            img = Image.open(infile)
            img.thumbnail(size, Image.ANTIALIAS)
        except IOError:
            print("cannot create thumbnail for '%s'" % infile)

    tkimage = ImageTk.PhotoImage(img)

    root.geometry('{}x{}'.format(width, height+20))
    gamelabel = tk.Label(root, text=gotw).pack()
    tk.Label(root, image=tkimage).pack()

    root.mainloop()