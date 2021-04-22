import socket, time, datetime, re, json

import Utils, Audiences

import SocketConnector

class BotTwitch:

    socketConnector = None
    is_using_tts = True
    is_tts_describing = False
    is_tts_voting = False

    is_tts_result = True

    def __init__(self, artManager):
        ### Options (Don't edit)
        self.SERVER = "irc.twitch.tv"  # server
        self.PORT = 6667  # port
        ### Options (Edit this)
        # self.PASS = "oauth:kykwow2afwwea6yvu92d6qoebt44c3"  # bot password can be found on https://twitchapps.com/tmi/
        # oauth:vsev4928vqu449rr6xwcp1nifwtttu
        self.PASS = "oauth:vsev4928vqu449rr6xwcp1nifwtttu"
        self.BOT = "botch932"  # Bot's name [NO CAPITALS]
        # self.CHANNEL = "ch932"  # Channal name [NO CAPITALS]
        # self.OWNER = "ch932"  # Owner's name [NO CAPITALS]
        self.CHANNEL = "segmeton"  # Channal name [NO CAPITALS]
        self.OWNER = "justin"  # Owner's name [NO CAPITALS]
        self.utils = Utils.Utils()

        self.pattern = re.compile("^[a-zA-Z0-9 ?.!-/:;]*$")

        self.isStopDescribingSignal = False
        self.isStopVotingSignal = False
        self.game_session = self.utils.get_last_game_session() + 1
        # self.game_session = 0

        self.audiences = Audiences.Audiences(artManager.get_images())

        self.des_id = self.audiences.get_init_des_id()

        ### Code start runs
        self.s_prep = socket.socket()
        self.s_prep.connect((self.SERVER, self.PORT))
        self.s_prep.send(("PASS " + self.PASS + "\r\n").encode())
        self.s_prep.send(("NICK " + self.BOT + "\r\n").encode())
        self.s_prep.send(("JOIN #" + self.CHANNEL + "\r\n").encode())

        self.joinchat()
        self.readbuffer = ""

        if self.is_using_tts:
            self.socketConnector = SocketConnector.SocketConnector()

    def get_audiences(self):
        return self.audiences

    def set_audiences(self, audiences):
        self.audiences = audiences

    def get_img_id(self, des_id):
        if des_id in self.audiences.get_descriptions():
            return self.audiences.get_descriptions().get(des_id)[0]
        return None

    def check_description_unique(self, img_id, description):
        des_id = next((id for id, v in self.audiences.get_descriptions().items() if
                       v[0] == img_id and v[1].strip() == description), None)
        if des_id is None:
            return True
        return False

    def refresh_desid(self):
        self.des_id = self.audiences.get_init_des_id()
        print("Initial des_id in BotTwitch ", self.des_id)

    def joinchat(self):
        readbuffer_join = "".encode()
        Loading = True
        while Loading:
            readbuffer_join = self.s_prep.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            temp = readbuffer_join.split("\n")
            readbuffer_join = readbuffer_join.encode()
            readbuffer_join = temp.pop()
            for line in temp:
                Loading = self.loadingCompleted(line)
        self.sendMessage("Chat room joined!")
        print("Bot has joined " + self.CHANNEL + " Channel!")

    def loadingCompleted(self, line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True

    def giving_stop_describing_signal(self):
        print("Stop describing now")
        # self.sendMessage(message)
        self.isStopDescribingSignal = True
        self.isStopVotingSignal = False

        if self.is_using_tts and self.is_tts_describing:
            self.socketConnector.send("clear", "command")

    def giving_stop_voting_signal(self):
        print("Stop voting now")
        # self.sendMessage(message)
        self.isStopVotingSignal = True
        self.isStopDescribingSignal = False

        if self.is_using_tts and self.is_tts_voting:
            self.socketConnector.send("clear", "command")

    def Console(self, line):
        # gets if it is a user or twitch server
        if "PRIVMSG" in line:
            return False
        else:
            return True

    def sendMessage(self, message):
        message = "PRIVMSG #" + self.CHANNEL + " :" + message
        self.s_prep.send((message + "\r\n").encode())

    def getUser(self, line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        try:
            message = (line.split(":", 2))[2].rstrip("\n\r")
        except:
            message = ""
        return message

    def setGameSession(self):
        self.game_session += 1

    def getGameSession(self):
        return self.game_session

    def get_num_des_of_image(self, img_id):
        count = 0
        for value in self.audiences.get_descriptions().values():
            if value[0] == img_id:
                count += 1
        return count

    def MainBotProcess(self, artManager):
        while True:
            try:
                self.readbuffer = self.s_prep.recv(2048)
                self.readbuffer = self.readbuffer.decode()
                temp = self.readbuffer.split("\n")
                self.readbuffer = self.readbuffer.encode()
                self.readbuffer = temp.pop()
            except:
                temp = ""
            for line in temp:
                try:
                    if line == "":
                        break
                    # So twitch doesn't timeout the bot.
                    if "PING" in line and self.Console(line):
                        msgg = "PONG tmi.twitch.tv\r\n".encode()
                        self.s_prep.send(msgg)
                        print(msgg)
                        break
                    # get user
                    user = self.getUser(line)
                    # get message send by user
                    message = self.getMessage(line)
                    # for you to see the chat from CMD
                    # print(user + " > " + message)
                    # sends private msg to the user (start line)
                    PMSG = "/w " + user + " "

                    ################################# Command ##################################
                    ############ Here you can add as many commands as you wish of ! ############
                    ############################################################################
                    self.utils.writeFileLog(user, message)  # write log file

                    if (user == self.OWNER) and (message == "!next\r"):
                        self.utils.writeFile(user, "!next")
                        self.sendMessage("Next level")
                        break
                    elif (user != self.OWNER) and (message == "!next\r"):
                        self.sendMessage("This is private command for ownner.")
                        break
                    elif (user != self.OWNER) and (message == "!retry\r"):
                        self.sendMessage("This is private command for ownner.")
                        break
                    elif (not self.isStopDescribingSignal) and self.isStopVotingSignal and (user != self.OWNER) \
                            and len(message.split(":")) == 2:

                        # print(user + " and " + message)
                        img_id = message.split(":")[0].strip()
                        description = message.split(":")[1].strip()

                        if bool(self.pattern.match(description)):
                            if self.get_num_des_of_image(img_id) <= 6:
                                images = artManager.get_images()
                                if img_id in images:
                                    if self.check_description_unique(img_id, description):

                                        # did = str(self.des_id)
                                        imgs = {}
                                        if user in self.audiences.get_describers():
                                            imgs = self.audiences.get_describers().get(user)
                                        if img_id in imgs:
                                            self.sendMessage("You have updated description for image " + img_id)
                                            did = next(iter(imgs.get(img_id)))  # string
                                        else:
                                            self.des_id += 1
                                            did = str(self.des_id - 1)

                                        # print("did in botTwitch: ", did)

                                        self.audiences.get_descriptions()[did] = (img_id, description, 'human')
                                        self.audiences.get_descriptions()[did] = (img_id, description, 'human')
                                        imgs[img_id] = {did: description}

                                        self.audiences.get_describers()[user] = imgs

                                        self.utils.writeVoteAndTagsData(user, message, images, self.game_session)

                                        # send image description
                                        if self.is_using_tts and self.is_tts_desccribing:
                                            self.socketConnector.send(description, "message")

                                        # print("descriptions in botTwitch " + json.dumps(self.audiences.get_descriptions()))

                                    else:
                                        self.sendMessage("This description is already existed for image " + img_id + \
                                                         ". Please give another desscription.")
                                else:
                                    self.sendMessage(
                                        "There is no typed image id shown on the screen. Please try again.")
                            else:
                                self.sendMessage(
                                    "Descriptions for image " + img_id + " has reached its limit. Choose others.")
                        else:
                            self.sendMessage("The sentence contains characters not supported. Please try again.")
                        break
                    elif (not self.isStopVotingSignal) and self.isStopDescribingSignal and (user != self.OWNER) \
                            and message.startswith("#"):

                        if user not in self.audiences.get_describers():

                            des_id = message.replace("#", "")  # string
                            descriptions = self.audiences.get_descriptions()
                            if des_id in descriptions:
                                description = descriptions.get(des_id)[1]

                                is_voted = True
                                if user in self.audiences.get_old_participants():
                                    if any(d['des'] == description for d in
                                           self.audiences.get_old_participants().get(user)):
                                        # if description == self.audiences.get_old_participants().get(user).get("des"):
                                        is_voted = False
                                        self.sendMessage(
                                            "You cannot vote for this description because it was the winning description you voted or created before")

                                if is_voted:

                                    img_id = self.get_img_id(des_id)

                                    des_list = {}
                                    if img_id in self.audiences.get_voters():
                                        des_list = self.audiences.get_voters().get(img_id)

                                    users = []
                                    if des_id in des_list:
                                        users = des_list.get(des_id)

                                        if user not in users:
                                            users.append(user)
                                            # print("images in BotTwitch " + json.dumps(artManager.get_images()))
                                            self.utils.writeVoteData(user, img_id, description, artManager.get_images(),
                                                                     self.game_session)

                                            # send voted description
                                            if self.is_using_tts and self.is_tts_voting:
                                                self.socketConnector.send(description, "message")

                                        else:
                                            self.sendMessage("You already voted for this description.")

                                    else:  # des_id not in des_list
                                        total_users = []  # flatten to 1 array of all users voted for all descriptions
                                        for ds in self.audiences.get_voters().values():
                                            total_users = total_users + [u for sublist in ds.values() for u in sublist]

                                        if user not in total_users:
                                            users.append(user)
                                            self.utils.writeVoteData(user, img_id, description, artManager.get_images(),
                                                                     self.game_session)

                                            # send voted description
                                            if self.is_using_tts and self.is_tts_voting:
                                                self.socketConnector.send(description, "message")

                                        else:
                                            self.sendMessage("You cannot vote for more than one description.")

                                    if users:  # store when users array not empty
                                        des_list[des_id] = users
                                        self.audiences.get_voters()[img_id] = des_list
                            else:
                                self.sendMessage(
                                    "There is no typed description id shown on the list. Please try again.")
                        else:
                            self.sendMessage(
                                "Sorry you cannot vote since you are a describer. Wait for the next round if you wish.")
                        break
                    elif (not self.isStopDescribingSignal) and self.isStopVotingSignal and message.startswith("#"):
                        self.sendMessage("Voting session is over. Please wait for its turn.")
                        break
                    elif self.isStopDescribingSignal and not self.isStopVotingSignal and len(
                            message.split(":")) == 2 and message.split(":")[0].isdigit():
                        self.sendMessage("You cannot describe picture in voting session.")
                        break
                    else:
                        # Replace all non-alphanumeric non-# characters in a string.
                        message = re.sub('[^0-9a-zA-Z#! ]+', '', message)
                        if message == "":
                            break
                        else:
                            # self.utils.writeFile(user,message)
                            break
                except:
                    self.sendMessage("Some characters are not supported. Please try again.")