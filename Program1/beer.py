#Import database as list of tuples
def create_dictionary():
    file = open('database2.txt','r').readlines()
    dictionary = {}
    for line in file:
        entry = line.split(',')
        dictionary[entry[0]] = [entry[1], entry[2], entry[3], entry[4]]
    return dictionary

#find the beer the user searched for
def find_input_beer(x, database):
    beer_selection_list = []
    file = open(database, 'r')
    file.seek(0, 0)
    for line in file:
        name = (line.split(','))[0]
        if input.lower() in name.lower():
            beer_selection_list.append(name)
    file.close()

#strip stats from entries in user file and return list of beer names
def statstrip(user_beers):
    new_list = []
    for entry in user_beers:
        name = (str(entry)).split(',')
        new_list.append(name[0])
    return new_list

#create a list with average stats for user 'liked' beers
def user_average(search_exclude, dictionary):
    count = 0
    ibu = 0
    abv = 0
    """[0] = ibu, [1] = abv, [2] = color (not working yet)"""
    user_average_stats = [0, 0]
    for key, code in search_exclude.iteritems():
        """a code of 1 means it is a beer the user has liked."""
        if code == 1:
            try:
                current_key = dictionary[key]
                user_average_stats[0] += float(current_key[1])
                user_average_stats[1] += float(current_key[2])
                count += 1
            except:
                continue
    try:
        user_average_stats[0] = user_average_stats[0] / count
    except:
        user_average_stats[0] = "Error 10"
    try:
        user_average_stats[1] = user_average_stats[1] / count
    except:
        user_average_stats[1] = "Error 10"

    ### commented out until we find a way to add color coding ###

    #try:
    #    user_average.append(color / count)
    #except:
    #    user_average.append("?\n")
    return user_average_stats

#Returns a dictionary of liked/disliked beers from user file
def pull_userfile_beers(search_exclude, username_directory, Username):
    file = open(username_directory + Username + '.txt', 'r')
    linecount = 0
    for line in file:
        splitline = line.split(',')
        splitline[-1] = splitline[-1].rstrip()
        if linecount == 0:
            for key in splitline:
                if key == 'LIKED:':
                    continue
                elif key == 'DISLIKED:':
                    linecount += 1
                    break
                elif key == '\n':
                    continue
                else:
                    search_exclude[key] = 1
        elif linecount == 1:
            for key in splitline:
                if key == 'LIKED:':
                    continue
                elif key == 'DISLIKED:':
                    continue
                elif key == '\n':
                    continue
                else:
                    search_exclude[key] = 2
        linecount += 1
    return search_exclude

#recommend new beer from database using user stats
def new_beer(uas, search_exclude, dictionary):
    uas_ibu = uas[0]
    uas_abv = uas[1]
    ibu_variance = 0
    abv_variance = 0
    """create an empty list in case multiple results are found"""
    new_recommendation_list = []
    #continue increasing variance for ibu and abv until a match is found
    while len(new_recommendation_list) == 0:
        ibu_variance += 5
        abv_variance += 2
        add_beer = True
        if ibu_variance == 50:
            break
        """Search for beers in dictionary, tests against current variance (range) variable.
        Increases variance if no beer is found within current range.
        Currently only works if the database has a number for both ibu and abv.
        Doesn't test for color."""
        for key, beer in dictionary.iteritems():
            try:
                beer_ibu = float(beer[1])
                beer_abv = float(beer[2])
                if (beer_ibu >= (uas_ibu - ibu_variance)) and (beer_ibu <= (uas_ibu + ibu_variance)):
                    if (beer_abv >= (uas_abv - abv_variance)) and (beer_abv <= (uas_abv + abv_variance)):
                        for SE_key, code in search_exclude.iteritems():
                            if (int(SE_key) == int(key)) and ((code == 2) or (code == 0)):
                                add_beer = False
                    else:
                        add_beer = False
                else:
                    add_beer = False
                if add_beer is True:
                    new_recommendation_list.append(key)
            except:
                continue
    try:
        return new_recommendation_list
    except:
        return "No beer found."
    return

#create string from user file
def pull_user_string(Userfile):
    newline = ""
    Userfile.seek(0, 0)
    for line in Userfile:
        newline = str(line) + str(newline)
    return newline

#update user file
def update_userfile(search_exclude, username_directory, username):
    """Add new beer to user file (create list of keys coded to 'liked:' then join into new string)"""
    newstring_list = []
    for key, code in search_exclude.iteritems():
        if code == 1:
            newstring_list.append(key)
    newstring_liked = ','.join(newstring_list)
    newstring_liked = 'LIKED:,' + newstring_liked
    """Add new beer to user file (create list of keys coded to 'disliked:' then join into new string)"""
    newstring_list = []
    for key, code in search_exclude.iteritems():
        if code == 2:
            newstring_list.append(key)
    newstring_disliked = ','.join(newstring_list)
    newstring_disliked = 'DISLIKED:,' + newstring_disliked
    masterstring = newstring_liked + '\n' + newstring_disliked
    file = open(username_directory + username + '.txt', 'w')
    file.write(masterstring)
    file.close()
    return