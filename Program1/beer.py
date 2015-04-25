#Import database as list of tuples
def create_beer_dictionary():

    file = open('database.txt','r').readlines()

    beer_dictionary = {}

    for line in file:
        entry = line.split('\t')
        beer_dictionary[entry[0]] = [entry[1], entry[2], entry[3], entry[4], entry [5]]

    return beer_dictionary

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

        #If the ibu variance has hit 50, there are no more beers to choose from.
        if ibu_variance == 50:
            break

        """Search for beers in dictionary, tests against current variance (range) variable.
        Increases variance if no beer is found within current range.
        Currently only works if the database has a number for both ibu and abv.
        Doesn't test for color."""
        for key, beer in beer_dictionary.iteritems():
            #only return American beers with accurate IBUs and ABVs - 
            if (float(beer[1]) == -1.0) or (float(beer[2]) == -1.0) or (not ('USA' in str(beer[4]))):
                continue
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

        #increase variance variables after each loop so the first loop can run without any variance
        ibu_variance += 1
        abv_variance += 0.5

    try:
        return new_recommendation_list
    except:
        return False
