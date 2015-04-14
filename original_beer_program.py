#next steps: if beer is liked or disliked, remove from possible suggestions
#add disliked beers to user profile somehow?

#define variables
found = False
exhaust_db_ibus = False
suggesteddb = []
suggested_beers = []
random_beer = []
good_beer = []
user_beers = []
bad_beers = []
new_user_file = ''
bad_string = 'disliked beers:'
user_file = ''
suggested_ibu_range = 0
suggested_srm_range = 0
randpickno = 0
max_ibu = 100

#create database list
database1 = open('database.txt').readlines()
database = []
for x in database1:
	if len(x) < 3:
		continue
	else:
		database.append(x.split(','))

#prompt for existing file, load existing file if possible
while True:
	existing = raw_input("Have you used this program before?: ")
	existing = existing.lower()
	name = raw_input("What is your name?: ").lower()
	if existing == "yes" or existing == "y":
		existing = True
		filename = name + '.txt'
		try:
			user_file_1 = open(filename,'r')
		except:
			print "That user name doesn't exist. We'll create one for you."
			existing = False
			break
		for x in user_file_1:
			if x.startswith('user average'):
				user_file = x.rstrip() + '\n' + name.rstrip()
			elif x.startswith(name):
				continue
			else:
				user_file = user_file.rstrip() + '\n' + x.rstrip()
				user_beers.append(x.split(','))
				continue
		break
	elif existing == "no" or existing == "n":
		filename = name + '.txt'
		existing = False
		break
	else:
		print "Please enter yes or no."
		continue

name = (name[:1].upper() + name[1:].lower()).strip()

#function to prompt for good beer, find it within database, and fill variables
def good_beer_func(x):
	global database
	retstring = 'Beer not found.'
	for y in database:
		itervar = str(y[0])
		if not x in itervar:
			continue
		else:
			retstring = y
			break
	return retstring

#Pick a beer from the database
def pick_beer():
	again = True
	while True:
		if again is True:
			good_beer = good_beer_func(raw_input("What's a good beer?: ").lower())
			if 'Beer not found' in good_beer:
				print 'Beer not found.  Please check your spelling.'
				continue
			else:
				print '\n' + "You chose: \n"
				print good_beer[0].upper()
				print "IBU: " + good_beer[1]
				print "ABV: " + good_beer[2] + "%"
				print "Standard Reference Method (color scale): " + good_beer[3]
		else:
			break
		while True:
			again = raw_input("Is this the beer you were looking for?: ").lower()
			if again == "yes" or again == "y":
				again = False
				if '?' in good_beer[1]:
					good_beer[1] = 'unknown'
				if '?' in good_beer[2]:
					good_beer[2] = 'unknown'
				if '?' in good_beer[3]:
					good_beer[3] = 'unknown'
				return good_beer
				break
			elif again == "no" or again == "n":
				again = True
				break
			else:
				print "Please enter yes or no."
				continue

def pull_user_average():
	global filename
	global name
	global bad_beers
	global bad_string
	global new_user_file
	skip = False
	count = 0.0
	user_file = open(filename).readlines()
	ibu = 0.0
	ibucount = 0.0
	abv = 0.0
	abvcount = 0.0
	srm = 0.0
	srmcount = 0.0
	for x in user_file:
		if skip is False:
			if x.startswith('user average'):
				continue
			elif x.startswith(name):
				continue
			elif not x.startswith('disliked beers:'):
				new_user_file = new_user_file.strip() + '\n' + x.strip()
				line = x.split(',')
				try:
					ibu = ibu + float(line[1])
					ibucount = ibucount + 1.0
				except:
					continue
				try:
					abv = abv + float(line[2])
					abvcount = abvcount + 1.0
				except:
					continue
				try:
					srm = srm + float(line[3].rstrip)
					srmcount = srmcount + 1.0
				except:
					continue
			elif x.startswith('disliked beers:'):
				skip = True
				continue
		else:
			if 'disliked beers:' in x:
				continue
			else:
				bad_string = bad_string.strip() + '\n' + x
				line = x.split(',')
				bad_beers.append(line)
	if ibucount == 0:
		ibu = "unknown"
	else:
		ibu = ibu / ibucount	
	if abvcount == 0:
		abv = "unknown"
	else:
		abv = abv / ibucount
	if srmcount == 0:
		srm = "unknown"
	else:
		srm = srm / srmcount
	return [str(ibu),str(abv),str(srm)]

if existing is True:
	good_beer = pull_user_average()
	#apply attributes of user average
	good_name = 'user average'
	good_ibu = good_beer[0].rstrip()
	good_abv = good_beer[1].rstrip()
	good_srm = good_beer[2].rstrip()
	good_string = (str(good_name) + ',' + str(good_ibu) + ',' + str(good_abv) + ',' + str(good_srm)).rstrip()
else:
	good_beer = pick_beer()
	#apply attributes of found beer
	good_name = good_beer[0].rstrip()
	good_ibu = good_beer[1].rstrip()
	good_abv = good_beer[2].rstrip()
	good_srm = good_beer[3].rstrip()
	good_string = (str(good_name) + ',' + str(good_ibu) + ',' + str(good_abv) + ',' + str(good_srm)).rstrip()

#find all beers in suggested range
def reccom_new(x,y):
	global database
	global suggesteddb
	global user_beers
	global existing
	global good_beer
	global suggested_beers
	global suggested_ibu_range
	global suggested_srm_range
	for beer in database:
		if float(beer[1]) >= (x - suggested_ibu_range) and float(beer[1]) <= (x + suggested_ibu_range) and float(beer[3]) >= (y - suggested_srm_range) and float(beer[3]) <= (y + suggested_srm_range):
			if existing is True:
				skip = False
				for userb in user_beers:
					if userb[0] in beer[0]:
						skip = True
						break
					else:
						continue
				if skip is False:
					suggesteddb.append(beer)
			else:
				if good_beer[0] in beer[0]:
					continue
				else:
					suggesteddb.append(beer)
		for beer2 in suggested_beers:
			if beer2[0] in beer[0]:
				suggesteddb.remove(beer)
				continue
		for beer2 in bad_beers:
			if beer2[0] in beer[0]:
				suggesteddb.remove(beer)
				continue

#check to make sure suggested_ibu_range is sufficient to create a database of random beers
def check_suggested_ibu_range(x,y):
	global suggesteddb
	global suggested_ibu_range
	global suggested_srm_range
	global reccom_new
	global exhaust_db_ibus
	while True:
		reccom_new(x,y)
		if exhaust_db_ibus is True:
			suggested_srm_range += 1
			suggested_ibu_range = 0
			exhaust_db_ibus = False
			reccom_new(x,y)
			continue
		else:
			if len(suggesteddb) < 1:
				suggested_ibu_range = suggested_ibu_range + 1
				reccom_new(x,y)
				continue
			else:
				break

#pick a random beer (random index number) from suggested list
def randpick_func():
	import random
	global suggested
	global randpickno
	randpick = random.randint(0,(len(suggesteddb) - 1))
	randpickno = randpick
	return randpick

#make sure suggestion range is > 0
try:
	check_suggested_ibu_range(float(good_ibu),float(good_srm))
except:
	suggested_srm_range = 40
	check_suggested_ibu_range(float(good_ibu),20)

#pick one of the reccomended beers
random_beer = suggesteddb[randpick_func()]

#print suggestion
why_not = "Why not try: " + str(random_beer[0]) + "?"
print '\n'
print why_not.upper()
print '\n'

random_name = random_beer[0].rstrip()
random_ibu = random_beer[1].rstrip()
random_abv = random_beer[2].rstrip()
random_srm = random_beer[3].rstrip()
random_string = (str(random_name) + ',' + str(random_ibu) + ',' + str(random_abv) + ',' + str(random_srm)).rstrip()

def no_new(x):
	global new_user_file
	global filename
	global good_string
	global bad_string
	if x is True:
		if new_user_file.startswith('user average'):
			start = new_user_file.find('\n') + 1
			new_beg = new_user_file[start:]
			new_save_file = good_string.strip() + '\n' + name.strip() + '\n' + new_beg.strip() + bad_string.strip()
			create_file = open(filename,'w')
			create_file.write(new_save_file)
		else:
			new_save_file = good_string.strip() + '\n' + name.strip() + '\n' + new_user_file.strip() + '\n' + bad_string.strip()
			create_file = open(filename,'w')
			create_file.write(new_save_file)
	else:
		new_save_file = name.strip() + '\n' + good_string.strip() + '\n' + bad_string.strip()
		create_file = open(filename,'w')
		create_file.write(new_save_file)

def new_beer(x):
	global new_user_file
	global filename
	global good_string
	global bad_string
	if x is True:
		if new_user_file.startswith('user average'):
			start = new_user_file.find('\n')
			new_beg = new_user_file[start:]
			new_save_file = good_string.rstrip() + '\n' + name.rstrip() + '\n' + new_beg.rstrip() + '\n' + random_string.rstrip() + '\n' + bad_string.rstrip()
			create_file = open(filename,'w')
			create_file.write(new_save_file)
		else:
			new_save_file = good_string.rstrip() + '\n' + name.rstrip() + '\n' + new_user_file.rstrip() + '\n' + random_string.rstrip() + '\n' + bad_string.rstrip()
			create_file = open(filename,'w')
			create_file.write(new_save_file)
	else:
		new_save_file = name.rstrip() + '\n' + good_string.rstrip() + '\n' + random_string.rstrip() + '\n' + bad_string.rstrip()
		create_file = open(filename,'w')
		create_file.write(new_save_file)

#save new file
#ask user if they like suggested beer
while True:
	tried = raw_input("Have you tried this beer before?: ").lower()
	if tried == "yes" or tried == "y":
		like = raw_input("Did you like this beer?: ")
		if like == "yes" or like == "y" :
			new_beer(existing)
			break
		#Just need to find out how to write "liked beer" to end of file!!!
		elif like == "no" or like == "n":
			bad_beers.append(random_beer)
			bad_string = bad_string.strip() + '\n' + random_beer[0] + ',' + random_beer[1] + ',' + random_beer[2] + ',' + random_beer[3].rstrip()
			print "Okay, maybe we can suggest another beer then. "
			again = raw_input("Would you like a different suggestion?: ").lower()
			if again == "yes" or again == "y":
				suggested_beers.append(random_beer)
				suggesteddb = []
				try:
					check_suggested_ibu_range(float(good_ibu),float(good_srm))
				except:
					suggested_srm_range = 40
					check_suggested_ibu_range(float(good_ibu),20)
				random_beer = suggesteddb[randpick_func()]

				#print suggestion
				why_not = "Why not try: " + str(random_beer[0]) + "?"
				print '\n'
				print why_not.upper()
				print '\n'
				random_name = random_beer[0].rstrip()
				random_ibu = random_beer[1].rstrip()
				random_abv = random_beer[2].rstrip()
				random_srm = random_beer[3].rstrip()
				random_string = (str(random_name) + ',' + str(random_ibu) + ',' + str(random_abv) + ',' + str(random_srm)).rstrip()
			elif again == "no" or again == "n":
				print "Ok.  Please re-run the program again later for another suggestion. \n"
				no_new(existing)
				break
	elif tried == "no" or tried == "n":
		again = raw_input("Would you like a different suggestion?: ").lower()
		if again == "yes" or again == "y":
			suggested_beers.append(random_beer)
			suggesteddb = []
			try:
				check_suggested_ibu_range(float(good_ibu),float(good_srm))
			except:
				suggested_srm_range = 40
				check_suggested_ibu_range(float(good_ibu),20)

			random_beer = suggesteddb[randpick_func()]

			#print suggestion
			why_not = "Why not try: " + str(random_beer[0]) + "?"
			print '\n'
			print why_not.upper()
			print '\n'
			random_name = random_beer[0].rstrip()
			random_ibu = random_beer[1].rstrip()
			random_abv = random_beer[2].rstrip()
			random_srm = random_beer[3].rstrip()
			random_string = (str(random_name) + ',' + str(random_ibu) + ',' + str(random_abv) + ',' + str(random_srm)).rstrip()
		elif again == "no" or again == "n":
			print "Ok.  Please re-run the program again later for another suggestion. \n"
			no_new(existing)
			break
	else:
		print "Please enter yes or no."
		continue

#ask if they want to know about their user profile
user_profile_question = raw_input("Do you want to know what your user profile currently says about you?: ").lower()
while True:
	if user_profile_question == "yes" or user_profile_question == "y":
		print "\n" + str(name)
		print "Preferred IBU: " + str(good_ibu)
		print "Preferred ABV: " + str(good_abv) + "%"
		print "Preferred SRM (Beer Color): " + str(good_srm) + '\n'
		break
	elif user_profile_question == "no" or user_profile_question == "n":
		print "Ok. \n"
		break
	else:
		print "Please enter yes or no."
		continue

raw_input("Press enter to close the program. ")

#User Experience
#prompt for user name
#User presented with beer of certain qualities (abv, ibu, srmv, etc.)
#User rates beer on hopiness, alcohol and other qualities
#user profile:
#	'user average,#ibu,#abv,#srm'
#	*user name*
#	list of liked beers