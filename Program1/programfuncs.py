### Frame/Widget Display Functions ###

#Enable User input/Console output
def enable_io(User_input_entry, input_button, console_output_label, entcolor, entfontcolor, bgcolor, butcolor, consolecolor, consolefont, console_output, User_input):
    """Create user input box"""
    User_input_entry = Entry(user_input_frame,
                             background = entcolor,
                             foreground = entfontcolor,
                             textvariable = User_input,).grid(row = 0, rowspan = 1, sticky = N+S+E+W)
    """Create user input button"""
    input_button = Button(user_input_frame,
                          text = "Enter",
                          relief = 'groove',
                          background = bgcolor,
                          foreground = butcolor,
                          command = input_button).grid(row = 2, rowspan = 2, sticky = N+S+E+W)
    """Create output text box"""
    console_output_label = Label(console_output_frame,
                                 wraplength = 225,
                                 justify = LEFT,
                                 background = bgcolor,
                                 foreground = consolecolor,
                                 font = consolefont,
                                 textvariable = console_output,).grid(row = 0, rowspan = 4, sticky = N+E)
    print_to_console("Give me the name of a good beer.  Spelling counts.")
    return

### Login Functions ###

#make sure Username is available
def check_availableUser(input, Username_list):
    #'True' is a placeholder for now.  Need to add a check for available Username.
    available = True
    for user in Username_list:
        if (input + '.txt') == user:
            available = False
    return available

### Functions for Operation of Program ###

#bind 'Enter' to named function
def bind_enter(root, func):
    root.bind('<Return>', func)
    return

#button to send data from input to program/console
def input_button():
    input = User_input.get()
    found = beer.find_input_beer(input, database_list)
    try:
        console_response = "Found the following beer:" + '\n' + str(found[0]).upper() + '\n' + "IBU:  " + str(found[1]).upper()
        print_to_console(console_response)
    except:
        print_to_console("Error3")    
    return

#create function for 'Enter/Return' key to call, since it requires an 'event' parameter
def input_enter(event):
    input = User_input.get()
    found = beer.find_input_beer(input, database_list)
    try:
        console_response = "Found the following beer:" + '\n' + str(found[0]).upper()
        print_to_console(console_response)
    except:
        print_to_console("Error4")    
    return

#return yes or no
def yes_no(response):
    if response is True:
        return True
    elif response is False:
        return False
