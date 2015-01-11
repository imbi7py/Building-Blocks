import sys,pygame,random,time, pygame.mixer, json
from pygame.locals import *
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

clock = pygame.time.Clock()

nodes = {}
world = {}

def new_node(name,attributes):
	nodes[name] = attributes
	return

def print_nodes():
	for x in nodes:
		print x
		print nodes[x]
	return
	
def play_sound(sound):
	pygame.mixer.music.load(sound)
	pygame.mixer.music.play()
	
def write(text, start_x,y):
	xadd = 0
	text = text.upper()
	for letter in str(text):
		screen.blit(pygame.image.load("textures/Numbers/"+letter+".png"),(start_x+xadd,y))
		xadd += 7
	
new_node("grass",{"description" : "Grass","hard" : "no"})
new_node("tallgrass",{"description" : "TallGrass","hard" : "no","passthrough":"yes"})
new_node("door",{"description" : "Door","hard" : "yes","passthrough":"yes"})
new_node("door_closed",{"description" : "Door_Closed","hard" : "yes"})
new_node("door2",{"description" : "Door2","hard" : "yes","passthrough":"yes"})
new_node("door_closed2",{"description" : "Door_Closed2","hard" : "yes"})
new_node("water",{"description" : "Water","hard" : "no","passthrough":"yes"})
new_node("flowingwater",{"description" : "FlowingWater","hard" : "no","passthrough":"yes"})
new_node("backwall",{"description" : "BackWall","hard" : "no","passthrough":"yes" })
new_node("leaves",{"description" : "Leaves","hard" : "no","passthrough":"yes"})
new_node("tree",{"description" : "Tree","hard" : "no","passthrough":"yes"})
new_node("iron",{"description" : "Iron","hard" : "yes"})
new_node("gold",{"description" : "Gold","hard" : "yes"})
new_node("stone",{"description" : "Stone","hard" : "yes"})
new_node("brick",{"description" : "Brick","hard" : "yes"})
new_node("air",{"description" : "Air","hard" : "no","passthrough":"yes"})
new_node("sand",{"description" : "Sand","hard" : "no"})
new_node("wood",{"description" : "Wood","hard" : "no"})
new_node("sapling",{"description" : "Sapling","hard" : "no"})
new_node("cactus",{"description" : "Cactus","hard" : "no","passthrough":"yes","ow":"yes"})

# This old function isn't needed. It justs prints the nodes that exist before the game starts.
# If you really need to see the nodes that exist, look at the lines above.
# print_nodes()

def place_node(x,y,name):
	name = name.lower() # You can put in either the description or the lowercase name.
	world[str(x)+","+str(y)] = nodes[name]["description"]
	
def get_node(x,y):
	if str(int(x))+","+str(int(y)) in world:
		return(world[str(int(x))+","+str(int(y))])
	else:
		return("Void")
	
def get_player_x():
	scrollcheck = scrollx%16
	if scrollcheck > 8:
		return int(scrollx/16)+1
	else:
		return int(scrollx/16)
		
def get_player_y():
	return(scrolly/16)
# Generate a 2d world

maplimitx1 = -50
maplimitx2 = 50
maplimity1 = -50
maplimity2 = 50

def mapgen(grass,stone,air,iron,gold,tree,leaves,water,sand,tallgrass):
	MAPGEN_WATER = 0
	MAPGEN_BIOME = "Grassy"
	#PREMAPGEN
	x = maplimitx1-1
	while x != maplimitx2+1:
		y = maplimity1-1
		while y != maplimity2+1:
			place_node(x,y,air)
			y += 1
		x += 1
	#MAPGEN
	x = maplimitx1
	while x != maplimitx2:
		y = maplimity1
		while y != maplimity2:
			if y == 1 and y > 0:
				if random.randint(1,10) == 1 and MAPGEN_WATER == 0:
					MAPGEN_WATER = 1
				if random.randint(1,7) == 1 and MAPGEN_WATER == 1:
					MAPGEN_WATER = 0
				if MAPGEN_WATER == 0:
					if get_node(x-1,y).lower() == water:
						place_node(x,y,sand)
						place_node(x-1,y-1,sand)
					else:
						if random.randint(1,10) == 1 and MAPGEN_BIOME == "Grassy":
							MAPGEN_BIOME = "Desert"
						if random.randint(1,7) == 1 and MAPGEN_BIOME == "Desert":
							MAPGEN_BIOME = "Grassy"
						if MAPGEN_BIOME == "Grassy":
							place_node(x,y,grass)
						elif MAPGEN_BIOME == "Desert":
							place_node(x,y,sand)
							if random.randint(1,2) == 1:
								place_node(x,y-1,sand)
				else:
					if get_node(x-1,y).lower() == grass:
						place_node(x,y,sand)
					else:
						if random.randint(1,3) == 2 and get_node(x-1,y).lower() != sand:
							place_node(x,y,water)
							place_node(x,y-1,water)
							place_node(x,y-2,sand)
						else:
							place_node(x,y,water)
							place_node(x,y-1,sand)
				if random.randint(1,5) == 1 and MAPGEN_WATER == 0 and MAPGEN_BIOME == "Grassy":
					treeheight = 1
					for i in range(1,random.randint(3,4)):
						place_node(x,y+i,tree)
						treeheight += 1
					place_node(x,y+treeheight,leaves)
					place_node(x+1,y+treeheight-1,leaves)
					place_node(x-1,y+treeheight-1,leaves)
				elif random.randint(1,5) == 1 and MAPGEN_WATER == 0 and MAPGEN_BIOME == "Grassy": # You may wonder what is different here. This new random will be different from the first, which causes this to work. Don't code like this, though.
					place_node(x,y+1, tallgrass)
				elif random.randint(1,5) == 1 and MAPGEN_WATER == 0 and MAPGEN_BIOME == "Desert":
					place_node(x,y+1,"cactus")
					place_node(x,y+2,"cactus") # Meh, forget asking for cactus name. I think I'll stop using arguments for this function eventually.
			elif y < 1 and y > -11:
				place_node(x,y,stone)
			elif y < -10:
				randoint = random.randint(1,15)
				if randoint < 2:
					place_node(x,y,iron)
				elif randoint == 15 and y < -5:
					place_node(x,y,gold)
				else:
					place_node(x,y,stone)
			else:
				if get_node(x,y).lower()== air:
					place_node(x,y,air)
			y += 1
		x += 1
	return
	
def print_world():
	for x in world:
		print world[x]
	return

mapgen("grass","stone","air","iron","gold","tree","leaves","water","sand","tallgrass")

hints = ["Logs can be used as one way ladders. You can jump without falling.","There is no method of healing, yet.","The code is open source.","There is no need to memorize craft recipes, just use the menu.","Only falling and cactus causes damage.","Don't punch the cactus, unless you have a pick.","Playing the game isn't much fun. Developing it is better."]
print("HAVE FUN!")
"""pygame window stuff"""
size = width,height = 600,400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Building Blocks")
flags = {"mute":False,"mode":"Creative"}
def menu():
	menubutton = Rect(300,200,50,30)
	soundbutton = Rect(300,250,62,23)
	exitbutton = Rect(300,300,41,23)
	modebutton = Rect(300,350,127,37)
	leave = 0
	hintnumber = random.randint(0,len(hints)-1)
	while leave != 1:
		screen.blit(pygame.image.load("textures/menu.png"),(0,0))
		screen.blit(pygame.image.load("textures/Menu/Play!.png"),(300,200))
		screen.blit(pygame.image.load("textures/Menu/Sound_"+str(flags["mute"])+".png"),(300,250))
		screen.blit(pygame.image.load("textures/Menu/Exit_up.png"),(300,300))
		screen.blit(pygame.image.load("textures/Menu/"+flags["mode"]+".png"),(300,350))
		write(hints[hintnumber],30,30)
		mouse_x,mouse_y = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# print(mouse_x,mouse_y)
				if pygame.Rect.collidepoint(menubutton,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					screen.blit(pygame.image.load("textures/Menu/PLAY!.png"),(300,200))
					pygame.display.flip()
					time.sleep(0.5)
					screen.blit(pygame.image.load("textures/Menu/Play!.png"),(300,200))
					pygame.display.flip()
					time.sleep(1)
					leave = 1
				if pygame.Rect.collidepoint(soundbutton,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					print("Sound (Un)Muting!")
					flags["mute"] = not flags["mute"]
				if pygame.Rect.collidepoint(exitbutton,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					print(";( Goodbye.")
					screen.blit(pygame.image.load("textures/Menu/Exit_down.png"),(300,200))
					time.sleep(0.5)
					sys.exit()
				if pygame.Rect.collidepoint(modebutton,(mouse_x,mouse_y)):
					if flags["mode"] == "Creative":
						flags["mode"] = "Survival"
					else:
						flags["mode"] = "Creative"
					print("Okay, "+flags["mode"]+" mode it is!")
		pygame.display.flip()

def craft():
	woodpick = Rect(300,200,16,16)
	woodbutton = Rect(300,250,16,16)
	door1button = Rect(250,250,16,32)
	door2button = Rect(350,250,12,32)
	exitbutton = Rect(300,300,41,23)
	saplingbutton = Rect(250,200,41,23)
	infotext = ""
	leave = 0
	while leave != 1:
		screen.blit(pygame.image.load("textures/craft.png"),(0,0))
		screen.blit(pygame.image.load("textures/Pick_Wood.png"),(300,200))
		screen.blit(pygame.image.load("textures/Wood.png"),(300,250))
		screen.blit(pygame.image.load("textures/Door.png"),(250,250))
		screen.blit(pygame.image.load("textures/Door2.png"),(350,250))
		screen.blit(pygame.image.load("textures/Menu/Exit_up.png"),(300,300))
		screen.blit(pygame.image.load("textures/Sapling.png"),(250,200))
		mouse_x,mouse_y = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# print(mouse_x,mouse_y)
				if pygame.Rect.collidepoint(woodbutton,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					if not "wood" in inventory:
						inventory["wood"] = 0
					if "tree" in inventory:
						if inventory["tree"] >= 1:
							print("You have crafted some wood.")
							inventory["wood"] += 4
							inventory["tree"] -= 1
							infotext = "Wood is made from trees."
						else:
							infotext = "You do not have enough items."
					else:
						inventory["tree"] = 0
						infotext = "You do not have enough items."
				if pygame.Rect.collidepoint(woodpick,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					if "wood" in inventory:
						if inventory["wood"] >= 4:
							print("You have crafted a pick.")
							inventory["pick"] = "Pick_Wood"
							inventory["wood"] -= 4
							infotext = "With a wood pick, you can mine stone and ore."
						else:
							infotext = "You do not have enough items."
					else:
						inventory["wood"] = 0
						infotext = "You do not have enough items."
				if pygame.Rect.collidepoint(saplingbutton,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					if not "sapling" in inventory:
						inventory["sapling"] = 0
					if "leaves" in inventory:
						if inventory["leaves"] >= 1:
							print("You have crafted a sapling.")
							inventory["sapling"] += 1
							inventory["leaves"] -= 1
							infotext = "Plant saplings to make more trees. You will need lots of trees"
						else:
							infotext = "You need to mine leaves for saplings. Get more leaves from trees."
					else:
						inventory["leaves"] = 0
						infotext = "You need to mine leaves for saplings. Get more leaves from trees."
				if pygame.Rect.collidepoint(door1button,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					if not "door" in inventory:
						inventory["door"] = 0
					if "wood" in inventory:
						if inventory["wood"] >= 6:
							print("You have crafted a door.")
							inventory["door"] += 1
							inventory["wood"] -= 6
							infotext = "This is a right side door. Doors can be opened and closed with a right click."
						else:
							infotext = "You do not have enough items."
					else:
						inventory["wood"] = 0
						infotext = "You do not have enough items."
				if pygame.Rect.collidepoint(door2button,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					if not "door2" in inventory:
						inventory["door2"] = 0
					if "wood" in inventory:
						if inventory["wood"] >= 6:
							print("You have crafted a door.")
							inventory["door2"] += 1
							inventory["wood"] -= 6
							infotext = "This is a left side door. Doors can be opened and closed with a right click."
						else:
							infotext = "You do not have enough items."
					else:
						inventory["wood"] = 0
						infotext = "You do not have enough items."
				if pygame.Rect.collidepoint(exitbutton,(mouse_x,mouse_y)):
					play_sound("sounds/click.ogg")
					print("Okay, Crafting Completed.")
					screen.blit(pygame.image.load("textures/Menu/Exit_down.png"),(300,200))
					time.sleep(0.5)
					leave = 1
		write(infotext,30,30)
		pygame.display.flip()

menu()
ychange = -1
timer = 0
scrollx = 0
scrolly = 0
direction = ["right","","0"]
jumpyness = 0
selectnode = "stone"
selectvar = 1
health = 3
gametime = 3000
selectlist = ["stone","grass","iron","gold","brick","tree","backwall","water","sand","door","door2","wood","sapling"]
inventory = {"pick":""}
pygame.key.set_repeat(1, 2)
gravitytimer = 0
dropthrough = ["Air","Water","FlowingWater","BackWall","TallGrass"]
old_top_text = ""
top_text = ""
top_text_timer = 0
## Functions to make it easier.
def get_node_passible(x,y,modder):
	if "passthrough" in nodes[get_node(x+modder,y).lower()]:
		return True
	else:
		return False
## End of Functions
while True:
	gametime += 1
	if gametime > 12000:
		gametime = 0
	if gametime > 3000 and gametime < 10000:
		screen.fill((125,125,255)) # Day
	elif (gametime < 3001 and gametime > 2250) or (gametime > 10000 and gametime < 10250):
		screen.fill((255,125,125)) # Dawn or Dusk
	else:
		screen.fill((50,50,100)) # Night
	write(top_text,10,10) # This is the text that appears up at the top of the screen. Usefull for messages to the player.
	if top_text != old_top_text:
		top_text_timer = 300
	old_top_text = top_text
	top_text_timer -= 1
	if top_text_timer <= 0:
		top_text = ""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# Quit
			sys.exit()
		elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_LEFT]:
			# Go left
			direction[0] = "left"
			direction[1] = ""
			if get_node_passible((scrollx/16),(scrolly/16)+1,1) and get_node_passible((scrollx/16),(scrolly/16)+2,1):
				if get_node(get_player_x(),get_player_y()) == "Water" or get_node(get_player_x(),get_player_y()) == "FlowingWater":
					scrollx += 2
					ychange += 1
					if ychange > 3:
						ychange = -1
					scrolly += ychange
				else:
					scrollx += 2
		elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_RIGHT]:
			direction[0] = "right"
			direction[1] = ""
			# Go right
			if get_node_passible((scrollx/16),(scrolly/16)+1,0) and get_node_passible((scrollx/16),(scrolly/16)+2,0):
				if get_node(get_player_x(),get_player_y()) == "Water" or get_node(get_player_x(),get_player_y()) == "FlowingWater":
					scrollx -= 2
					ychange += 1
					if ychange > 3:
						ychange = -1
					scrolly += ychange
				else:
					scrollx -= 2
		elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_UP]:
			# Jump
			if get_node(scrollx/16,scrolly/16) != "Air" and get_node_passible(get_player_x(),get_player_y()+3,0):
				if get_node(get_player_x(),get_player_y()) == "Water" or get_node(get_player_x(),get_player_y()) == "FlowingWater":
					scrolly += 2
				else:
					scrolly += 28
					gravitytimer = 0
		elif event.type == pygame.KEYDOWN and event.key == K_g:
			# Find the node under the player and print it (if you are using a terminal)
			print(get_node(scrollx/16,scrolly/16))
			print scrolly
		elif event.type == pygame.KEYDOWN and event.key == K_c:
			# Change Clothing
			if direction[2] == "0":
				direction[2] = "1"
			elif direction[2] == "1":
				direction[2] = "2"
			elif direction[2] == "2":
				direction[2] = "0"
		elif event.type == pygame.KEYDOWN and event.key == K_m:
			# Make stuff, or craft if your from minecraft.
			craft()
		elif event.type == pygame.KEYDOWN and event.key == K_s:
			# Save
			play_sound("sounds/Save.wav")
			WorldSave = open("world/world.txt","wb")
			WorldSave.write(json.dumps(world))
			
			WorldSave.close()
			pos_and_gametime = {"pos":str(scrollx) + "," + str(scrolly),"gametime":gametime,"inventory":inventory}
			PosSave = open("world/pos.txt","wb")
			PosSave.write(json.dumps(pos_and_gametime))
			
			PosSave.close()
			top_text = "Saved."
		elif event.type == pygame.KEYDOWN and event.key == K_l:
			# Load
			try:
				play_sound("sounds/Load.wav")
				WorldSave = open("world/world.txt","r")
				iterate = 0
				world = json.loads(WorldSave.read())
				WorldSave.close()
				PosSave = open("world/pos.txt","r")
				pos_and_gametime = json.loads(PosSave.read())
				newplayerpos = pos_and_gametime["pos"]
				newplayerx,newplayery = newplayerpos.split(",")
				scrollx = int(newplayerx)
				scrolly = int(newplayery)
				gametime = pos_and_gametime["gametime"]
				inventory = pos_and_gametime["inventory"]
				PosSave.close()
				top_text = "Load Complete"
			except:
				top_text = "Load Failure, maybe your file is old?"
		elif event.type == pygame.KEYDOWN and event.key == K_n:
			# Make a new world, so you don't need to restart.
			top_text = "Are you sure? Press Y to confirm, or press any key to stop."
			end = 0
			while end != 1:
				write(top_text,10,10)
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN and event.key == K_y:
						mapgen("grass","stone","air","iron","gold","tree","leaves","water","sand","tallgrass")
						end = 1
					elif event.type == pygame.KEYDOWN and event.key != K_y:
						end = 1
				pygame.display.flip()
						
			top_text = "Created another world."
			gametime = 3000
		elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
			# Change selected item
			selectvar += 1
			if selectvar > len(selectlist) -1:
				selectvar = 0
			selectnode = selectlist[selectvar]
		elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
			# Pause and go to the menu.
			menu()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# Build or dig
			mouse_x,mouse_y = pygame.mouse.get_pos()
			spos = sx,sy = (int(round((-(mouse_x/16)+19.7)+scrollx/16)),int(round((-(mouse_y/16)+14.7)+scrolly/16)))
			if event.button == 1: # Dig or Build
				if get_node(sx,sy) == "Air" or get_node(sx,sy) == "Water" or get_node(sx,sy) == "FlowingWater":
					if selectnode in inventory and flags["mode"] == "Survival" and inventory[selectnode] > 0:
						place_node(sx,sy,selectnode)
						inventory[selectnode] -= 1
					elif flags["mode"] == "Creative":
						place_node(sx,sy,selectnode)
					direction[1] = "build"
					if flags["mute"] == False:
						play_sound("sounds/place.ogg")
				else:
					if get_node(sx,sy).lower() in inventory:
						if inventory["pick"] != "" or nodes[get_node(sx,sy).lower()]["hard"] == "no" or flags["mode"] == "Creative":
							inventory[get_node(sx,sy).lower()] += 1
							old_node = get_node(sx,sy)
							place_node(sx,sy,"air")
							if inventory["pick"] == "" and "ow" in nodes[old_node.lower()] and flags["mode"] == "Survival":
								health -= 1
					else:
						if inventory["pick"] != "" or nodes[get_node(sx,sy).lower()]["hard"] == "no" or flags["mode"] == "Creative":
							inventory[get_node(sx,sy).lower()] = 1
							place_node(sx,sy,"air")
					direction[1] = "pick"
					if flags["mute"] == False:
						play_sound("sounds/dig.ogg")
			elif event.button == 3: # Open Doors, press buttons, etc.
				if get_node(sx,sy) == "Door":
					place_node(sx,sy,"door_closed")
				elif get_node(sx,sy) == "Door_Closed":
					place_node(sx,sy,"door")
				if get_node(sx,sy) == "Door2":
					place_node(sx,sy,"door_closed2")
				elif get_node(sx,sy) == "Door_Closed2":
					place_node(sx,sy,"door2")
					
			 	
	scrollcheck = (scrollx%16)
	# Gravity
	if get_node(get_player_x(),get_player_y()) in dropthrough:
		gravityon = True
		if get_node(get_player_x(),get_player_y()) == "Water" or get_node(get_player_x(),get_player_y()) == "FlowingWater":
			scrolly -= 1
			gravitytimer = 0
		else:
			gravitytimer += 1
			scrolly -= 4
	else:
		gravityon = False
		if gravitytimer > 30 and flags["mode"] == "Survival":
			play_sound("sounds/damage.ogg")
			health -= 1
			if gravitytimer > 60: # If I fell even farther, give even more damage.
				health -= 1
		gravitytimer = 0
		
	if not gravityon: # Puts you strait on the ground if you missed it.
		scrolly += scrolly%16 - 12
		if (not get_node(get_player_x(),get_player_y() + 1) in dropthrough) and not get_node_passible(get_player_x(),get_player_y()+1,0):
			scrolly += 16
	if scrolly > -290:
		screen.blit(pygame.image.load("textures/Underground.png"),(0,scrolly+((int(300)-14.5)))) # Makes underground dark.
	else:
		screen.blit(pygame.image.load("textures/Underground.png"),(0,0)) # Makes underground dark.
	# ABMs, Physics, Block drawing, etc.
	for block in world:
		x, y = block.split(",")[:2]
		# Do water and sand physics
		if world[block] == "Water":
			if get_node(x,int(y)-1) != "Air":
				if get_node(int(x)-1,y) == "Air":
					place_node(int(x)-1,y,"flowingwater")
				if get_node(int(x)+1,y) == "Air":
					place_node(int(x)+1,y,"flowingwater")
			else:
				place_node(x,int(y)-1,"flowingwater")
			if get_node(x,int(y)-1) == "Air" or get_node(x,int(y)-1) == "FlowingWater":
				place_node(x,int(y)-1, "water")
		if world[block] == "FlowingWater":
			if get_node(x,int(y)-1) != "Air":
				if get_node(int(x)-1,y) == "Air" and (get_node(int(x),int(y)-1) != "Air" and get_node(int(x),int(y)-1) != "Water" and get_node(int(x),int(y)-1) != "FlowingWater"):
					place_node(int(x)-1,y,"flowingwater")
				if get_node(int(x)+1,y) == "Air" and (get_node(int(x),int(y)-1) != "Air" and get_node(int(x),int(y)-1) != "Water" and get_node(int(x),int(y)-1) != "FlowingWater"):
					place_node(int(x)+1,y,"flowingwater")
			if get_node(x,int(y)-1) == "Air" or get_node(x,int(y)-1) == "FlowingWater":
				place_node(x,int(y)-1, "water")
		if world[block] == "Sand" and timer == 10:
			if get_node(x,int(y)-1) == "Air" or get_node(x,int(y)-1) == "TallGrass":
				place_node(x,y,"air")
				place_node(x,int(y)-1,"sand")
		# Grow Saplings
		if world[block] == "Sapling" and timer == 10 and random.randint(1,10) == 1:
			place_node(x,y,"tree")
			place_node(x,int(y)+1,"tree")
			if random.randint(1,3) == 3:
				place_node(x,int(y)+2,"tree")
				place_node(int(x)+1,int(y)+2,"leaves")
				place_node(int(x)-1,int(y)+2,"leaves")
				place_node(x,int(y)+3,"leaves")
			else:
				place_node(int(x)+1,int(y)+1,"leaves")
				place_node(int(x)-1,int(y)+1,"leaves")
				place_node(x,int(y)+2,"leaves")
		# Render blocks
		if world[block] != "Air":
			if scrollx+((int(x)-20) * -16) < 610 and scrollx+((int(x)-20) * -16) > -10:
				if scrolly+((int(y)-14)* -16) < 410 and scrolly+((int(y)-14)* -16) > -30:
					screen.blit(pygame.image.load("textures/" + world[block] + ".png"),(scrollx+((int(x)-19.5) * -16),scrolly+((int(y)-14.5)* -16)))
	if flags["mode"] == "Survival": # Hearts, Death Screen and Respawn.
		if health > 2:
			screen.blit(pygame.image.load("textures/player/heart.png"),(20,20))
		if health > 1:
			screen.blit(pygame.image.load("textures/player/heart.png"),(35,20))
		if health > 0:
			screen.blit(pygame.image.load("textures/player/heart.png"),(50,20))
		if health <= 0:
			screen.blit(pygame.image.load("textures/Death.png"),(250,250))
			health = 0
		if health == 0 and timer == 15:
			health = 3
			scrollx = 0
			scrolly = 0
	# Render the player
	player = pygame.transform.scale(pygame.image.load("textures/player/playerleft" + direction[1] + direction[2] + ".png"),(32,40))
	if direction[0] == "right":
		# If he is pointing in another direction, turn around.
		player = pygame.transform.flip(player,True,False)
	screen.blit(player,(306,204))
	screen.blit(pygame.image.load("textures/BlockSelect.png"),(550,25))
	screen.blit(pygame.image.load("textures/" + nodes[selectnode]["description"] + ".png"),(552,27))
	if flags["mode"] == "Survival":
		xadd = 0
		if selectnode in inventory:
			for letter in str(inventory[selectnode]):
				screen.blit(pygame.image.load("textures/Numbers/"+letter+".png"),(535+xadd,40))
				xadd += 10
		else:
			screen.blit(pygame.image.load("textures/Numbers/0.png"),(535,40))
		if not inventory["pick"] == "":
			screen.blit(pygame.image.load("textures/" + inventory["pick"] + ".png"),(552,47))
	# Timer for certain things.
	if timer >= 15:
		timer = 0
	timer += 1
	if scrolly > -50: # If you aren't underground, then show the sky.
		# The Dark. At night time. (And some stars.)
		if gametime > 10250:
			screen.blit(pygame.image.load("textures/TheDark.png"),(0,0))
			screen.blit(pygame.image.load("textures/Stars.png"),((gametime - 10250)/10,0))
			screen.blit(pygame.image.load("textures/Stars.png"),(((gametime - 10250)/10) - 400,0))
		if gametime < 2250:
			screen.blit(pygame.image.load("textures/TheDark.png"),(0,0))
			screen.blit(pygame.image.load("textures/Stars.png"),((gametime + 175)/10,0))
			screen.blit(pygame.image.load("textures/Stars.png"),(((gametime + 175)/10) - 400,0))
		# The sun. At day time.
		if gametime > 3000 and gametime < 10000:
			screen.blit(pygame.image.load("textures/Sun.png"),((gametime - 3000)/17.5,10))
	# Update the screen.
	pygame.display.flip()