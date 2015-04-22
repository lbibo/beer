#Import database as list of tuples
def create_beer_dictionary():

    file = open('database.txt','r').readlines()

    beer_dictionary = {}

    for line in file:
        entry = line.split('\t')
        beer_dictionary[entry[0]] = [entry[1], entry[2], entry[3], entry[4]]

    return beer_dictionary

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

#recommend new beer from database using user stats
def new_beer(uas, search_exclude, beer_dictionary):
    uas_ibu = uas[0]
    uas_abv = uas[1]
    ibu_variance = 0
    abv_variance = 0

    """create an empty list in case multiple results are found"""
    new_recommendation_list = []

    #continue increasing variance for ibu and abv until a match is found
    while len(new_recommendation_list) == 0:
        ibu_variance += 1
        abv_variance += 0.5

        #If the ibu variance has hit 50, there are no more beers to choose from.
        if ibu_variance == 50:
            break

        """Search for beers in dictionary, tests against current variance (range) variable.
        Increases variance if no beer is found within current range.
        Currently only works if the database has a number for both ibu and abv.
        Doesn't test for color."""
        for key, beer in beer_dictionary.iteritems():
            add_beer = True

            try:
                beer_ibu = float(beer[1])
                beer_abv = float(beer[2])

                if (beer_ibu >= (uas_ibu - ibu_variance)) and (beer_ibu <= (uas_ibu + ibu_variance)):
                    add_beer = True

                    if (beer_abv >= (uas_abv - abv_variance)) and (beer_abv <= (uas_abv + abv_variance)):
                        add_beer = True

                        for SE_key, code in search_exclude.iteritems():

                            if (int(SE_key) == int(key)):
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
        return False
