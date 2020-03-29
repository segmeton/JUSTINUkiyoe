import csv, requests, random, datetime, os, json
import pandas as pd

class Utils:
    def __init__(self):
        self.url_bg_img1 = ""
        self.url_bg_img2 = ""
        self.url_bg_img3 = ""
    
    def retrieveImages(self):
        # df = pd.read_csv('data_preparing/Data/cleaned-ukiyo-e-content-remove-nan-keyword-filtered.csv')
        df = pd.read_csv('data_preparing/Data/cleaned-ukiyo-e-content-remove-nan-keyword-filtered.csv')
        qualified_images = self.load_qualified_images()
        df = df[df.Source.apply(lambda url: os.path.basename(url) not in qualified_images)]
        df = df[~df['Keywords'].str.contains("sex")]
        
        n = 3
        if len(df) < 3:
            n = len(df)
        
        df = df.sample(n=n)
        urls = list(df.Source)

        print(urls)
        bg_imgs = []
        for i in range(n):
            bg_imgs.append(os.path.basename(urls[i]))

        # return (bg_img1, bg_img2, bg_img3)
        return bg_imgs
    
    def writeFileVote(self, user, message):
        ### open bg_vote.txt and append
        f = open("../AngryICE/bg_vote.txt", "a")
        ### write user name and message 
        f.write(user+":"+message+"\n")
    

    def writeFile(self, user, message):
        ### open chat.txt and append
        f = open("../AngryICE/chat.txt", "a")
        ### write user name and message 
        f.write(user+":"+message+"\n")
        
    def writeFile2(self, user, message):
        ### open chat.txt and append
        f = open("../AngryICE2/chat.txt", "a")
        ### write user name and message 
        f.write(user+":"+message+"\n")
    
    def writeVoteData(self, user, img_id, description, images, game_session):

        f = open("vote_log.txt", "a")
        print("images in writevotedata " + json.dumps(images))
        print("user in writeVoteData " + str(user))
        print("description in writeVoteData " + str(description))
        print("game session in writeVoteData " + str(game_session))
        picname = images.get(img_id)
        print("img_id in writeVoteData " + str(img_id))
        print("pic name in writeVoteData " + str(picname))
        f.write(str(game_session) + "," + user + "," + picname + "," + description+"\n")

    def writeVoteAndTagsData(self, user, message, images, game_session):

        f = open("votetag_log.txt", "a")
        lines = message.split(":")
        img_id = lines[0]
        description = lines[1]
        if img_id in images:
            picname = images.get(img_id)
            f.write(str(game_session) + "," + img_id + "," + user + "," + picname + "," + description+"\n")
    
    def writeFileLog(self, user, message):
        f = open("chat_log.txt", "a")
        f.write("Time="+str(datetime.datetime.now())+" Name="+user+" Message="+message+"\n")

    def get_last_game_session(self):
        game_session = 1
        try:
            f = open('votetag_log.txt', 'r')
            lines = f.read().rstrip('\n').splitlines()
            last_line = lines[-1]
            game_session = int(last_line.split(",")[0])
        except:
            pass
        
        return game_session

    def store_winning_users(self, winning_users):
        f = open("Data/winning_users_log.txt", "a")
        for userInfo in winning_users:
            f.write(userInfo + "\n")

    def get_old_participants_for_used_images(self, images, win_des_candidate):
        old_participants = {} ### {u8: {'imgs': {img1: {d1: "description"}, img2: {d6: "description"}}, 'role':'former_voter'}, 
                        ###  u9:...}
        tmp = self.get_img_descriptions_by_pythia(images)
        descriptions = tmp[0]

        des_id = tmp[1]

        used_images = {} # initialize the status of images, used or new
        for img in images:
            used_images[img] = 0
        
        try:
            f = open('Data/winning_users_log.txt', 'r')
            lines = f.read().splitlines()
            
            for line in lines:
                
                components = line.split("||")
                img_id = next((id for id, img in images.items() if img == components[2]), None)
                
                if img_id is not None:
                    used_images[img_id] = 1

                    if components[3] in win_des_candidate:
                        metadata = []
                        if components[1] in old_participants:
                            metadata = old_participants.get(components[1])
                        metadata.append({"des": components[3], "img_id": img_id, "other_role": components[4]})
                        old_participants[components[1]] = metadata
                        if components[4] == "describer":
                            descriptions[str(des_id)] = (img_id, components[3], 'human')
                            des_id += 1
            
        except:
            print("Cannot read file winning_users_log.txt")
        
        print('Initial des_id ', des_id)
        print('Initial descriptions ', json.dumps(descriptions))
        print('Initial old_participants ', json.dumps(old_participants))

        return (old_participants, des_id, descriptions, used_images)

    def get_img_descriptions_by_pythia(self, images):
        df = pd.read_csv("data_preparing/Data/Pythia/uki-captions-pythia.csv")
        descriptions = {}

        des_id = 1
        for id, img in images.items():
            try:
                descriptions[str(des_id)] = (id, df.loc[df['name'] == img]['caption_1'].values[0], 'AI')
                descriptions[str(des_id + 1)] = (id, df.loc[df['name'] == img]['caption_2'].values[0], 'AI')
                des_id += 2
            except:
                print("error ")

        return (descriptions, des_id)

    def store_participants_info(self, participants):
        with open('Data/participants_info.json', 'w') as outfile:
            json.dump(participants, outfile)
    
    def load_participants_info(self):
        participants = {}
        try:
            with open('Data/participants_info.json') as json_file:
                participants = json.load(json_file)
        except:
            pass
        return participants
    
    def load_winning_des(self):
        win_des = {}
        try:
            with open('Data/winning_description_candidate.json') as json_file:
                win_des = json.load(json_file)
        except:
            pass
        return win_des
    
    def store_winning_des(self, win_des):
        with open('Data/winning_description_candidate.json', 'w') as outfile:
            json.dump(win_des, outfile)

    def store_good_winning_des(self, win_des):
        f = open("Data/good_winning_descriptions.txt", "a")
        for d, value in win_des.items():
            f.write(d + "||" + str(value[0].get('score')) + "||" + str(value[0].get('used_time')) + "||" + value[1] + "\n")
    
    def load_qualified_images(self):
        images = []
        try:
            f = open('Data/good_winning_descriptions.txt', 'r')
            lines = f.read().splitlines()
            for line in lines:
                images.append(line.split('||')[3])
        except:
            print('cannot open file good_winning_descriptions.txt')
        return images
    
    def store_bad_winning_des(self, win_des):
        f = open("Data/bad_winning_descriptions.txt", "a")
        for d, value in win_des.items():
            f.write(d + "||" + str(value.get('score')) + "||" + str(value.get('used_time')) + "\n")

    def get_top_participants(self, participants):
        top_participants = None
        if bool(participants):
            top_participants = sorted(participants.items(), key=lambda x: x[1].get("total_score"), reverse=True)
        
        return top_participants

    def store_ranking(self):
        participants = self.load_participants_info()
        participants = self.get_top_participants(participants)

        users = []
        scores = []
        if participants is not None:
            for participant in participants:
                users.append(participant[0])
                score = participant[1].get('total_score')

                if participant[1].get('total_score') < 0:
                    score = 0
                
                scores.append(int(round(score*10)))

            result = {'user': users, 'score': scores}
            resultdf = pd.DataFrame(result, columns= ['user', 'score'])
            
            resultdf.to_csv('Data/scoring_board.csv', index=None, header=True)