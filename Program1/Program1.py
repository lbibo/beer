from Tkinter import *
import tkMessageBox
import os
import csv
import random

import beer
import programfuncs

###classes

#User file class
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

#gets the current file path
current_directory = os.getcwd()
#gets the path to the usernames
username_directory = current_directory + '/Users/'
#lists all current users
Username_list = os.listdir(username_directory)
#create variable that points to location of database
database = current_directory + '/database.txt'
#create a dictionary of keys/beers
beer_dictionary = beer.create_beer_dictionary()
#create string to add to beginning of recommend string to reflect dislike of previous recommendation
disliked_previous = ""
#set global active settings
login_screen_active = True
has_profile = False
Username = None
#set sizes
WIDTH = 600
HEIGHT = 600
#set background color to black
BGCOLOR = '#000000'
#set entry box font color to dark gray
entfontcolor = '#444444'
#set console text color to yellow
consolecolor = '#FFFF00'
#set button colors to dark yellow
butcolor = '#AAAA00'
#set entry box color to white
entcolor = '#FFFFFF'
#set console font to courier
consolefont = 'calibri'

#create main app
beerapp = Tk()
beerapp.resizable(width = FALSE, height = FALSE)
beerapp.title("Beer")
beerapp.configure(background = BGCOLOR)
beerapp.columnconfigure(0, weight = 1)
beerapp.columnconfigure(1, weight = 1)
beerapp.columnconfigure(2, weight = 1)
beerapp.rowconfigure(0, weight = 1)
beerapp.rowconfigure(1, weight = 1)
beerapp.rowconfigure(2, weight = 1)

###Create Sub-Frames###

#create login screen
login_buttons = Frame(beerapp, background = BGCOLOR, padx = 5)
login_buttons.grid(row = 1, column = 0)
login_buttons.columnconfigure(0, minsize = int(WIDTH / 3), weight = 0)
login_buttons.rowconfigure(0, minsize = int(HEIGHT / 3), weight = 0)
login_buttons.rowconfigure(1, minsize = int(HEIGHT / 3), weight = 0)

#create user input frame
user_input_frame = Frame(beerapp, background = BGCOLOR, padx = 5)
user_input_frame.grid(row = 1, column = 0)
user_input_frame.columnconfigure(0, minsize = int(WIDTH / 3), weight = 0)
user_input_frame.rowconfigure(0, minsize = int(HEIGHT / 3), weight = 0)
user_input_frame.rowconfigure(1, minsize = int(HEIGHT / 3), weight = 0)

#create console output frame
console_output_frame = Frame(beerapp, background = BGCOLOR, padx = 15, pady = 15)
console_output_frame.grid(row = 1, rowspan = 2, column = 1, columnspan = 2)
console_output_frame.columnconfigure(0, minsize = int((WIDTH / 3) * 2), weight = 0)
console_output_frame.rowconfigure(0, minsize = int((HEIGHT / 3) * 2), weight = 0)

###Functions###

#function to print to console
def print_to_console(output):

    try:
        console_output.set(str(output))
    except:
        console_output.set("Console output error.")

    return

#Log in as existing user via "Enter" key
def existingUser_login(event):
    global User

    x = UserStr.get()
    User = Userfile(x)

    if programfuncs.check_availableUser(User.get_username(), Username_list) is False:
        """read beers from user file into search exclusion list"""
        User.login(username_directory)

        """Set global active settings"""
        login_screen_active = False
        has_profile = True

        """remove login buttons, update login information"""
        new_recommend_button.grid(row = 0, column = 0, sticky = 'w')
        show_user_button.grid(row = 3, column = 2, sticky = 'e')
        new_entry_button.grid(row = 3, column = 0, sticky = 'w')
        login_buttons.grid_forget()
        print_to_console("Logged in.")

        """"Set login header"""
        UserLabelStr.set('Logged in as ' + User.get_username())
    else:
        """Pop up "No User Found." message box."""
        ask_new_user = tkMessageBox.askquestion("Username not found.", "Username not found. \n Create one with the name %s?" % User.get_username())

        if ask_new_user == 'yes':
            """Create user file"""
            User.create_user(username_directory)

            """force user to pick initial 'liked' beer"""
            enable_new_beer_entry()

            """update login information"""
            UserLabelStr.set('Logged in as ' + User.get_username())
            login_screen_active = False
            login_buttons.grid_forget()
            new_entry_button.grid(row = 3, column = 0, sticky = 'w')

    return

#Log in as existing user via button
def existingUser_loginbutton():
    global User

    x = UserStr.get()
    User = Userfile(x)

    if programfuncs.check_availableUser(User.get_username(), Username_list) is False:
        """read beers from user file into search exclusion list"""
        User.login(username_directory)

        """Set global active settings"""
        login_screen_active = False
        has_profile = True

        """remove login buttons, update login information"""
        new_recommend_button.grid(row = 0, column = 0, sticky = 'w')
        show_user_button.grid(row = 3, column = 2, sticky = 'e')
        new_entry_button.grid(row = 3, column = 0, sticky = 'w')
        login_buttons.grid_forget()
        print_to_console("Logged in.")

        """"Set login header"""
        UserLabelStr.set('Logged in as ' + User.get_username())
    else:
        """Pop up "No User Found." message box."""
        ask_new_user = tkMessageBox.askquestion("Username not found.", "Username not found. \n Create one with the name %s?" % User.get_username())

        if ask_new_user == 'yes':
            """Create user file"""
            User.create_user(username_directory)

            """force user to pick initial 'liked' beer"""
            enable_new_beer_entry()

            """update login information"""
            UserLabelStr.set('Logged in as ' + User.get_username())
            login_screen_active = False
            login_buttons.grid_forget()
            new_entry_button.grid(row = 3, column = 0, sticky = 'w')

    return

#Enable user manual 'liked' beer entry
def enable_new_beer_entry():
    global User_input_entry, input_button, yes_button, no_button

    """Reset input controls"""
    try:
        yes_button.grid_forget()
        no_button.grid_forget()
        user_input_entry.grid_forget()
        input_button.grid_forget()
    except:
        pass

    """Create user input box"""
    User_input_entry.grid(row = 0, sticky = W+S+E)
    User_input_entry.focus_set()
    programfuncs.bind_enter(beerapp, input_enter)

    """Create user input button"""
    input_button.grid(row = 1, sticky = W+N+E)
    print_to_console("Give me the name of a good beer.  Spelling counts.")

    return

#button to send data from input to program/console
def input_button_click():
    global found_beer, yes_button, no_button, found_key

    """get user's input string"""
    input = User_input.get()
    User_input_entry.grid_forget()
    input_button.grid_forget()

    """find beer in database containing user's input string"""
    beer_selection_list = []
    for dictkey, beer_data in beer_dictionary.items():
        name = beer_data[0].lower()
        lower_input = input.lower()

        if str(lower_input) in str(name):
            beer_selection_list.append([dictkey, 0])

            for userkey, code in User.get_dict().items():
                if str(userkey) == str(dictkey):
                    beer_selection_list.remove([dictkey, 0])

    """if there is at lease one beer in the returned list, pick the first one.  Otherwise, try again."""
    if len(beer_selection_list) > 0:
        amount_found = len(beer_selection_list) - 1
        found_key = (beer_selection_list[0])[0]
        found_beer = beer_dictionary[found_key]
        console_response = """Found the following beer:
        
%s

Is this correct?""" % (str(found_beer[0]).upper())
        print_to_console(console_response)
        enable_beer_found_buttons()
    else:
        print_to_console("Beer not found.  Please try again.")
        enable_new_beer_entry()

    """reset 'disliked_previous' modifier"""
    disliked_previous = ''

    return

#create function for 'Enter/Return' key to call, since it requires an 'event' parameter
def input_enter(event):
    global found_beer, yes_button, no_button, found_key

    """get user's input string"""
    input = User_input.get()
    User_input_entry.grid_forget()
    input_button.grid_forget()

    """find beer in database containing user's input string"""
    beer_selection_list = []
    for dictkey, beer_data in beer_dictionary.items():
        name = beer_data[0].lower()
        lower_input = input.lower()

        if str(lower_input) in str(name):
            beer_selection_list.append([dictkey, 0])

            for userkey, code in User.get_dict().items():
                if str(userkey) == str(dictkey):
                    beer_selection_list.remove([dictkey, 0])

    """if there is at lease one beer in the returned list, pick the first one.  Otherwise, try again."""
    if len(beer_selection_list) > 0:
        amount_found = len(beer_selection_list) - 1
        found_key = (beer_selection_list[0])[0]
        found_beer = beer_dictionary[found_key]
        console_response = """Found the following beer:
        
%s

Is this correct?""" % (str(found_beer[0]).upper())
        print_to_console(console_response)
        enable_beer_found_buttons()
    else:
        print_to_console("Beer not found.  Please try again.")

    """reset 'disliked_previous' modifier"""
    disliked_previous = ''

    return


#Create yes/no buttons for manual user entry
def enable_beer_found_buttons():
    global yes_button, no_button

    """create "Yes" button"""
    yes_button.grid(row = 0, sticky = W+S+E)
    yes_button.configure(command = lambda: accept_beer_found(True))

    """create "No" button"""
    no_button.grid(row = 1, sticky = W+N+E)
    no_button.configure(command = lambda: accept_beer_found(False))

    return

#Accepts entry, adds to user file
def accept_beer_found(response):
    global yes_button, no_button, found_key, has_profile

    if response is True:
        #try:
        User.add_beer(found_key, 1)
        """update user file"""
        User.update_userfile(username_directory)
        """Clear yes/no buttons"""
        yes_button.grid_forget()
        no_button.grid_forget()
        print_to_console("Beer added to user file.")
        if has_profile is False:
            has_profile = True
            new_recommend_button.grid(row = 0, column = 0, sticky = 'w')
            show_user_button.grid(row = 3, column = 2, sticky = 'e')
        #except:
        #    print_to_console("Error 7")
    elif response is False:
        try:
            yes_button.grid_forget()
            no_button.grid_forget()
            enable_new_beer_entry()
            User.add_beer(found_key, 0)
        except:
            pass
    else:
        print_to_console("Error 6")

    return

#Recommend new beer
def recommend_new():
    global Userfile, yes_button, no_button, recommend_beer, disliked_previous
    
    """Reset input controls"""
    try:
        yes_button.grid_forget()
        no_button.grid_forget()
        user_input_entry.grid_forget()
        input_button.grid_forget()
    except:
        pass

    enable_recommend_buttons1()
    user_average_stats = User.get_user_average_stats()    

    #try:
    """Get a list of beers within the smallest range that meets all user criteria"""
    new_recommendation_list = beer.new_beer(user_average_stats, User.get_dict(), beer_dictionary)

    """Pick a random beer from the returned list"""
    if len(new_recommendation_list) == 0:
        ### No new beer found.  This should never happen unless the variation variables are not increasing properly
        yes_button.grid_forget()
        no_button.grid_forget()
        recommend_string = "Beer search error: no beers found."

    elif len(new_recommendation_list) == 1:
        enable_recommend_buttons1()
        random_beer = 0
        recommend_beer = new_recommendation_list[random_beer]
        beer_property_list = beer_dictionary[recommend_beer]
        """Create a string to print with the new beer's stats"""
        recommend_string = disliked_previous + """New suggestion, based on your previous entries:
    
%s
IBU: %s
ABV: %s

Have you tried this beer?""" % (beer_property_list[0], beer_property_list[1], beer_property_list[2])

        disliked_previous = ''

    else:
        enable_recommend_buttons1()

        recommend_length = len(new_recommendation_list) - 1
        random_beer = random.randint(0, recommend_length)
        recommend_beer = new_recommendation_list[random_beer]
        beer_property_list = beer_dictionary[recommend_beer]
        """Create a string to print with the new beer's stats"""
        recommend_string = disliked_previous + """New suggestion, based on your previous entries:
    
%s
IBU: %s
ABV: %s

Have you tried this beer?""" % (beer_property_list[0], beer_property_list[1], beer_property_list[2])

        disliked_previous = ''

    print_to_console(recommend_string)
    #except:
    #    print_to_console("new_recommendation error.")

    return

#Enable yes/no buttons upon new recommendation - "Have you tried it?"
def enable_recommend_buttons1():
    global yes_button, no_button

    """Create yes button"""
    yes_button.grid(row = 0, sticky = W+S+E)
    yes_button.configure(command = lambda: tried_beer(True))

    """Create no button"""
    no_button.grid(row = 1, sticky = W+N+E)
    no_button.configure(command = lambda: tried_beer(False))

    return

#Ask if user has tried recommended beer
def tried_beer(response):
    global yes_button, no_button, recommend_beer

    yes_button.grid_forget()
    no_button.grid_forget()

    if response is True:
        enable_recommend_buttons2()
        print_to_console("Did you like it?")
    else:
        User.add_beer(recommend_beer, 0)
        recommend_new()

    return

#Enable yes/no buttons upon new recommendation - "Did you like it?"
def enable_recommend_buttons2():
    global yes_button, no_button

    """Create yes button"""
    yes_button.grid(row = 0, sticky = W+S+E)
    yes_button.configure(command = lambda: accept_beer_recommend(True))

    """Create no button"""
    no_button.grid(row = 1, sticky = W+N+E)
    no_button.configure(command = lambda: accept_beer_recommend(False))

    return

#Accepts entry, adds to user file
def accept_beer_recommend(response):
    global yes_button, no_button, recommend_beer, has_profile, disliked_previous

    if response is True:
        try:
            """add beer to list of liked beers"""
            User.add_beer(recommend_beer, 1)

            """update user file"""
            User.update_userfile(username_directory)

            """Clear yes/no buttons"""
            yes_button.grid_forget()
            no_button.grid_forget()
            print_to_console("Beer added to user file.")

        except:
            print_to_console("Error 7")

    elif response is False:
        try:
            """add beer to list of disliked beers"""
            User.add_beer(recommend_beer, 2)

            """update user file"""
            User.update_userfile(username_directory)

            """update disliked_previous"""
            disliked_previous = "Previous beer added to 'disliked' list.\n\n"

            """remove yes/no buttons, reset user entry"""
            yes_button.grid_forget()
            no_button.grid_forget()
            recommend_new()

        except:
            pass

    else:
        print_to_console("Error 6")

    return

#tells program that user wants to enter a new beer into their database
def new_entry():
    global yes_button, no_button

    if login_screen_active is False:
        yes_button.grid_forget()
        no_button.grid_forget()
        enable_new_beer_entry()

    return

#tells program to recommend a new beer based on user's preferences
def new_recommend():
    global yes_button, no_button

    if login_screen_active is False:
        yes_button.grid_forget()
        no_button.grid_forget()
        recommend_new()

    return

#shows user liked beers
def show_user():

    liked_string = 'Liked beers:\n'
    disliked_string = '\n\nDisliked beers:\n'
    to_try_string = '\n\nSaved to try later:\n'

    #reset screen
    try:
        yes_button.grid_forget()
        no_button.grid_forget()
        User_input_entry.grid_forget()
        input_button.grid_forget()
    except:
        pass
    
    for beer in User.get_liked():
        beer_name = beer_dictionary[beer][0]
        liked_string += '\n %s' % (beer_name.upper())

    for beer in User.get_disliked():
        beer_name = beer_dictionary[beer][0]
        disliked_string += '\n %s' % (beer_name.upper())

    for beer in User.get_to_try():
        beer_name = beer_dictionary[beer][0]
        to_try_string += '\n %s' % (beer_name.upper())        

    print_string = liked_string + disliked_string + to_try_string
    print_to_console(print_string)

    return

#closes window, shuts down program
def quit_program():

    beerapp.destroy()

    return

###Create top bar widgets###

#Username/login information
UserLabelStr = StringVar()
UserLabelStr.set("Not logged in.  Enter a Username.")
login_status = Label(beerapp,
               background = BGCOLOR,
               foreground = consolecolor,
               font = consolefont,
               textvariable = UserLabelStr)
login_status.grid(row = 0, columnspan = 3)

#new entry button
new_entry_button = Button(beerapp,
                     background = BGCOLOR,
                     foreground = butcolor,
                     text = "Add a beer to 'Preferred Beers'",
                     command = enable_new_beer_entry)

#new recommendation button
new_recommend_button = Button(beerapp,
                     background = BGCOLOR,
                     foreground = butcolor,
                     text = "Find a new good beer",
                     command = recommend_new)

#show user button
show_user_button = Button(beerapp,
                     background = BGCOLOR,
                     foreground = butcolor,
                     text = "Show user file",
                     command = show_user)

#exit button
exit_button = Button(beerapp,
                     background = BGCOLOR,
                     foreground = butcolor,
                     text = "Exit",
                     command = quit_program)
exit_button.grid(row = 0, column = 2, sticky = 'e')

###Create String Variables###

#User input field
User_input = StringVar()

#Console output label
console_output = StringVar()

###Create Widgets (forget each until called - except login widgets)###

#Username entry box
UserStr = StringVar()
Username_entry = Entry(login_buttons,
                       textvariable = UserStr,
                       background = entcolor,
                       foreground = entfontcolor,
                       relief = 'groove',)
Username_entry.grid(row = 0, sticky = W+S+E)

#user login/create user buttons
existingUser_button = Button(login_buttons,
                             text = "Login as User",
                             relief = 'groove',
                             background = BGCOLOR,
                             foreground = butcolor,
                             command = existingUser_loginbutton)
existingUser_button.grid(row = 1, sticky = W+N+E)

#Create output text box
console_output_label = Label(console_output_frame,
                             justify = LEFT,
                             background = BGCOLOR,
                             foreground = consolecolor,
                             font = consolefont,
                             wraplength = ((WIDTH / 3) * 2),
                             textvariable = console_output)
console_output_label.grid(row = 0, sticky = W)

#Set initial console text
print_to_console("Please log in.  If you don't have a profile, you will be prompted to create one.")

#Create user input box
User_input_entry = Entry(user_input_frame,
                         background = entcolor,
                         foreground = entfontcolor,
                         textvariable = User_input)
User_input_entry.grid_forget()

#Create user input button
input_button = Button(user_input_frame,
                      text = "Enter",
                      relief = 'groove',
                      background = BGCOLOR,
                      foreground = butcolor,
                      command = input_button_click)
input_button.grid_forget()

#create "Yes" button
yes_button = Button(user_input_frame,
                    text = "Yes",
                    relief = 'groove',
                    background = BGCOLOR,
                    foreground = butcolor,)
yes_button.grid_forget()

#create "No" button
no_button = Button(user_input_frame,
                   text = "No",
                   relief = 'groove',
                   background = BGCOLOR,
                   foreground = butcolor,)
no_button.grid_forget()

#binds "Enter" key to existing user login button, set focus on login entry
programfuncs.bind_enter(beerapp, existingUser_login)
Username_entry.focus_set()

#start frame (login)
beerapp.mainloop()