import requests
import tkinter as tk
import sys
import os

# UNNECESSARY
import base64
import re
import io
import urllib.request
from PIL import Image

# UNNECESSARY
def convert_extra(url):
    url = re.sub("/^data:image\\/[a-z]+;base64,/", "", url) # gets rid of base64 indicator
    url = re.sub("\\?.*", "", url) # gets rid of queries
    match = re.findall("\\.\\w*$", url)
    print(extension)

    if(len(match) == 0): # no extension exists
        # need to check if base64 (could be cdn)
        binary = base64.b64decode(url)
        print(binary)
        img = Image.frombytes("RGB", (300, 168), binary)
        img.save("out/cool.png")
    else: # an extension exists
        extension = match[0]
        urllib.request.urlretrieve(url, f"in/image{extension}")
        img = Image.open(f"in/image{extension}")
        size = img.size
        print(size)

        img.save("out/image.png")

# UNNECESSARY 
def init_gui():
    root = tk.Tk()
    root.title("Image Converter :3")
    root.geometry("600x400")
    root.configure(background='gray8')

    label = tk.Label(root, text="URL to convert:", font=("calibre", 25, "bold"))
    url = tk.Text(root, width=50, height=10)
    button = tk.Button(root, text="Submit", width=25, height=1, command=lambda:(convert(url.get("1.0", "end-1c"))))

    label.pack(pady=25, anchor="center")
    url.pack(anchor="center")
    button.pack(anchor="center")

    tk.mainloop()

def convert(url, filename):
    # error handling?

    data = requests.get(url, stream=True).content
    with open(f"out/{filename}", "wb") as output:
        output.write(data)

def main():
    if(not os.path.exists("in")):
        os.makedirs("in")
    if(not os.path.exists("out")):
        os.makedirs("out")

    if(len(sys.argv) < 2):
        print("No link specified.")
        return
    
    # support for uploading files (no longer cli)
    
    filename = "image.png"

    extensions = {".apng", ".png", ".avif", ".gif", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".svg", ".webp"}
    if(len(sys.argv) > 2):
        match = re.findall("\\.\\w*$", sys.argv[2])
        extension = None
        if(len(match)):
            extension = match[0]
            if(extension in extensions):
                filename = sys.argv[2]
            else:
                print("Invalid extension. Defaulting to .png")
                filename = sys.argv[2][:(-1*len(extension))] + ".png"
        else:
            print("No extension specified. Defaulting to .png")
            filename = sys.argv[2] + ".png"
    else:
        print("No filename specified. Defaulting to image.png")
    
    convert(sys.argv[1], filename)

if __name__ == '__main__':
    main()