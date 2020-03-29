from tkinter import *
import BotManager, ArtManager1, Utils, BotTwitch
import threading

artManager = ArtManager1.ArtManager1()
botTwitch = BotTwitch.BotTwitch(artManager)

class Main:
    def __init__(self):
        
        global botTwitch
        global artManager
        # self.runGwapWindow(artManager, botTwitch)
        thread1 = threading.Thread(target=self.runGwapWindow, args=(artManager, botTwitch,))
        thread1.start()
        botTwitch.MainBotProcess(artManager)
        # thread2 = threading.Thread(target=botTwitch.MainBotProcess, args=(artManager,))
        # thread2.start()

        # thread3 = threading.Thread(target=botTwitch.CheckScoreProcess)
        # thread3.start()
        

    def runGwapWindow(self, artManager, botTwitch):
        window = Tk()
        window.title('GWAP for Ukiyo-e images')
        # window.geometry("1660x960+5+10")
        window.geometry("1670x1040")
        window.resizable(0, 0)
        window.configure(background='white')
        
        artManager.initialize_window(window)
        botManager = BotManager.BotNotifier(artManager, botTwitch)
        window.mainloop()

# Run everything here
Main()

# class Hello:
#     def __init__(self):

#         self.describers = {}
#         self.voters = {}
    
#     def get_voters(self):
#         return self.voters

# hello = Hello()

# hello.get_voters()["user"] = "whattt"

# print(hello.get_voters())
