import socket
import datetime
import re
import threading
import time

from PIL import Image
import requests
from io import BytesIO
import random
import csv

import codecs
import webbrowser

from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

### Options (Don't edit)
SERVER = "irc.twitch.tv"  # server
PORT = 6667 # port
### Options (Edit this)
PASS = "oauth:kykwow2afwwea6yvu92d6qoebt44c3"  # bot password can be found on https://twitchapps.com/tmi/
BOT = "botch932"  # Bot's name [NO CAPITALS]
CHANNEL = "ch932"  # Channal name [NO CAPITALS]
OWNER = "ch932"  # Owner's name [NO CAPITALS]

### global variables
isStopDescribingSignal = False
isStopVotingSignal = False

### Functions



    
# end here, right?
# below this draw GUI
def drawGUIVote():
    global bg_img1
    global bg_img2
    global bg_img3
    
    name_bg_file = open('../VoteImage/name_bg.txt','r')
    name_bg_file_lines = name_bg_file.read().splitlines()  
    bg_img1 = name_bg_file_lines[0]
    bg_img2 = name_bg_file_lines[1]
    bg_img3 = name_bg_file_lines[2]

    
    # asking people vote and tag pictures
    sendMessage(s, 'Please vote and describe pictures on the left of screen you prefer follow format "imageID:discription"')
    t = threading.Timer(60.0, giving_stop_describing_signal) # after 1 min stop receiving chat messages
    t.start()

    # time.sleep(60)
    t.cancel()

    t1 = threading.Timer(15.0, giving_stop_voting_signal)
    t1.start()
    t1.cancel()


        
def MainBotProcess():
    global isStopDescribingSignal   
    while True:
        try:
            readbuffer = s.recv(2048)
            readbuffer = readbuffer.decode()
            temp = readbuffer.split("\n")
            readbuffer = readbuffer.encode()
            readbuffer = temp.pop()
        except:
            temp = ""
        for line in temp:
            if line == "":
                break
            # So twitch doesn't timeout the bot.
            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                s.send(msgg)
                print(msgg)
                break
            # get user
            user = getUser(line)
            # get message send by user
            message = getMessage(line)
            # for you to see the chat from CMD             
            print(user + " > " + message)         
            # sends private msg to the user (start line)
            PMSG = "/w " + user + " "
            

################################# Command ##################################
############ Here you can add as many commands as you wish of ! ############
############################################################################
            writeFileLog(user,message)#write log file
            if (user == OWNER) and (message == "!next\r"):
                writeFile(user,"!next")
                sendMessage(s, "Next level")
                break
            elif (user == OWNER) and (message == "!retry\r"):
                writeFile(user,"!retry")
                sendMessage(s, "Retry level")
                break  
            elif (user == OWNER) and (message == "!s\r"):#Shoot
                writeFile(user,"!s")
                break
            elif (message == "!aa\r")  or (message == "!AA\r"):#Ability  #user1     
                writeFile(user,"!a")
                break            
            elif (message == "!am\r")  or (message == "!AM\r"):       
                writeFile(user,"!m")
                break
            elif (message == "!al\r") or (message == "!AL\r"):       
                writeFile(user,"!l")
                break
            elif (message == "!au\r") or (message == "!AU\r"):       
                writeFile(user,"!u")
                break
            elif (message == "!ad\r") or (message == "!AD\r"):       
                writeFile(user,"!d")
                break
            elif (message == "!ba\r")  or (message == "!BA\r"):#Ability   #user2
                writeFile2(user,"!a")
                break            
            elif (message == "!bm\r")  or (message == "!BM\r"):       
                writeFile2(user,"!m")
                break
            elif (message == "!bl\r") or (message == "!BL\r"):       
                writeFile2(user,"!l")
                break
            elif (message == "!bu\r") or (message == "!BU\r"):       
                writeFile2(user,"!u")
                break
            elif (message == "!bd\r") or (message == "!BD\r"):       
                writeFile2(user,"!d")
                break   
            elif (message == "!bg1\r"):       
                writeFileVote(user,"!bg1")
                break  
            elif (message == "!bg2\r"):       
                writeFileVote(user,"!bg2")
                break 
            elif (message == "!bg3\r"):       
                writeFileVote(user,"!bg3")
                break             
            elif (user != OWNER) and (message == "!next\r"):
                sendMessage(s, "This is private command for ownner.")
                break   
            elif (user != OWNER) and (message == "!retry\r"):
                sendMessage(s, "This is private command for ownner.")
                break
            elif not isStopDescribingSignal and (user != OWNER) and len(message.split(":")) == 2:
                print(user + " and " + message)
                writeVoteAndTagsData(user, message)
                writeDescriptionsData(user, message)
                break
            elif (user != OWNER) and message.startswith("#"):
                writeVoteData(user, message)
                break
            else:
                # Replace all non-alphanumeric non-# characters in a string.
                message = re.sub('[^0-9a-zA-Z#! ]+', '', message)
                if (message == ""):
                    break
                else :
                    writeFile(user,message)
                    break      
############################################################################
# RandomBackGround()

thread1 = threading.Thread(target=MainBotProcess)
thread1.start()

thread2 = threading.Thread(target=CheckScoreProcess)
thread2.start()

thread3 = threading.Thread(target=drawGUIVote)
thread3.start()

