from sys import path
import tkinter as tk
from tkinter import StringVar
from tkinter.constants import END, INSERT
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image
import numpy as np
import cv2

root = tk.Tk()
root.title("Image Steganography")
root.geometry("800x650")

def pixel_to_bin(mess):
    return [format(i,'08b') for i in mess]


def mask(image,message):
    secret_msg = ''.join(format(ord(i),'08b') for i in message) #this is used to convert string into binary
    #.join to join the characters to string fortmat to convert to binary where as ord gives ascii equivalent

    n_bytes_image = image.shape[0] * image.shape[1] * 3 // 8;

    if n_bytes_image < len(secret_msg):
        raise ValueError("Error : the size dosenot match")
    
    data_index = 0
    data_len = len(secret_msg)

    for values in image:
        for pixel in values:
            r,g,b = pixel_to_bin(pixel)
            if data_index < data_len:
                pixel[0] = int(r[:-1]+secret_msg[data_index],base=2)
                #print(f'r => {r},{r[:-1]+secret_msg[data_index]},{val},{secret_msg[data_index]}')
                data_index+=1
            if data_index < data_len:
                pixel[1] = int(g[:-1]+secret_msg[data_index],base=2)
                #print(f'g => {g},{g[:-1]+secret_msg[data_index]},{val},{secret_msg[data_index]}')
                data_index+=1
            if data_index < data_len:
                pixel[2] = int(b[:-1]+secret_msg[data_index],base=2)
                #print(f'b => {b},{b[:-1]+secret_msg[data_index]},{val},{secret_msg[data_index]}')
                data_index+=1
            if data_index >= data_len:
                break
    return image

def unmask(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r,g,b = pixel_to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    eight_bit_list = [binary_data[i : i+8] for i in range(0,len(binary_data),8)]#here we are keeping a stepsize as 8 that means we are jumping for 8 values and we are grabing that 8 values from binary_data and storing in eight_bit_list
    data = ""
    for i in eight_bit_list:
        data += chr(int(i,base=2))
        if data[-5:] == "#####":
            break
    return data[:-5]

def encode():
    image = cv2.imread(path)
    message = txt.get("1.0",END)
    message += "#####"
    encoded_image = mask(image,message)
    cv2.imwrite("encoded_un.png",encoded_image)
    secret_image = Image.open('encoded_un.png')
    np_load_image = np.asarray(secret_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    label_image.config(text="Encoded Image")
    label_image.text = "Encoded Image"
    render = ImageTk.PhotoImage(np_load_image)
    disp_image.config(image = render)
    disp_image.image = render
    txt.delete("1.0",END)

def decode():
    image = cv2.imread(path)
    text = unmask(image)
    print("decoded image is :")
    print("The Decoded message is => ",text)
    secret_image = Image.open('encoded_un.png')
    np_load_image = np.asarray(secret_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    label_image.config(text="Decoded Image")
    render = ImageTk.PhotoImage(np_load_image)
    disp_image.config(image = render)
    disp_image.image = render
    txt_decode.insert(INSERT,text,END)


def openImage():
    file = askopenfilename()
    global path
    path = file
    if file is not None:
        load_image = Image.open(file)
        np_load_image = np.asarray(load_image)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        label_image.config(text="Selected Image")
        disp_image.config(image = render)
        disp_image.image = render

button = tk.Button(root,text="Select Image",width=25,command=openImage)
button.place(x=250,y=10)

label_image = tk.Label(root)
label_image.place(x=20,y=50)

disp_image = tk.Label(root)
disp_image.place(x=20,y=70)

label_encode = tk.Label(root,text="Enter the text here")
label_encode.place(x=540,y=35)

txt = tk.Text(root, width=30)
txt.place(x=540, y=55, height=165)

btn_encode = tk.Button(root,text="Encode",width=25,command=encode)
btn_encode.place(x=540,y=300)

btn_decode = tk.Button(root,text="Decode",width=25,command=decode)
btn_decode.place(x=540,y=340)

label_decode = tk.Label(root,text="Decoded text")
label_decode.place(x=540,y=440)

txt_decode = tk.Text(root, width=30)
txt_decode.place(x=540, y=460, height=165)

root.mainloop()