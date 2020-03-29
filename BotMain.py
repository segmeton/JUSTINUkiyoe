from tkinter import *
import tkinter as tk
import BotManager
import ArtManager
import Utils
import threading

import time

class Main:
    def __init__(self):
        thread1 = threading.Thread(target=self.runArtManagerWindow)
        thread1.start()
        thread2 = threading.Thread(target=self.runBotManager)
        thread2.start()

    def runArtManagerWindow(self):
        window2 = tk.Tk()
        window2.title('Vote BG')
        window2.geometry("350x800") 
        window2.resizable(0, 0) 
        artManager = ArtManager.ArtManager2(window2)
        window2.mainloop()
    
    def runBotManager(self):
        window1 = tk.Tk()
        window1.title("Bot Manager")
        window1.configure(background="green")
        window1.geometry("800x100") 
        window1.resizable(0, 0) 
        window1.columnconfigure(0, weight=1)
        window1.rowconfigure(0, weight=1)

        botManager = BotManager.BotNotifier(window1)
        window1.mainloop()

# Run everything here
Main()



