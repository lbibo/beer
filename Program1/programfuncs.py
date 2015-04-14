#make sure Username is available
def check_availableUser(input, Username_list):

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