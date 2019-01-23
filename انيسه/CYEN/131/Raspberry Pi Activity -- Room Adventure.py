######################################################################
# Name: Anisah Alahmed
# Date: 1/14/2019
# Description: Room Adventure
######################################################################

# Changes overview:
# Made it so that item descriptions change when you pick up a grabbable
# Added some new rooms in the "up" direction
# Added some more items and grabbables

######################################################################
# the blueprint for a room
class Room(object):
	# the constructor
	def __init__(self, name):
		# rooms have a name, exits (e.g., south), exit locations
		# (e.g., to the south is room n), items (e.g., table), item
		# descriptions (for each item), and grabbables (things that
		# can be taken into inventory)
		self.name = name
		self.exits = []
		self.exitLocations = []
		self.items = []
		self.itemDescriptions = []
		self.grabbables = {} # CHANGE: changed grabbables to a dictionary to pair grabbables with items that they are contained on

	# getters and setters for the instance variables
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def exits(self):
		return self._exits

	@exits.setter
	def exits(self, value):
		self._exits = value

	@property
	def exitLocations(self):
		return self._exitLocations

	@exitLocations.setter
	def exitLocations(self, value):
		self._exitLocations = value

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, value):
		self._items = value

	@property
	def itemDescriptions(self):
		return self._itemDescriptions

	@itemDescriptions.setter
	def itemDescriptions(self, value):
		self._itemDescriptions = value

	@property
	def grabbables(self):
		return self._grabbables

	@grabbables.setter
	def grabbables(self, value):
		self._grabbables = value

	# adds an exit to the room
	# the exit is a string (e.g., north)
	# the room is an instance of a room
	def addExit(self, exit, room):
		# append the exit and room to the appropriate lists
		self._exits.append(exit)
		self._exitLocations.append(room)

	# adds an item to the room
	# the item is a string (e.g., table)
	# the desc is a string that describes the item (e.g., it is made
	# of wood)
	def addItem(self, item, desc):
		# append the item and description to the appropriate lists
		self._items.append(item)
		self._itemDescriptions.append(desc)

	# adds a grabbable item to the room
	# the item is a string (e.g., key)
	def addGrabbable(self, item, location, update=None):
		# append the item to the list
		self._grabbables[item] = [location, update]# CHANGE: grabbables are added to the dictionary with a location for the grabbable

	# removes a grabbable item from the room
	# the item is a string (e.g., key)
	def delGrabbable(self, item):
		# CHANGE: update the description of the container
		container = self.grabbables[item][0]
		update = self.grabbables[item][1]
		# find the index of the container in the items list
		containerIndex = self.items.index(container)
		self._itemDescriptions[containerIndex] = update
		# remove the item from the list
		self._grabbables.pop(item)

	# returns a string description of the room
	def __str__(self):
		# first, the room name
		s = "You are in {}.\n".format(self.name)
		# next, the items in the room
		s += "You see: "
		for item in self.items:
			s += item + " "
		s += "\n"
		# next, the exits from the room
		s += "Exits: "
		for exit in self.exits:
			s += exit + " "
		return s

# creates the rooms
def createRooms():
	# r1 through r4 are the four rooms in the mansion
	# currentRoom is the room the player is currently in (which can
	# be one of r1 through r4)
	# since it needs to be changed in the main part of the program,
	# it must be global
	global currentRoom

	# create the rooms and give them meaningful names
	r1 = Room("Room 1")
	r2 = Room("Room 2")
	r3 = Room("Room 3")
	r4 = Room("Room 4")

	# add exits to room 1
	r1.addExit("east", r2) # -> to the east of room 1 is room 2
	r1.addExit("south", r3)
	# add grabbables to room 1
	# CHANGE: Worked the description updating into the key grabbable
	r1.addGrabbable("key", "table", "It is made of oak. The key is gone.")
	# add items to room 1
	r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
	r1.addItem("table", "It is made of oak. A golden key rests on it.")

	# add exits to room 2
	r2.addExit("west", r1)
	r2.addExit("south", r4)
	# add items to room 2
	r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
	r2.addItem("fireplace", "It is full of ashes.")

	# add exits to room 3
	r3.addExit("north", r1)
	r3.addExit("east", r4)
	# add grabbables to room 3
	# CHANGE: Worked the description updating into the book grabbable
	r3.addGrabbable("book", "desk", "The statue is still resting on it, but the book is gone.")
	# add items to room 3
	r3.addItem("bookshelves", "They are empty. Go figure.")
	r3.addItem("statue", "There is nothing special about it.")
	r3.addItem("desk", "The statue is resting on it. So is a book.")

	# add exits to room 4
	r4.addExit("north", r2)
	r4.addExit("west", r3)
	r4.addExit("south", None) # DEATH!
	# add grabbables to room 4
	# CHANGE: Worked the description updating into the 6-pack grabbable
	r4.addGrabbable("6-pack", "brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig. You took the 6-pack already. Please drink responsibly.")
	# add items to room 4
	r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig. A 6-pack is resting beside it.")

	# set room 1 as the current room at the beginning of the game
	currentRoom = r1

	# NEW STUFF STARTS HERE --------------
	r5 = Room("Room 5")
	r6 = Room("Room 6")

	# Connect first floor to second floor
	r1.addExit("up", r5)
	r2.addExit("up", r6)

	# Configure room 5
	r5.addExit("down", r1)
	r5.addExit("east", r6)

	r5.addItem("window", "There is a window to the outside with a potted_plant on it. Through it you can see the matrix.")
	r5.addGrabbable("potted_plant", "window", "There is a window to the outside. Through it you can see the matrix.")

	# Configure room 6
	r6.addExit("down", r2)
	r6.addExit("west", r5)

	r6.addItem("fridge", "There is a fridge. It is empty except for some milk.")
	r6.addItem("counter", "A countertop. It's pretty dirty.")
	r6.addItem("stove", "There is a stove with a skillet on it.")
	r6.addItem("skillet", "There is turkey_bacon in this skillet. Fresh. Mm....")

	r6.addGrabbable("milk", "fridge", "There is a fridge. It is empty.")
	r6.addGrabbable("turkey_bacon", "skillet", "The turkey bacon is gone. It was delicious.")

# displays an appropriate "message" when the player dies
# yes, this is intentionally obfuscated!
def death():
        print " " * 17 + "u" * 7
        print " " * 13 + "u" * 2 + "$" * 11 + "u" * 2
        print " " * 10 + "u" * 2 + "$" * 17 + "u" * 2
        print " " * 9 + "u" + "$" * 21 + "u"
        print " " * 8 + "u" + "$" * 23 + "u"
        print " " * 7 + "u" + "$" * 25 + "u"
        print " " * 7 + "u" + "$" * 25 + "u"
        print " " * 7 + "u" + "$" * 6 + "\"" + " " * 3 + "\"" + "$" * 3 + "\"" + " " * 3 + "\"" + "$" * 6 + "u"
        print " " * 7 + "\"" + "$" * 4 + "\"" + " " * 6 + "u$u" + " " * 7 + "$" * 4 + "\""
        print " " * 8 + "$" * 3 + "u" + " " * 7 + "u$u" + " " * 7 + "u" + "$" * 3
        print " " * 8 + "$" * 3 + "u" + " " * 6 + "u" + "$" * 3 + "u" + " " * 6 + "u" + "$" * 3
        print " " * 9 + "\"" + "$" * 4 + "u" * 2 + "$" * 3 + " " * 3 + "$" * 3 + "u" * 2 + "$" * 4 + "\""
        print " " * 10 + "\"" + "$" * 7 + "\"" + " " * 3 + "\"" + "$" * 7 + "\""
        print " " * 12 + "u" + "$" * 7 + "u" + "$" * 7 + "u"
        print " " * 13 + "u$\"$\"$\"$\"$\"$\"$u"
        print " " * 2 + "u" * 3 + " " * 8 + "$" * 2 + "u$ $ $ $ $u" + "$" * 2 + " " * 7 + "u" * 3
        print " u" + "$" * 4 + " " * 8 + "$" * 5 + "u$u$u" + "$" * 3 + " " * 7 + "u" + "$" * 4
        print " " * 2 + "$" * 5 + "u" * 2 + " " * 6 + "\"" + "$" * 9 + "\"" + " " * 5 + "u" * 2 + "$" * 6
        print "u" + "$" * 11 + "u" * 2 + " " * 4 + "\"" * 5 + " " * 4 + "u" * 4 + "$" * 10
        print "$" * 4 + "\"" * 3 + "$" * 10 + "u" * 3 + " " * 3 + "u" * 2 + "$" * 9 + "\"" * 3 + "$" * 3 + "\""
        print " " + "\"" * 3 + " " * 6 + "\"" * 2 + "$" * 11 + "u" * 2 + " " + "\"" * 2 + "$" + "\"" * 3
        print " " * 11 + "u" * 4 + " \"\"" + "$" * 10 + "u" * 3
        print " " * 2 + "u" + "$" * 3 + "u" * 3 + "$" * 9 + "u" * 2 + " \"\"" + "$" * 11 + "u" * 3 + "$" * 3
        print " " * 2 + "$" * 10 + "\"" * 4 + " " * 11 + "\"\"" + "$" * 11 + "\""
        print " " * 3 + "\"" + "$" * 5 + "\"" + " " * 22 + "\"\"" + "$" * 4 + "\"\""
        print " " * 5 + "$" * 3 + "\"" + " " * 25 + "$" * 4 + "\""

######################################################################
# START THE GAME!!!
inventory = [] # nothing in inventory...yet
createRooms() # add the rooms to the game

# play forever (well, at least until the player dies or asks to quit)
while (True):
	# set the status so the player has situational awareness
	# the status has room and inventory information
	status = "{}\nYou are carrying: {}\n".format(currentRoom, inventory)

	# if the current room is None, then the player is dead
	# this only happens if the player goes south when in room 4
	if (currentRoom == None):
		status = "You are dead."

	# display the status
	print "========================================================="
	print status

	# if the current room is None (and the player is dead), exit the
	# game
	if (currentRoom == None):
		death()
		break

	# prompt for player input
	# the game supports a simple language of <verb> <noun>
	# valid verbs are go, look, and take
	# valid nouns depend on the verb
	# we use raw_input here to treat the input as a string instead of
	# a numeric value
	action = raw_input("What to do? ")

	# set the user's input to lowercase to make it easier to compare
	# the verb and noun to known values
	action = action.lower()

	# exit the game if the player wants to leave (supports quit,
	# exit, and bye)
	if (action == "quit" or action == "exit" or action == "bye"):
		break

	# set a default response
	response = "I don't understand. Try verb noun. Valid verbs are go, look, and take"
	# split the user input into words (words are separated by spaces)
	words = action.split()

	# the game only understands two word inputs
	if (len(words) == 2):
		# isolate the verb and noun
		verb = words[0]
		noun = words[1]

		# the verb is: go
		if (verb == "go"):
			# set a default response
			response = "Invalid exit."

			# check for valid exits in the current room
			for i in range(len(currentRoom.exits)):
				# a valid exit is found
				if (noun == currentRoom.exits[i]):
					# change the current room to the one that is
					# associated with the specified exit
					currentRoom = currentRoom.exitLocations[i]
					# set the response (success)
					response = "Room changed."

					# no need to check any more exits
					break

		# the verb is: look
		elif (verb == "look"):
			# set a default response
			response = "I don't see that item."

			# check for valid items in the current room
			for i in range(len(currentRoom.items)):
				# a valid item is found
				if (noun == currentRoom.items[i]):
					# set the response to the item's description
					response = currentRoom.itemDescriptions[i]

					# no need to check any more items
					break

		# the verb is: take
		elif (verb == "take"):
			# set a default response
			response = "I don't see that item."

			# check for valid grabbable items in the current room
			for grabbable in currentRoom.grabbables:
				# a valid grabbable item is found
				if (noun == grabbable):
					# add the grabbable item to the player's
					# inventory
					inventory.append(grabbable)

					# remove the grabbable item from the room
					currentRoom.delGrabbable(grabbable)

					# set the response (success)
					response = "Item grabbed."

					# no need to check any more grabbable items
					break

	# display the response
	print "\n{}".format(response)