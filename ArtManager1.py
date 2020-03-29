from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import requests, csv, random, json
import Utils

class ArtManager1:
    def __init__(self):
        self.images = {}
        self.set_images()

    def initialize_window(self, window):

        self.window = window
        
        
        self.Top = Frame(self.window, width=1680, height=50, bg="white", relief="raise")
        self.Top.pack(side=TOP, padx=5, pady=5)

        self.TopLeft = Frame(self.Top, width=1350, height=50, bg="white", relief="raise")
        self.TopLeft.pack(side=LEFT, padx=5, pady=5)

        self.TopRight = Frame(self.Top, width=280, height=50, bg="black", relief="raise")
        self.TopRight.pack(side=RIGHT, padx=5, pady=5)

        self.Title = Label(self.TopLeft, font=('castellar', 35, 'bold'), fg="red", bg="white", bd=10, anchor='w')
        self.Title.configure(text="Describing Session                                 ")
        self.Title.grid(row=0,column=0)

        self.Remind = Label(self.TopLeft, font=('arial', 28, 'bold'), 
            text='Feel free to describe as many images below as you want                        ',
            anchor='w', bg='white')
        self.Remind.grid(row=1, column=0, columnspan=5)

        self.Bottom = Frame(self.window, width=1680, height=150, bg="white", relief="raise")
        self.Bottom.pack(side=BOTTOM, padx=10, pady=10)

        # self.Right = Frame(self.window, width=250, height=750, bg="white", relief="raise")
        # self.Right.pack(side=RIGHT, padx=5, pady=5)

        self.show_content_improved()
        
    # this one for refresh GUI if there folder have new IMAGE in ../VoteImage
    def refresh(self):
        try:
            
            self.set_images()

            self.show_content_improved()

        except:
            pass

    def get_images(self):
        return self.images
    
    def set_images(self):
        self.images = {}

        img_ids = ['A', 'B', 'C']
        imgs = Utils.Utils().retrieveImages()
        for i in range(len(imgs)):
            self.images[img_ids[i]] = imgs[i]

    def show_content_improved(self):

        height, width = 450, 550

        self.Center = Frame(self.window, width=1680, height=800, bg="white", relief="raise")
        self.Center.pack(side=BOTTOM, padx=5, pady=5)

        i = 0
        for img_id, image_name in self.images.items():
            T = Label(self.Center, font=('arial', 20, 'bold'), text=img_id, bg="white", anchor="w")
            T.grid(row=0,column=i)
            
            img = ImageTk.PhotoImage(self.resize_image(Image.open("data_preparing/Data/images/" + \
                image_name), height, width))
            pannel = Label(self.Center, image = img, height=height, width=width, bg="white", padx=0)
            pannel.grid(row=1, column=i)
            pannel.image = img
            
            if i < 4:
                Label(self.Center, font=('arial', 2), bg="white", text=" ").grid(row=1, column=i+1)
            i += 2

    def show_content(self):
        bg_img1_order = "A"
        bg_img2_order = "B"
        bg_img3_order = "C"

        height, width = 450, 560

        self.Center = Frame(self.window, width=1680, height=750, bg="white", relief="raise")
        self.Center.pack(side=BOTTOM, padx=5, pady=5)

        self.T = Label(self.Center, font=('arial', 20, 'bold'), text=bg_img1_order, bg="white", anchor="w")
        self.T.grid(row=0,column=0)
        
        # img = ImageTk.PhotoImage(self.resize_image(Image.open("../VoteImage/image1.jpg"), 550))
        img = ImageTk.PhotoImage(self.resize_image(Image.open("data_preparing/Data/images/" + \
            self.images.get(bg_img1_order)), height, width))
        self.panel = Label(self.Center, image = img, height=height, width=width, bg="white", padx=0)
        self.panel.grid(row=1, column=0)
        self.panel.image = img
        
        Label(self.Center, font=('arial', 2), bg="white", text=" ").grid(row=1, column=1)

        self.T2 = Label(self.Center, font=('arial', 20, 'bold'), bg="white", text=bg_img2_order, anchor="w")
        self.T2.grid(row=0, column=2)
        
        # img2 = ImageTk.PhotoImage(self.resize_image(Image.open("../VoteImage/image2.jpg"), 550))
        img2 = ImageTk.PhotoImage(self.resize_image(Image.open("data_preparing/Data/images/" + \
            self.images.get(bg_img2_order)), height, width))
        self.panel2 = Label(self.Center, image = img2, height=height, width=width, bg="white", padx=0)
        self.panel2.grid(row=1, column=2)
        self.panel2.image = img2

        Label(self.Center, font=('arial', 2), bg="white", text=" ").grid(row=1, column=3)

        self.T3 = Label(self.Center, font=('arial', 20, 'bold'), text=bg_img3_order, bg="white", anchor="w")
        self.T3.grid(row=0, column=4)
        
        # img3 = ImageTk.PhotoImage(self.resize_image(Image.open("../VoteImage/image3.jpg"), 550))
        img3 = ImageTk.PhotoImage(self.resize_image(Image.open("data_preparing/Data/images/" + \
            self.images.get(bg_img3_order)), height, width))
        self.panel3 = Label(self.Center, image = img3, height=height ,width=width, bg="white", padx=0)
        self.panel3.grid(row=1, column=4)
        self.panel3.image = img3
    
    def resize_image(self, img, height, width):
        if img.size[0] > img.size[1]:
            wpercent = (width/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((width, hsize), Image.ANTIALIAS)
        else:
            wpercent = (height/float(img.size[1]))
            wsize = int((float(img.size[0])*float(wpercent)))
            img = img.resize((wsize, height), Image.ANTIALIAS)

        return img