from tkinter import *
import tkinter as tk
import Utils
import json
import sys

import pygame

class BotNotifier:

    volume = 0.1
    is_use_music = False

    def __init__(self, artManager, botTwitch):
        

        self.artManager = artManager
        self.botTwitch = botTwitch
        self.utils = Utils.Utils()

        text = 'Please describe them in format: "imageID:description". For example:\n \
             A:There is a group of kids playing on a beach.'
        

        self.botTwitch.giving_stop_voting_signal() # stop voting at the beginning   
        
        self.label = Label(self.artManager.Bottom, text=text, bg="white", fg="black", 
                            font="arial 25 bold", wraplength=1600)
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        top_score_text = self.set_top_score_text()

        self.top_score_label = Label(self.artManager.TopRight, text=top_score_text, bg="white", 
                                    fg="blue", font="arial 16")
        self.top_score_label.grid(row=0, column=0, padx=3, pady=1, sticky=W)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)

        self.quality_win_des = {}
        self.bad_win_des = {}

        self.session = 0
        self.twinkle_signal = 0
        self.update_label()
        # self.check_at_least_has_one_description() # start 
        self.create_notification_label()

        # play music
        pygame.init()
        if self.is_use_music:
            pygame.mixer.music.load("Data/BGM/sukiyaki_instrumental_describing.mp3")
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

    def check_at_least_has_one_description(self):
        while True:
            if len(self.botTwitch.get_audiences().get_describers()) == 1:
                self.update_label()
                break

    def set_top_score_text(self):
        top_score_text = "Ranking score:\n"
        top_participants = self.botTwitch.get_audiences().get_top_participants()
        top_users_text = []
        if top_participants is not None:
            for participant in top_participants:
                top_users_text.append(participant[0] + ": " + str(int(round(participant[1].get("total_score")*10))))
        return top_score_text + "\n".join(top_users_text)

    def create_notification_label(self):
        if self.twinkle_signal == 0:
            self.label.after(1000, self.change_label_color)
            self.twinkle_signal = 1
        else:
            self.label.after(1000, self.revert_label_color)
            self.twinkle_signal = 0
        
        self.label.after(1000, self.create_notification_label)

    # set time
    def update_label(self):
        # time = 90000 # describing session
        time = 80000
        if self.session == 0:
            self.label.after(time, self.change_label_text)
            self.session = 1
        elif self.session == 1:
            # time = 35000 # voting session
            time = 30000
            self.label.after(time, self.showing_winner)
            self.session = 2
        else:
            # time = 15000 # result
            time = 10000
            self.label.after(time, self.revert_label_text)
            self.session = 0
        self.label.after(time, self.update_label)
    
    def play_sound(self):
        self.bgm.play()

    def change_label_color(self):
        self.label.configure(fg="green")

    def revert_label_color(self):
        self.label.configure(fg="black")

    def change_label_text(self):

        #change music
        if self.is_use_music:
            pygame.mixer.music.unload()
            pygame.mixer.music.load("Data/BGM/sukiyaki_instrumental_voting.mp3")
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

        self.botTwitch.giving_stop_describing_signal()
        self.artManager.Title.configure(text="Voting session                                 ")
        self.artManager.Remind.configure(text="")

        row1 = row2 = row3 = 2
        if bool(self.botTwitch.get_audiences().get_descriptions()):
            text = 'Please vote for only one description that best suits its image above in format: "#description_id". For example: #1'
            win_des = self.botTwitch.get_audiences().get_win_des()
            images = self.artManager.get_images()
            print("win_des in BotManager ", json.dumps(self.botTwitch.get_audiences().get_win_des()))

            used_images = self.botTwitch.get_audiences().get_used_images()

            for des_id, value in self.botTwitch.get_audiences().get_descriptions().items():
                if value[1] in win_des:
                    if win_des.get(value[1]).get('used_time') >= 1:
                        
                        if win_des.get(value[1]).get('score') >= 2 or win_des.get(value[1]).get('score') < 0.3: # not showing description 
                                                                                                                 # if its score in this range
                            if win_des.get(value[1]).get('score') >= 2:
                                self.quality_win_des[value[1]] = (win_des.get(value[1]), images.get(value[0]))
                            else:
                                self.bad_win_des[value[1]] = win_des.get(value[1])
                            
                            print("remove ", value[1], " out of win_des dict")
                            del self.botTwitch.get_audiences().get_win_des()[value[1]]
                            print("win_des after remove key ", json.dumps(self.botTwitch.get_audiences().get_win_des()))

                            continue
                else:
                    if used_images.get(value[0]) == 1 and value[2] == 'AI' \
                        and self.botTwitch.get_num_des_of_image(value[0]) > 0:
                        # not show the previous lost description by Pythia if the image has descriptions
                        continue

                des = des_id + ":" + value[1]
                if value[0] == "A":
                    l7 = Label(self.artManager.Center, font=('arial', 19), text=des, bg="white", wraplength=560).grid(row=row1, column=0)
                    row1 += 1
                elif value[0] == "B":
                    l7 = Label(self.artManager.Center, font=('arial', 19), text=des, bg="white", wraplength=560).grid(row=row2, column=2)
                    row2 += 1
                else:
                    l7 = Label(self.artManager.Center, font=('arial', 19), text=des, bg="white", wraplength=560).grid(row=row3, column=4)
                    row3 += 1
        else:
            text = "There is no description to vote. :("
        
        self.label.configure(text=text)
        self.utils.retrieveImages() # random retrieve other images
        

    def revert_label_text(self):

        # change music
        if self.is_use_music:
            pygame.mixer.music.unload()
            pygame.mixer.music.load("Data/BGM/sukiyaki_instrumental_describing.mp3")
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

        if self.botTwitch.is_using_tts and self.botTwitch.is_tts_result:
            self.botTwitch.socketConnector.send("clear", "command")

        self.botTwitch.setGameSession() # increase game session to next round
        self.artManager.Title.configure(text="Describing session                                 ")
        self.artManager.Remind.configure(text="Feel free to describe as many images below as you want                        ")
        
        self.reset_description_labels()
        self.artManager.refresh() # refresh to new images
        
        self.botTwitch.get_audiences().refresh_players(self.artManager.get_images())
        self.botTwitch.refresh_desid()
        
        self.quality_win_des = {}
        self.bad_win_des = {}

        text = 'Please describe them in format: "imageID:description". For example:\n \
             A:There is a group of kids playing on a beach.'
            
        self.label.configure(text=text)

    def reset_description_labels(self):
        self.artManager.Center.destroy()

    def showing_winner(self):
        self.botTwitch.giving_stop_voting_signal()
        game_session = self.botTwitch.getGameSession()

        self.artManager.Title.configure(text="Result of round " + str(game_session) + "                           ")
        text = "Winning descriptions for this round are:\n"
        descriptions = self.botTwitch.get_audiences().get_descriptions()
        images = self.artManager.get_images()

        # rap_text = "I wanna be the ever best that no one ever was"
        rap_text = ""

        for img_id in images:
            des_id = self.botTwitch.get_audiences().get_winning_des_id_foreach_img(img_id)
            if des_id is not None:
                description = descriptions.get(des_id)[1]
                winning_rap = "For image " + des_id + " is  " + description
                text = text + "   " + img_id + ": " + description + " for image " + img_id + "\n"
                rap_text = rap_text + winning_rap + "\n"
            else:
                text = text + "    None for image " + img_id + "\n"
        
        
        participant_results = self.botTwitch.get_audiences().get_participants_results(images, game_session, descriptions)

        if participant_results:
            text = text + "\nScore awarded to players:\n\n"

        for u, value in sorted(participant_results.items()):
            
            game_session_value = value.get(game_session)

            if game_session_value is not None:
            
                added_score = game_session_value.get("added_score")
                if added_score < 0:
                    message = "      User " + u + " get penalized score " + str(int(round(added_score*10))) \
                        + " for describing or voting bad descriptions in previous rounds."
                else:
                    message = "      User " + u + " get score " + str(int(round(added_score*10)))
                text = text + message

        if rap_text != "" and self.botTwitch.is_using_tts and self.botTwitch.is_tts_result:
            self.botTwitch.socketConnector.send(rap_text, "message")

        self.label.configure(text=text)
        self.utils.store_participants_info(participant_results)
        self.utils.store_winning_des(self.botTwitch.get_audiences().get_win_des())
        self.utils.store_ranking()

        if bool(self.quality_win_des):
            self.utils.store_good_winning_des(self.quality_win_des)
        if bool(self.bad_win_des):
            self.utils.store_bad_winning_des(self.bad_win_des)

        top_score_text = self.set_top_score_text()
        self.top_score_label.configure(text=top_score_text)

        # showing full list of ranking
        # self.botTwitch.sendMessage('you can see full list of ranking scores here: https://drive.google.com/file/d/1WY3xdfaJbWxlQoJkjhrq04SdCApIiXT4/view')
