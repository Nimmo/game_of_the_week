from PIL import Image, ImageTk

# Required for video support
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

        
def get_filetype(infile):
    image_types = ["png", "jpg"]
    video_types = ["mov"]
    filetype = infile.split(".")[-1]
    if filetype in image_types:
        filetype = "image"
    elif filetype in video_types:
        filetype = "video"

    return filetype

if __name__ == "__main__":
    try:
        settings = json.load(open("settings.json"))
        gotw = settings["gotw"]
        ssotw = settings["ssotw"]
        image_directory = "images"
        try:
            screenshot_file = os.path.join(image_directory, ssotw)
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
    
    file_type = get_filetype(screenshot_file)

    root.geometry('{}x{}'.format(width, height+20))
    game_of_the_week_label = tk.Label(root, text="Game of the week:", font=("Courier", 44), bg="black", fg="white").pack()

    if file_type == "image":
        try:
            img = Image.open(screenshot_file)
            img.thumbnail(size, Image.ANTIALIAS)
        except IOError:
            print("cannot create thumbnail for '%s'" % screenshot_file)
            sys.exit()
        image_container = ImageTk.PhotoImage(img)
        tk.Label(root, image=image_container).pack()
    elif file_type == "video":
        try:
            video = imageio.get_reader(screenshot_file)
        except imageio.core.fetching.NeedDownloadError:
            imageio.plugins.ffmpeg.download()
            video = imageio.get_reader(screenshot_file)
        except OSError:
            print("It looks as though some OS permissions are preventing you from creating a thread to handle the video")
            video = None
        if video is not None:
            video_container = tk.Label(root)
            video_container.pack()
            thread = threading.Thread(target=stream, args=(video_container,))
            thread.daemon = 1
            thread.start()
    else:
        print("There currently isn't support for files of type", file_type + ", raise an issue on github if you feel that it should be supported.")
    game_label = tk.Label(root, text=gotw, font=("Courier", 44), bg="black", fg="white").pack()
    root.mainloop()
