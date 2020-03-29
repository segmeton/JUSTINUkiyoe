import Utils, json

class Audiences:

    def __init__(self, images):
        self.utils = Utils.Utils()
        self.voters = {}
        
        self.win_des = self.utils.load_winning_des()
        tmp = self.utils.get_old_participants_for_used_images(images, self.win_des)
        self.old_participants = tmp[0]
        self.init_des_id = tmp[1]
        self.descriptions = tmp[2]
        self.used_images = tmp[3]

        ## {u8: {'imgs': {img1: {d1: "description"}, img2: {d6: "description"}}, 'role':'former_voter'}, 
        ###  u9:...}
        self.describers = {}

        self.participants = self.utils.load_participants_info()
        
        # print('participants ' + str(json.dumps(self.participants)))
    
    def set_voters(self, voters):
        self.voters = voters
    
    def get_voters(self):
        return self.voters
    
    def set_describers(self, describers):
        self.describers = describers
    
    def get_describers(self):
        return self.describers

    def get_old_participants(self):
        return self.old_participants
    
    def get_win_des(self):
        return self.win_des
    
    def get_top_participants(self):
        top_participants = None
        if bool(self.participants):
            top_participants = sorted(self.participants.items(), key=lambda x: x[1].get("total_score"), reverse=True)
            if len(self.participants) >= 4:
                top_participants = top_participants[:4]
        
        return top_participants
    

    def refresh_players(self, images):
        # self.win_des = self.utils.load_winning_des()
        tmp = self.utils.get_old_participants_for_used_images(images, self.win_des)
        self.old_participants = tmp[0]
        self.init_des_id = tmp[1]
        self.descriptions = tmp[2]
        self.used_images = tmp[3]

        self.describers = {}
        self.voters = {}
    
    def get_descriptions(self):
        return self.descriptions
    
    def get_used_images(self):
        return self.used_images
    
    def get_init_des_id(self):
        return self.init_des_id

    def get_winning_des_id_foreach_img(self, img_id):
        if img_id in self.voters:
            return sorted(self.voters.get(img_id).items(), key=lambda x: len(x[1]))[-1][0]
        else:
            return None

    def get_winning_des_list(self, images):
        w_des_list = []
        for img_id in images:
            winning_des_id = self.get_winning_des_id_foreach_img(img_id)
            if winning_des_id is not None:
                w_des_list.append(winning_des_id)
        
        return w_des_list
    
    def get_participants_results(self, images, game_session, descriptions):
        winning_users = []

        # if bool(self.voters): # do all this when voters do something, means there is some winning description
        winning_des_list = self.get_winning_des_list(images)
        print('winning description list ', winning_des_list)

        total_votes_img = {} # calculate total votes on each image
        for img_id in images: # Initialize 0 vote score for each image
            total_votes_img[img_id] = 0
        
        for img_id, des_list in self.voters.items():
            total_votes = 0
            for _, u_list in des_list.items():
                total_votes += len(u_list)
            total_votes_img[img_id] = total_votes
        
        num_votes = 0
        for img_id, des_list in self.voters.items(): ## calculate or update scores for all voters who voted winning descriptions this game session
            for d, u_list in des_list.items():
                num_votes += len(u_list)
                if d in winning_des_list:
                    for u in u_list:
                        old_score = 0
                        prop = {}
                        if u in self.participants:
                            prop = self.participants.get(u)
                            old_score = prop.get("total_score")
                        
                        added_score = (1/len(images))*len(u_list)/total_votes_img.get(img_id)
                        prop[game_session] = {"role": "voter", "added_score": added_score}
                        prop["total_score"] = old_score + added_score # normalize

                        self.participants[u] = prop
                        winning_users.append(str(game_session) + "||" + u + "||" + images.get(img_id) \
                             + "||" + descriptions.get(d)[1] + "||" + "voter")
                        # self.utils.store_winning_user(u, game_session, images.get(img_id), descriptions.get(d)[1], "voter")
        
        print("describers in get participants result " + str(json.dumps(self.describers)))
        for u, imgs in self.describers.items(): ## calculate or update scores for all describers who created winning descriptions this game session
            new_score = 0
            added_score = 0
            prop = {}
            
            print("imgs in get results " + json.dumps(imgs))

            for img_id, d in imgs.items():
                d_id = next(iter(d))
                print('d_id in calculating score for describers ', d_id)
                if d_id in winning_des_list:
                    u_list = self.voters.get(img_id).get(d_id)
                    added_score += len(u_list)/total_votes_img.get(img_id)
                    
                    description = descriptions.get(d_id)[1]
                    winning_users.append(str(game_session) + "||" + u + "||" + images.get(img_id) \
                             + "||" + description + "||" + "describer")
                    # self.utils.store_winning_user(u, game_session, images.get(img_id), description, "describer")
                    
                    des_score = 0
                    used_time = 1

                    print('description ', description , ' got scored') 
                    des_score += len(u_list)/total_votes_img.get(img_id) # add score for description (description here are all new)
                    self.win_des[description] = {'score': des_score, 'used_time': used_time}
                    
            old_score = 0 
            if u in self.participants:
                prop = self.participants.get(u)
                old_score = prop.get("total_score")
            
            if added_score > 0:
                new_score = old_score + added_score/len(images)
                prop[game_session] = {"role": "describer", "added_score": added_score/len(images)}
                prop["total_score"] = new_score

                self.participants[u] = prop
        
        if num_votes > len(images): # only apply penalty when total votes in current round > number of images shown by system.
        # if num_votes > 0: # for testing because currently only 2 voters in total, unfortunately
            candidate_des = []
            excluded_players = [] # list of old players who are ignored by penalty mechanism 
            for u, value in self.old_participants.items():
                for metadata in value:
                    description = metadata.get("des")
                    if description in self.win_des:
                        if u in self.describers:
                            imgs = self.describers.get(u)
                            if metadata.get('img_id') in imgs:
                                d = imgs.get(metadata.get('img_id'))
                                d_id = next(iter(d))
                                if d_id in winning_des_list:  # if this user created new description for the image and it wins, user will not get penalty
                                    print('new des_id ', d_id, ' of description ', description ,' for the image and it wins, user', u, \
                                        ' will not get penalty')
                                    excluded_players.append(u)
                        
                        print("----------------user ", u, " might get penalty by ", description)
                        desID = next((id for id, value in self.descriptions.items() \
                            if value[1] == description), None)
                        
                        print('des_id in old_participant ', desID)
                        if desID is not None:
                            print('winning_des list ', winning_des_list)
                            if desID not in winning_des_list:
                                uj = total_votes_img.get(metadata.get('img_id'))/sum(total_votes_img.values()) #popularity of image j at current round
                                vsj = 0
                                if metadata.get('img_id') in self.voters:
                                    des_list = self.voters.get(metadata.get('img_id'))
                                    if desID in des_list:
                                        u_list = des_list.get(desID)
                                        vsj = len(u_list)
                                vij_star = 1
                                win_des_id = self.get_winning_des_id_foreach_img(metadata.get('img_id'))
                                if win_des_id is not None:
                                    vij_star = len(self.voters.get(metadata.get('img_id')).get(win_des_id))
                                
                                penalty_score = uj*(1 - vsj/vij_star)
                                total_score = 0
                                role = metadata.get("other_role")
                                added_score = -penalty_score
                                prop = {}
                                if u not in excluded_players: 
                                    if u in self.participants:
                                        prop = self.participants.get(u)
                                        total_score = prop.get("total_score")
                                        total_score -= penalty_score
                                        if game_session in prop:
                                            added_score = prop.get(game_session).get("added_score") - penalty_score
                                            role = prop.get(game_session).get("role")
                                    prop[game_session] = {"role": role, "added_score": added_score}
                                    prop["total_score"] = total_score
                                    self.participants[u] = prop

                                if description not in candidate_des: # set score only one time
                                    print('description ', description, ' got penalty')
                                    score = self.win_des.get(description).get('score')
                                    print('score before penalty', score)
                                    score -= penalty_score
                                    print('score after penalty', score)
                                    used = self.win_des.get(description).get('used_time') + 1
                                    self.win_des[description] = {'score': score, 'used_time': used}

                                    candidate_des.append(description)

                            else:
                                if description not in candidate_des: # set score only one time
                                    # score for those description win again
                                    u_list = self.voters.get(metadata.get('img_id')).get(desID)
                                    
                                    des_score = self.win_des.get(description).get('score') + len(u_list)/total_votes_img.get(metadata.get('img_id')) # add score for description
                                    used_time = self.win_des.get(description).get('used_time') + 1
                                    
                                    print('description ', description , ' got scored after winning again')
                                    self.win_des[description] = {'score': des_score, 'used_time': used_time}

                                    candidate_des.append(description)
        if winning_users:
            self.utils.store_winning_users(winning_users)

        return self.participants