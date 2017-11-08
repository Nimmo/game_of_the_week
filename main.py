from PIL import Image, ImageTk
import imageio
import tkinter as tk, threading
import os
import json
import sys


def stream(label):

    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image

        
def prepare_file(infile, size):
    image_types = ["png", "jpg"]
    filetype = infile.split(".")[-1]
    if filetype in image_types:
        filetype = "image"
        outfile = os.path.splitext(infile)[0] + ".thumbnail"
        if infile != outfile:
            try:
                img = Image.open(infile)
                img.thumbnail(size, Image.ANTIALIAS)
            except IOError:
                print("cannot create thumbnail for '%s'" % infile)
                sys.exit()
    else:
        filetype = "video"
        img = infile            

    return img, filetype

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
    except:
        print("An unexpected error occurred, exiting gracefully.")
        sys.exit()

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Game of the week")
    root.configure(bg="black")

    width = 800
    height = 400

    size = width, height-60
    
    screenshot, filetype = prepare_file(infile, size)    

    root.geometry('{}x{}'.format(width, height+20))
    game_of_the_week_label = tk.Label(root, text="Game of the week:", font=("Courier", 44), bg="black", fg="white").pack()

    if filetype == "image":
        tkscreenshot = ImageTk.PhotoImage(screenshot)
        tk.Label(root, image=tkscreenshot).pack()
    else:
        video = imageio.get_reader(screenshot)
        my_label = tk.Label(root)
        my_label.pack()
        thread = threading.Thread(target=stream, args=(my_label,))
        thread.daemon = 1
        thread.start()

    
    
    gamelabel = tk.Label(root, text=gotw, font=("Courier", 44), bg="black", fg="white").pack()
    root.mainloop()
