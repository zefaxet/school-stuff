#########################################
# Name: Anisah Alahmed
# Date: 2/20/2019
# Desc: My Barbie World Adventure!
#########################################

class State(object):

	def __init__(self):
		self.options = []
		self.optionDescriptions = []

	@property
	def story(self):
		return self._story

	@story.setter
	def story(self, value):
		self._story = value

	def addOption(self, option, optionDesc):
		self.optionDescriptions.append(optionDesc)
		self.options.append(option)

	def isOptionValid(self, value):
		for option in self.options:
			if value == option:
				return True
		return False

	def __str__(self):
		string = self.story
		for i in range(len(self.options)):
			string += "\n\t{} ({})".format(self.optionDescriptions[i], self.options[i])
		return string

states = {}

start = State()
start.story = "You are a Barbie Girl in a Barbie World. Wrapped in Plastic, it's fantastic.\nYou want to be famous, no matter what it takes.\nHow should you do this?"
start.addOption("surgery", "Do plastic surgery.")
start.addOption("model", "Apply to a modeling agency.")
start.addOption("movie", "Make a real Hollywood movie.")
states["start"] = start

surgery = State()
surgery.story = "You decide to get plastic surgery, but what kind of surgery do you want?"
surgery.addOption("implants", "Butt implants.")
surgery.addOption("fillers", "Lip fillers.")
states["surgery"] = surgery

model = State()
model.story = "When you apply to model for IMG models, they tell you you're too fat and need to lose a few inches of your waistline."
model.addOption("diet", "Strict diet.")
model.addOption("liposuction", "Liposuction.")
states["model"] = model

movie = State()
movie.story = "You pack your things and say goodbye to your family.\nHollywood acting is your true calling.\nHow do you reach fame?"
movie.addOption("school", "Go to acting school.")
movie.addOption("indie", "Make your own indie movie.")
states["movie"] = movie

implants = State()
implants.story = "You proceeded to get implants surgically in your butt. You posted the pictures on Instagram, which Kim Kardashian noticed and followed you for.\nYou are now BFFs with Kim Kardashian. So watermelon!\nWhere do you take your new connection?"
implants.addOption("friends", "Just stay friends and become a social media influencer.")
implants.addOption("yeezy", "Take advantage of her and become the main model for Yeezy.")
states["implants"] = implants

fillers = State()
fillers.story = "You proceed to get fillers for your lips. You posted the pictures on Instagram, which Kylie Jenner noticed and followed you for.\nYou are now BFFs with Kylie Jenner and you started a limited edition makeup line in cooperation with her."
fillers.addOption("friends", "Stay the course and become social media influencer, stealing from Kylie's mindless following.")
fillers.addOption("hookup", "Hook up with your best friend's sister's boyfriend.")
states["fillers"] = fillers

diet = State()
diet.story = "You proceed to subject yourself to extreme stress and pressure by taking away any enjoyment from eating.\nYou consume strictly whole weat gluten free bread and celery for 6 months.\nAfter these months you are in a state of severe anguish and mental depression, and you haven't lost the inches yet.\nMaybe you should have done lipsuction instead. It would have been easier.\nWhat do you do?"
diet.addOption("break bones", "Break your ribs to lose the inches.")
diet.addOption("keep dieting", "Keep dieting.")
diet.addOption("give up", "Give up.")
diet.addOption("youtube", "Make body positivity videos on YouTube.")
diet.addOption("dr. phil", "Go to Dr. Phil and talk about your eating disorder.")
states["diet"] = diet

liposuction = State()
liposuction.story = "You proceed to subject your body to intense physical stress of forcible removal of body fat.\nThis is a very uncomfortable procedure but it's worth it, you're going to be famous!\nAfter 6 months tortuting your skin, you still haven't lost the inches.\nMaybe you should have done the diet instead of trying to take a shortcut.\nWhat do you do now?"
liposuction.addOption("break bones", "Break your ribs to lose the inches.")
liposuction.addOption("give up", "Give up.")
liposuction.addOption("youtube", "Make body positivity videos on YouTube.")
states["liposuction"] = liposuction

school = State()
school.story = "You enroll in some acting school nobody has ever heard of, but whatever - the degree is all that matters.\nYou discover that your acting skills are pretty terrible. How do you pass?"
school.addOption("seduce", "Seduce the teacher.")
school.addOption("sympathy", "Play dumb for sympathy grades.")
school.addOption("try", "Try really hard in school.")
states["school"] = school

indie = State()
indie.story = "You make a romantic drama movie so unbelievably terrible that everybody loves it as a comedy.\nIt becomes one of the most well-known movies of all time as the worst of all time.\nYou somehow managed to spend 5 million dollars on this movie but no one knows where you got the money."
states["indie"] = indie

friends = State()
friends.story = "You decide to become a social media influencer on instagram and twitter.\nYou rake in tons of cash from ad revenue and garner major clout from your followers who will now die for you."
states["friends"] = friends

yeezy = State()
yeezy.story = "You are now top model for one of the most pointless and lucritive brands in the world. Congratulations!"
states["yeezy"] = yeezy

hookup = State()
hookup.story = "Nice going. Now literally everybody on Instagram, which is everybody that matters, hates you.\nYour life is ruined. Now you'll never be famous!"
states["hookup"] = hookup

breakBones = State()
breakBones.story = "You broke your ribs on purpose. It was really painful but now you lost the inches!\nIMG accepts you as a model! You did it, you're famous!"
states["break bones"] = breakBones

keepDieting = State()
keepDieting.story = "You continue to subject yourself to extreme mental anguish and physical malnourishment in hopes of losing the inches.\nUnfortunately you keep doing this for so long your vital systems cease to function correctly and your liver fails.\nYou die shortly after. Oh no!"
states["keep dieting"] = keepDieting

giveUp = State()
giveUp.story = "You gave up. You're just an average regular everyday Barbie Girl in this cruel Barbie World. Not Fantastic!"
states["give up"] = giveUp

youtube = State()
youtube.story = "You make body positivity videos on YouTube telling girls how to love themselves no matter how they look.\nYou gain a meager following but its better than nothing."
states["youtube"] = youtube

drPhil = State()
drPhil.story = "You go on to Dr. Phil and talk about eating disorders.\nBecause you're not like everyone else and a very special Barbie Girl, you yell a lot and say crazy things for attention.\nPeople watching find this hilarious and boost you into the social media limelight.\nNow you're famous somehow, but you're not complaining!"
states["dr. phil"] = drPhil

seduce = State()
seduce.story = "You hook up with the teacher and convince him to give you passing grades.\nYou manage to graduate with honors without ever doing any work.\nYou land a role in diaper commercials. Nice!"
states["seduce"] = seduce

sympathy = State()
sympathy.story = "Your acting is so terrible that you use it to your advantage to make the professors feel sorry for you.\nThey go easy on you and you pass with average grades. C's get degrees!\nYou catch the eye of Prince Harry when performing your senior thesis.\nYou get married and all of the sudden you're the queen of England. Sweet!"
states["sympathy"] = sympathy

trySchool = State()
trySchool.story = "You try really hard to pass the right way, because the right way always wins.\nIt takes you 8 years to graduate with a terrible GPA but you feel really good about it in the end.\nSurely your hard work will be rewarded!\nAfter years of fruitless searching you finally land a job as a high school english teacher. Shucks!"
states["try"] = trySchool

# Main ###########################
print("VERY IMPORTANT!")
print("Go to the following link to play the background music for this story. It is VERY important for the mood and crucial for the story.")
print("https://www.youtube.com/watch?v=CEYHQjcn_M8")
raw_input("When the music is ready, press enter to start the story.\n")

currentState = start

while len(currentState.options) > 0:

	print(currentState)
	option = raw_input("Do: ")
	option = option.lower()
	if not currentState.isOptionValid(option):
		print("Invalid option.")
		print("")
		continue
	else:
		currentState = states[option]
		print("")

print(currentState)
print("That's the end!")
