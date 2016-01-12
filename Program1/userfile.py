class Userfile:
    def __init__(self, username, user_dict = {}):
        self.username = username.upper()
        self.user_dict = user_dict

    #sets the active user name
    def set_username(self, user_input):
        self.username = user_input.upper()

    #returns the active user name
    def get_username(self):
        return self.username

    #returns the user dictionary
    def get_dict(self):
        return self.user_dict

    #creates the user file on initial creation
    def create_user(self, username_directory):
        file = open(username_directory + self.username + '.txt', 'w')
        file.close()

    #Populates user beer dictionary from keys saved in user file
    def login(self, username_directory):
        file = open(username_directory + self.username + '.txt', 'r')

        linecount = 0

        for line in file:
            splitline = line.split(',')
            splitline[-1] = splitline[-1].rstrip()

            if linecount == 0:

                for line_item in splitline:

                    if line_item == 'LIKED:':
                        continue
                    elif line_item == 'DISLIKED:':
                        linecount += 1
                        break
                    elif line_item == '\n':
                        continue
                    else:
                        self.user_dict[line_item] = 1

            elif linecount == 1:

                for line_item in splitline:

                    if line_item == 'LIKED:':
                        continue
                    elif line_item == 'DISLIKED:':
                        continue
                    elif line_item == '\n':
                        continue
                    else:
                        self.user_dict[line_item] = 2

            linecount += 1

        file.close()

    #add a beer key and corresponding liked/disliked code to the user beer dictionary
    def add_beer(self, key, code):
        self.user_dict[key] = code

    #save updated user beer dicitonary to user file
    def update_userfile(self, username_directory):
        liked_string = 'LIKED:'
        disliked_string = 'DISLIKED:'
        to_try_string = 'TO TRY:'

        dictionary = self.user_dict

        for key, code in dictionary.items():

            if code == 1:
                liked_string += ',' + str(key)
            elif code == 2:
                disliked_string += ',' + str(key)
            elif code == 3:
                to_try_string += ',' + str(key)

        master_string = '%s\n%s\n%s' % (liked_string, disliked_string, to_try_string)

        file = open(username_directory + self.username + '.txt', 'w')
        file.write(master_string)
        file.close()

    #returns a list of keys for beers user has liked
    def get_liked(self):
        liked_list = []
        
        dictionary = self.user_dict

        for key, code in dictionary.items():

            if code == 1:
                liked_list.append(key)

        return liked_list

    #returns a list of keys for beers user has disliked
    def get_disliked(self):
        disliked_list = []
        
        dictionary = self.user_dict

        for key, code in dictionary.items():

            if code == 2:
                disliked_list.append(key)

        return disliked_list
    
    #returns a list of keys for beers user has liked
    def get_to_try(self):
        to_try_list = []
        
        dictionary = self.user_dict

        for key, code in dictionary.items():

            if code == 3:
                to_try_list.append(key)

        return to_try_list

    #returns a list of average stats for beers user has liked
    def get_user_average_stats(self):
        stats_total_list = [0, 0]
        count = 0
        
        dictionary = self.user_dict

        for key, code in dictionary.items():
            temp_list = []

            #makes sure the user liked the beer
            if code == 1:
                beer_entry = beer_dictionary[key]
                count += 1

                temp_list.append(beer_entry[1])
                temp_list.append(beer_entry[2])
                #comment out unil color is implemented
                #temp_list.append(beer_entry[3])
                stats_total_list[0] += float(temp_list[0])
                stats_total_list[1] += float(temp_list[1])

        user_average = [0, 0]
        user_average[0] = stats_total_list[0] / count
        user_average[1] = stats_total_list[1] / count

        return user_average