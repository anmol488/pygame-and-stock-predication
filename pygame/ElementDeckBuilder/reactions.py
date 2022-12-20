from draw import element_list
all_elements = tuple(x[0] for x in element_list)
# getting every element through list comprehension, used for black hole
# can later be used as a tagging system (e.g. living, ocean, etc.) to do a filter before going through 
#   the synergy list to reduce lag when going to next cycle

synergy_list = [
    #((Element 1, Element 2), (Replacement 1, Replacement 2), Money from Replacement)
    # Note: Element 1/2 can either be one element or possible elements available for the reaction.
    #           If the reaction is not a replacement reaction, meaning the elements stay the same
    #           but there is gold earnt from it (an adjacency bonus reaction), 
    #           (Replacement 1, Replacement 2) should be ("No Change")
    #   Element 1 --> Replacement 1, Element 2 --> Replacement 2.
    (("Earth", "Air"), ("Dust", "Empty"), 3), 
    (("Fire", "Air"), ("Energy", "Empty"), 3), 
    (("Light", ("Light", "Air", "Fire")), ("Energy", "Empty"), 15), 
    (("Fire", "Cold"), ("Air", "Empty"), 3), 
    (("Earth", "Fire"), ("Lava", "Empty"), 3), 
    (("Fire", "Fire"), ("Light", "Empty"), 3), 
    (("Earth", "Water"), ("Clay", "Empty"), 3), 
    (("Water", ("Fire", "Energy")), ("Steam", "Empty"), 3), 
    (("Rain", "Fire"), ("No Change", "Steam"), 3), 
    (("Steam", "Cold"), ("Water", "Empty"), 3),
    (("Energy", "Cold"), ("Empty", "Empty"), 25),
    (("Lava", "Water"), ("Stone", "Steam"), 3), 
    (("Sun", "Cold"), ("No Change", "Water"), 3), 
    (("Sun", "Water"), ("No Change", "Steam"), 3), 
    (("Sun", ("Light", "Energy")), ("No Change"), 5), 
    (("Lava", "Cold"), ("Stone", "Empty"), 3),  
    (("Stone", "Fire"), ("Metal", "Empty"), 3),
    (("Dust", "Dust"), ("Sand", "Empty"), 3), 
    (("Dust", "Sandstorm"), ("Sand", "No Change"), 3), 
    (("Wind", ("Dust", "Ash", "Tumbleweed")), ("Wind", "Empty"), 5), 
    (("Metal", "Energy"), ("Electricity", "Empty"), 3), 
    (("Gold", "Gold"), ("No Change"), 5), 
    (("Steam", "Steam"), ("Cloud", "Empty"), 3), 
    (("Cloud", ("Steam", "Cloud", "Water")), ("Rain", "Empty"), 3), 
    ((("Rain", "Cloud"), ("Electricity", "Energy")), ("Thunder", "Empty"), 3), 
    (("Thunder", "Rain"), ("No Change"), 8), 
    (("Sun", ("Cloud", "Rain", "Thunder")), ("No Change"), 5),
    (("Cloud", ("Rain", "Thunder")), ("No Change"), 5),
    (("Rain", "Rain"), ("Thunder", "Empty"), 3),  
    (("Thunder", "Thunder"), ("No Change"), 6),
    ((("Rain", "Thunder", "Cloud"), "Wind"), ("Empty", "Empty"), 200),  
    ((("Energy", "Light"), ("Energy", "Light")), ("Sun", "Empty"), 3), 
    
    (("Sun", "Sun"), ("Black Hole", "Empty"), 3), 
    (("Black Hole", "Black Hole"), ("Empty", "Empty"), 0), 
    ((all_elements, "Black Hole"), ("Empty", "Empty"), -250),
    
    # pyromaniac    
    ((("Fire", "Electricity"), ("Wood", "Boat", "House")), ("Fire", "Coal"), 30), 
    (("Fire", ("Tree", "Electricity")), ("Fire", "Coal"), 80), 
    (("Fire", ("Forest", "Electricity")), ("Fire", "Coal"), 250), 
    ((("Fire", "Phoenix", "Volcano", "Lava"), ("Plants", "Dust", "Cactus", "Tumbleweed")), ("No Change", "Ash"), 50),
    
    (("Phoenix", ("Wood", "Boat", "House")), ("Phoenix", "Coal"), 30), 
    (("Phoenix", "Tree"), ("Phoenix", "Coal"), 80), 
    (("Phoenix", "Forest"), ("Phoenix", "Coal"), 250), 

    (("Coal", "Water"), ("Oil", "Empty"), 3), 
    (("Coal", "Air"), ("Natural Gas", "Empty"), 3), 

    (("Fire", "Coal"), ("Fire", "Carbon Dioxide"), 150), 
    (("Fire", "Oil"), ("Fire", "Carbon Dioxide"), 175), 
    (("Fire", "Natural Gas"), ("Fire", "Carbon Dioxide"), 200), 

    (("Fire", "Alcohol"), ("Fire", "Fire"), 75), 

    # cold things
    (("Water", "Air"), ("Cold", "Empty"), 3), 
    (("Water", "Cold"), ("Ice", "Empty"), 3), 
    (("Rain", ("Cold", "Ice")), ("Snow", "Empty"), 3), 
    (("Cloud", ("Cold", "Ice")), ("Snow", "Empty"), 3), 
    (("Snow", ("Energy", "Landslide")), ("Avalanche", "Empty"), 3), 
    (("Snow", "Human"), ("Snowman", "Human"), 3), 
    (("Avalanche", "Blizzard"), ("Snow", "Snow"), 15), 
    (("Earth", ("Ice", "Snow", "Cold")), ("Permafrost", "Empty"), 3), 
    (("Ice", "Snow"), ("Glacier", "Empty"), 3), 

    (("Snow", "Snow"), ("No Change"), 4), 
    (("Glacier", "Ocean"), ("No Change"), 3), 
    (("Snowman", "Snowman"), ("No Change"), 3), 
    (("Snow", ("Glacier", "Permafrost", "Snowman", "Avalanche")), ("No Change"), 5), 
    ((("Glacier", "Permafrost"), "Cold"), ("No Change"), 5), 
    (("Glacier", "Glacier"), ("No Change"), 5),  
    (("Permafrost", "Permafrost"), ("No Change"), 3), 
    (("Penguin", ("Permafrost", "Snow", "Glacier", "Ocean", "Cold", "Ice")), ("No Change"), 5), 

    # cold synergy with fire & carbon dioxide
    ((("Fire", "Energy"), ("Snow", "Snowman", "Avalanche", "Glacier")), ("Empty", "Water"), 150),
    ((("Fire", "Energy"), "Permafrost"), ("Carbon Dioxide", "Earth"), 150), 
    ((("Phoenix", "Sun"), ("Snow", "Snowman", "Avalanche", "Glacier")), ("No Change", "Water"), 150),
    ((("Phoenix", "Sun"), "Permafrost"), ("No Change", "Earth"), 150), 
    (("Volcano", ("Snow", "Snowman", "Avalanche", "Glacier", "Lake", "Wave", "Tsunami")), ("Mountain", "Water"), 150),
    (("Volcano", "Permafrost"), ("Mountain", "Earth"), 150), 
    (("Lava", ("Snow", "Snowman", "Avalanche", "Glacier")), ("Stone", "Water"), 150), 
    (("Lava", "Permafrost"), ("Stone", "Earth"), 150), 

    ((("Glacier", "Permafrost", "Snow", "Ice", "Snowman", "Avalanche"), "Carbon Dioxide"), 
                ("No Change", "Empty"), 25), 

    # ice kingdom
    (("Ice", "Ice"), ("Ice Brick", "Empty"), 3),  
    (("Ice Brick", "Ice Brick"), ("Ice Wall", "Empty"), 3),  
    (("Ice Wall", "Ice Wall"), ("Ice Building", "Empty"), 3),  
    (("Ice Building", "Ice Building"), ("Ice Mansion", "Empty"), 3),  
    (("Ice Mansion", "Ice Mansion"), ("Ice Palace", "Empty"), 3),    

    (("Ice", ("Glacier", "Permafrost", "Penguin", "Snowman", "Avalanche", "Blizzard", "Cold")), 
        ("No Change"), 2), 
    (("Ice Brick", ("Snow", "Ice", "Glacier", "Permafrost", "Penguin", "Snowman", "Avalanche", "Cold", "Blizzard")), 
        ("No Change"), 3), 
    (("Ice Wall", ("Snow", "Ice", "Ice Brick", "Glacier", "Permafrost", "Penguin", "Snowman", "Avalanche", "Cold", 
        "Blizzard")), ("No Change"), 5), 
    (("Ice Building", ("Snow", "Ice", "Ice Brick", "Ice Wall", "Glacier", "Permafrost", "Penguin", "Snowman", 
        "Avalanche", "Cold", "Blizzard")), ("No Change"), 7),
    (("Ice Mansion", ("Snow", "Ice", "Ice Brick", "Ice Wall", "Ice Building", "Glacier", "Permafrost", "Penguin", 
        "Snowman", "Avalanche", "Cold", "Blizzard")), ("No Change"), 9), 
    (("Ice Palace", ("Snow", "Ice", "Ice Brick", "Ice Wall", "Ice Building", "Ice Mansion", "Glacier", "Permafrost", 
        "Penguin", "Snowman", "Avalanche", "Cold", "Blizzard")), ("No Change"), 12), 

    (("Ice", ("Fire", "Energy")), ("Water", "Empty"), 5), 
    (("Ice Brick", ("Fire", "Energy")), ("Water", "Empty"), 40), 
    (("Ice Wall", ("Fire", "Energy")), ("Water", "Empty"), 135), 
    (("Ice Building", ("Fire", "Energy")), ("Water", "Empty"), 320), 
    (("Ice Mansion", ("Fire", "Energy")), ("Water", "Empty"), 625), 
    (("Ice Palace", ("Fire", "Energy")), ("Water", "Empty"), 1080), 

    (("Ice", "Lava"), ("Water", "Stone"), 5), 
    (("Ice Brick", "Lava"), ("Water", "Stone"), 40), 
    (("Ice Wall", "Lava"), ("Water", "Stone"), 135), 
    (("Ice Building", "Lava"), ("Water", "Stone"), 320), 
    (("Ice Mansion", "Lava"), ("Water", "Stone"), 625), 
    (("Ice Palace", "Lava"), ("Water", "Stone"), 1080), 

    (("Ice", "Volcano"), ("Water", "Mountain"), 5), 
    ((("Ice Brick", "Snow"), "Volcano"), ("Water", "Mountain"), 40), 
    (("Ice Wall", "Volcano"), ("Water", "Mountain"), 135), 
    (("Ice Building", "Volcano"), ("Water", "Mountain"), 320), 
    (("Ice Mansion", "Volcano"), ("Water", "Mountain"), 625), 
    (("Ice Palace", "Volcano"), ("Water", "Mountain"), 1080), 

    (("Ice", ("Phoenix", "Sun")), ("Water", "No Change"), 5), 
    (("Ice Brick", ("Phoenix", "Sun")), ("Water", "No Change"), 40), 
    (("Ice Wall", ("Phoenix", "Sun")), ("Water", "No Change"), 135), 
    (("Ice Building", ("Phoenix", "Sun")), ("Water", "No Change"), 320), 
    (("Ice Mansion", ("Phoenix", "Sun")), ("Water", "No Change"), 625), 
    (("Ice Palace", ("Phoenix", "Sun")), ("Water", "No Change"), 1080), 

    (("Ice Building", ("Human", "Angler", "Miner", "Hero")), ("No Change"), 3), 
    (("Ice Mansion", ("Royalty", "Hero")), ("No Change"), 10), 
    (("Ice Palace", "Royalty"), ("No Change"), 20), 

    # living (or close enough) things:
    (("Clay", "Energy"), ("Life", "Empty"), 3), 

    (("Metal", "Gold"), ("Circuit", "Empty"), 3),                 # robotic
    (("Metal", ("Life", "Circuit", "Electricity")), ("Robot", "Empty"), 3),
    (("Circuit", ("Circuit", "Electricity", "Robot", "Metal", "Gold")), ("AI", "Empty"), 3), 
    ((("Robot", "Circuit"), "AI"), ("Android", "Empty"), 3), 
    ((("AI", "Robot"), "Music"), ("Vocaloid", "Empty"), 3), 
    
    ((("Electricity", "Circuit"), "Gold"), ("No Change"), 5), 
    (("Metal", "Electricity"), ("No Change"), 6), 
    ((("Robot", "AI", "Vocaloid", "Android"), ("Electricity", "Metal", "Circuit")), ("No Change"), 9), 

    (("Stone", "Life"), ("Egg", "Empty"), 3),             # animals
    (("Egg", ("Fire", "Air", "Wind", "Energy")), ("Bird", "Empty"), 3), 
    (("Egg", "Sun"), ("Bird", "No Change"), 3), 
    (("Egg", "Life"), ("Bird", "Empty"), 100), 
    (("Egg", "Love"), ("Bird", "Empty"), 200), 
    (("Bird", "Stone"), ("Bird", "Egg"), 3), 
    ((("Bird", "Egg"), ("Snow", "Ice", "Cold")), ("Penguin", "Empty"), 3), 
    (("Bird", ("Air", "Wind")), ("No Change"), 5), 
    ((("Egg", "Bird"), "Water"), ("Fish", "Empty"), 3),
    ((("Bird", "Egg"), "Ocean"), ("Fish", "Ocean"), 3), 
    (("Beast", "Ocean"), ("Turtle", "Ocean"), 3), 
    (("Beast", "Water"), ("Turtle", "Empty"), 3), 
    (("Fish", ("Earth", "Stone")), ("Turtle", "Empty"), 3), 
    ((("Bird", "Egg"), ("Earth", "Mountain")), ("Beast", "Empty"), 3),
    ((("Egg", "Bird"), "Lava"), ("Phoenix", "Empty"), 3),  
    (("Bird", ("Fire", "Lava", "Life")), ("Phoenix", "Empty"), 3), 
    (("Beast", ("Bird", "Penguin")), ("Dragon", "Empty"), 3), 
    (("Light", "Life"), ("Will o' Wisp", "Empty"), 3), 

    (("Earth", "Life"), ("Plants", "Empty"), 3),            # nature
    (("Sand", ("Plants", "Seeds")), ("Cactus", "Empty"), 3),
    (("Plants", "Wind"), ("Tumbleweed", "Empty"), 3), 
    (("Tree", "Tree"), ("Forest", "Empty"), 3), 
    (("Seeds", ("Water", "Earth", "Rain", "Light")), ("Tree", "Empty"), 3),
    ((("Tree", "Forest"), "Life"), ("World Tree", "Empty"), 3), 
    (("Lake", ("Plants", "Tree", "Forest")), ("Swamp", "Empty"), 3),
    (("Swamp", ("Ocean", "Beach", "Lake")), ("Mangrove", "Empty"), 3),

    ((("Beast", "Bird", "Fish", "Turtle", "Bird"), "Plants"), ("No Change", "Seeds"), 30),
    ((("Bird", "Phoenix"), "Seeds"), ("No Change", "Empty"), 50), 

    ((("Earthquake", "Tsunami", "Hurricane", "Blizzard", "Sandstorm", "Duststorm", "Tornado", "Landslide", 
        "Avalanche"), "Tree"), ("Empty", "Wood"), 50), 
    ((("Earthquake", "Tsunami", "Hurricane", "Blizzard", "Sandstorm", "Duststorm", "Tornado", "Landslide", 
        "Avalanche"), ("Forest", "Mangrove", "Swamp")), ("Empty", "Wood"), 250), 

    (("Cactus", ("Sand", "Beach")), ("No Change"), 8), 
    (("Mangrove", ("Ocean", "Lake", "Beach")), ("No Change"), 5),

    ((("Mangrove", "Swamp"), ("Fish", "Turtle")), ("No Change"), 8),    
    ((("Mangrove", "Swamp", "Forest", "World Tree"), ("Bird", "Beast", "Dragon", "Will o' Wisp")), ("No Change"), 8),
    
    ((("Plants", "Mangrove", "Swamp", "Forest", "Tree"),  
        ("Plants", "Mangrove", "Swamp", "Forest")), ("No Change"), 5), 
    ((("Plants", "Mangrove", "Swamp", "Forest", "Tree", "Cactus", "World Tree"),  
        ("Water", "Light", "Ash")), ("No Change", "Empty"), 50),
    ((("Plants", "Mangrove", "Swamp", "Forest", "Tree", "Cactus", "World Tree"),  
        ("Sun", "Rain", "Earth", "Clay", "Seeds")), ("No Change"), 7), 
    (("World Tree", ("Plants", "Cactus", "Forest", "Tree", "World Tree", "Mangrove", "Swamp")), ("No Change"), 15),
    ((("Plants", "Mangrove", "Swamp", "Forest", "Tree", "Cactus", "World Tree"),  
        ("Love", "Music", "Vocaloid")), ("No Change"), 10),

    ((("Plants", "Forest", "Tree", "Cactus", "World Tree"), ("Carbon Dioxide")), ("No Change", "Empty"), 50),
    ((("Ocean", "Swamp", "Mangrove"), "Carbon Dioxide"), ("No Change", "Empty"), 50), 

    ((("Swamp", "Mangrove"), "Energy"), ("No Change", "Life"), 3), 

    (("Clay", "Life"), ("Human", "Empty"), 3),              # humans
    (("Human", "Human"), ("Love", "Empty"), 3), 
    (("Wood", "Wind"), ("Music", "Empty"), 3), 
    (("Wood", "Clay"), ("House", "Empty"), 3), 
    (("House", "House"), ("No Change"), 3), 
    (("House", ("Human", "Angler", "Miner")), ("No Change"), 15), 
    ((("Human", "Hero"), "Phoenix"), ("Hero", "Empty"), 300), 
    ((("Human", "Hero"), "Dragon"), ("Hero", "Empty"), 500), 
    (("Human", "Plants"), ("Human", "Alcohol"), 3), 
    (("Water", "Carbon Dioxide"), ("Cola", "Empty"), 3), 
    (("Human", "Fish"), ("Angler", "Fish"), 3), 
    (("Angler", "Fish"), ("Angler", "Empty"), 75), 
    (("Human", "Mountain"), ("Miner", "Mountain"), 3),
    (("Miner", "Mountain"), ("Miner", "Stone"), 3), 
    (("Miner", "Stone"), ("Miner", "Metal"), 3), 
    (("Miner", "Metal"), ("Miner", "Gold"), 3), 
    (("Miner", "Gold"), ("Miner", "Coal"), 3), 
    (("Human", "Gold"), ("Pirate", "Empty"), 3), 
    (("Pirate", "Gold"), ("Pirate", "Empty"), 100), 
    ((("Hero", "Angel"), "Pirate"), ("No Change", "Human"), 50), 
    (("Human", ("Light", "Bird")), ("Angel", "Empty"), 3), 
    ((("Human", "Angler", "Miner"), "Angel"), ("Royalty", "Empty"), 5),

    # consuming things
    ((("Human", "Hero", "Miner", "Angler", "Pirate", "Royalty"), ("Alcohol", "Cola")), ("No Change", "Empty"), 75),  
    (("Angel", "Cola"), ("Angel", "Empty"), 150), 
    (("Royalty", ("Alcohol", "Cola")), ("Royalty", "Empty"), 75), 
    ((("Dragon", "Phoenix"), ("Alcohol", "Cola")), ("No Change", "Empty"), 50), 

    ((("Human", "Miner", "Angler", "Pirate", "Hero", "Royalty", "Bird", "Beast", "Fish", "Turtle", "Penguin", 
        "Dragon", "Phoenix"), "Air"), ("No Change", "Carbon Dioxide"), 15), 
    
    (("Robot", "Robot"), ("No Change"), 3),                # synergies amongst selves
    ((("Robot", "AI"), "Android"), ("No Change"), 5), 
    (("Android", "Android"), ("No Change"), 3), 
    (("Vocaloid", "Vocaloid"), ("No Change"), 3),
    (("Human", "Beast"), ("No Change"), 5), 
    (("Bird", "Bird"), ("No Change"), 3), 
    (("Bird", ("Fish", "Turtle")), ("Bird", "Empty"), 50), 
    (("Penguin", "Fish"), ("Penguin", "Empty"), 75), 
    (("Turtle", "Fish"), ("Turtle", "Empty"), 50), 
    (("Beast", ("Fish", "Turtle")), ("Beast", "Empty"), 75), 
    (("Fish", ("Water", "Fish")), ("No Change"), 5),
    (("Beast", "Beast"), ("No Change"), 3), 
    (("Penguin", "Penguin"), ("No Change"), 3), 
    (("Turtle", "Turtle"), ("No Change"), 3), 
    (("Phoenix", ("Ash", "Fire", "Lava", "Volcano")), ("No Change"), 10), 
    (("Dragon", ("Phoenix", "Gold")), ("No Change"), 10),     
    ((("Dragon", "Phoenix"), "Royalty"), ("No Change", "Empty"), 200),
    
    (("Tumbleweed", ("Earth", "Sand", "Stone", "Clay", "Plants", "Seeds", "Dust")), 
            ("Tumbleweed", "Tumbleweed"), 10),  

    ((("Human", "Beast", "Bird", "Phoenix", "Dragon", "Android", "Angler", "Miner", "Pirate", 
        "Vocaloid", "Hero", "Will o' Wisp", "Penguin", "Turtle", "Angel", "Royalty", 
        "Mangrove", "Snowman"), "Love"), ("No Change"), 8), 

    ((("Human", "Beast", "Phoenix", "Dragon", "Android" "Angler", "Miner",  "Hero", "Penguin", "Turtle"),
         "Music"), ("No Change"), 7),
    ((("Bird", "Pirate", "Vocaloid", "Angel", "Royalty"), "Music"), ("No Change"), 10), 

    ((("Human", "Beast", "Phoenix", "Dragon", "Android", "Angler", "Miner", 
    "Hero", "Penguin", "Turtle"), "Vocaloid"), ("No Change"), 5),
    ((("Pirate", "Bird", "Vocaloid", "Angel", "Royalty"), "Vocaloid"), ("No Change"), 10), 

    ((("Beast", "Bird", "Angler", "Miner", "Pirate", "Penguin", "Turtle"), "Light"), ("No Change"), 2),
    ((("Hero", "Will o' Wisp", "Angel", "Royalty"), "Light"), ("No Change"), 7), 

    ((("Human", "Angler", "Miner", "Pirate", "Hero", "Royalty"), "Will o' Wisp"), ("Empty", "Empty"), 100), 
    (("Angel", "Will o' Wisp"), ("Angel", "Empty"), 100),  

    ((("Human", "Angler", "Miner", "Hero"), "Royalty"), ("No Change"), 7), 

    ((("Android", "Robot", "AI", "Vocaloid"), ("Ocean", "Wave", "Tsunami")), ("Metal", "Water"), 150), 
    ((("Android", "Robot", "AI", "Vocaloid"), "Water"), ("Metal", "Empty"), 50), 

    ((("Human", "Android", "Angler", "Miner", "Pirate", "Hero", "Royalty", "Penguin"), "Snowman"), ("No Change"), 5),

    ((("House", "Boat"), ("Earthquake", "Tornado", "Blizzard", "Hurricane", "Duststorm", "Sandstorm", "Earthquake", 
        "Landslide", "Avalanche")), ("Empty", "Empty"), 100), 
    
    (("Pirate", ("Boat", "Ocean", "Beach", "Pirate")), ("No Change"), 7),
    (("Miner", ("Bird", "Human", "Angler", "Miner")), ("No Change"), 7), 
    (("Angler", ("Human", "Ocean", "Beach", "Boat", "Angler", "Turtle", "Lake")), ("No Change"), 7), 
    (("Hero", ("Human", "Angler", "Miner")), ("No Change"), 7), 
    (("Royalty", "Royalty"), ("Royalty", "Empty"), 300),
    (("Royalty", "Pirate"), ("Empty", "Empty"), 400),
    (("Angel", ("Bird", "Angel")), ("No Change"), 5),
    (("Angel", "Hero"), ("No Change"), 15),
    (("Angel", ("Phoenix", "Dragon")), ("Empty", "Empty"), 1000), 


    # phenomena / other disasters
    (("Air", "Air"), ("Wind", "Empty"), 3),                       # swirly lads
    (("Wind", "Wind"), ("Tornado", "Empty"), 3), 
    (("Tornado", "Dust"), ("Duststorm", "Empty"), 3), 
    (("Duststorm", "Dust"), ("No Change"), 5), 
    (("Tornado", ("Ice", "Snow", "Cold")), ("Blizzard", "Empty"), 3),
    (("Blizzard", "Snow"), ("No Change"), 5), 
    (("Tornado", "Sand"), ("Sandstorm", "Empty"), 3), 
    (("Sandstorm", "Sand"), ("No Change"), 5), 
    (("Tornado", ("Water", "Steam")), ("Hurricane", "Empty"), 3), 
    (("Ocean", ("Steam", "Fire", "Wind", "Rain", "Tornado")), ("Hurricane", "Empty"), 3), 
    (("Ocean", "Sun"), ("Hurricane", "Sun"), 3), 
    (("Hurricane", ("Ocean", "Steam")), ("No Change"), 8), 
    (("Hurricane", ("Cold", "Ice")), ("Water", "Empty"), 70), 

    ((("Tornado", "Hurricane", "Sandstorm", "Duststorm", "Blizzard"), "Wind"), ("Empty", "Empty"), 50), 
    ((("Tornado", "Hurricane", "Sandstorm", "Duststorm", "Blizzard"), 
            ("Tornado", "Hurricane", "Sandstorm", "Duststorm", "Blizzard")), ("Empty", "Empty"), 100), 
    
    # rocky lads
    ((("Earth", "Earthquake", "Stone", "Clay"), ("Earth", "Earthquake", "Stone", "Clay")), ("Mountain", "Empty"), 3),
    (("Clay", "Clay"), ("Mountain", "Empty"), 3), 
    (("Mountain", "Mountain"), ("No Change"), 3), 
    (("Mountain", ("Stone", "Dust")), ("Mountain", "Empty"), 5),
    (("Mountain", "Lava"), ("Volcano", "Empty"), 3), 
    (("Volcano", "Lava"), ("No Change"), 5), 
    (("Mountain", "Volcano"), ("No Change"), 5), 
    (("Volcano", "Volcano"), ("No Change"), 3), 
    (("Volcano", "Water"), ("Volcano", "Steam"), 3), 
    (("Earth", "Energy"), ("Earthquake", "Empty"), 3), 
    (("Mountain", ("Tornado", "Energy", "Earthquake", "Tsunami")), ("Landslide", "Empty"), 3), 
    (("Landslide", ("Stone", "Earth")), ("Earth", "Earth"), 50), 
    (("Mountain", "Landslide"), ("No Change"), 5), 
    (("Landslide", "Landslide"), ("Mountain", "Mountain"), 50),
    (("Landslide", "Mountain"), ("Earth", "Earth"), 50), 

    (("Ocean", "Earthquake"), ("Tsunami", "Empty"), 3),           # tsunami, also an ocean thing
    (("Wave", ("Wave", "Energy", "Wind")), ("Tsunami", "Empty"), 3), 

    # ocean things
    (("Water", "Water"), ("Lake", "Empty"), 3),                  # ocean/wave/sand
    (("Lake", ("Water", "Lake")), ("Ocean", "Empty"), 3),
    (("Ocean", ("Wind", "Energy")), ("Wave", "Empty"), 3), 
    (("Ocean", "Ocean"), ("No Change"), 5), 
    (("Ocean", "Lake"), ("Ocean", "Ocean"), 3), 
    (("Stone", ("Wave", "Cold", "Wind")), ("Sand", "Empty"), 15), 
    (("Stone", "Plants"), ("Sand", "Plants"), 10), 
    ((("Ocean", "Sun"), "Stone"), ("No Change", "Sand"), 10), 
    ((("Ocean", "Lake"), "Fire"), ("No Change", "Steam"), 10), 
    ((("Ocean", "Lake"), "Sun"), ("Cloud", "Sun"), 3), 
    (("Lake", "Lava"), ("Water", "Stone"), 3), 
    (("Ocean", ("Volcano", "Lava", "Mountain")), ("Island", "Empty"), 3), 
    (("Ocean", ("Wood", "Metal")), ("Ocean", "Boat"), 3),
    (("Ocean", "Sand"), ("Beach", "Empty"), 3),
    
    (("Beach", ("Tsunami", "Hurricane")), ("Sand", "Ocean"), 100),
    (("Tsunami", ("Tsunami", "Hurricane")), ("Ocean", "Ocean"), 50), 

    (("Beach", ("Sand", "Wave")), ("No Change", "Empty"), 75), 
    (("Island", "Sand"), ("Island", "Empty"), 75), 
    ((("Tsunami", "Hurricane"), "Boat"), ("Ocean", "Empty"), 200), 

    (("Ocean", ("Wave", "Beach", "Fish", "Boat", "Tsunami")), ("No Change"), 10),
    (("Island", ("Ocean", "Plants", "Fish", "Tree", "Forest", "Mangrove", "Swamp")), ("No Change"), 10), 
    (("Lake", ("Fish", "Boat")), ("No Change"), 5),
    (("Island", "Island"), ("No Change"), 5), 
    (("Boat", "Boat"), ("No Change"), 5), 
    (("Turtle", ("Beach", "Ocean", "Island")), ("No Change"), 5),

    # desert things
    (("Sand", "Sand"), ("Desert", "Empty"), 3), 
    (("Desert", "Earth"), ("No Change", "Sand"), 3), 
    (("Desert", ("Water", "Rain", "Lake")), ("Oasis", "Empty"), 3), 
    (("Desert", "Tornado"), ("No Change", "Sandstorm"), 3), 
    
    (("Desert", "Lava"), ("Stone", "Stone"), 75),
    (("Desert", "Volcano"), ("Stone", "Mountain"), 75),  

    (("Oasis", "Fire"), ("Desert", "Steam"), 75), 
    (("Oasis", "Lava"), ("Desert", "Stone"), 75), 
    (("Oasis", "Volcano"), ("Desert", "Mountain"), 75), 
    (("Oasis", ("Phoenix", "Sun")), ("Desert", "No Change"), 75), 

    (("Desert", "Wind"), ("Sand", "Sand"), 75), 
    (("Oasis", ("Sandstorm", "Tornado", "Blizzard", "Duststorm", "Sandstorm")), ("Sand", "Sand"), 75), 
    ((("Desert", "Oasis"), "Tsunami"), ("Sand", "Water"), 75), 
     
    (("Desert", ("Cactus", "Sand", "Oasis", "Sandstorm", "Sun", "Lava", "Volcano")), ("No Change"), 10),
    (("Desert", "Desert"), ("No Change"), 5),
    (("Oasis", ("Cactus", "Sand", "Oasis", "Wave", "Rain", "Water")), ("No Change"), 5),

    # glassware/ceramic
    (("Clay", "Fire"), ("Ceramic", "Empty"), 3),
    (("Sand", "Fire"), ("Glassware", "Empty"), 3), 
    (("Clay", ("Sun", "Phoenix")), ("Ceramic", "No Change"), 3), 
    (("Sand", ("Sun", "Phoenix")), ("Glassware", "No Change"), 3), 

    ((("Tornado", "Hurricane", "Sandstorm", "Duststorm", "Blizzard", "Earthquake", "Landslide", "Pirate", "Hero",
        "Wind", "Stone"), ("Ceramic", "Glassware")), ("No Change", "Empty"), 50),
 
    (("Glassware", ("Ceramic", "Alcohol", "Water", "Cola")), ("No Change"), 5), 
    (("Ceramic", "Ceramic"), ("No Change"), 3), 
    (("Glassware", "Glassware"), ("No Change"), 2), 

]

def x_in_y(element, group):         # The regular "in" function can't diffrentiate properly between
    if type(group) is str:          # things like "Earth" and "Earthquake", hence I had to make my own.
        if element == group:
            return True
    elif type(group) is tuple:
        for thing in group:
            if element == thing:
                return True
    return False

# elements = (reactant1, reactant 2)
# synergy = ((reactant1, reactant2), (product1, product2), gold_from_reaction)
def check_for_synergy(elements):            # takes in tuple of reactant elements to check
    for synergy in synergy_list:
        if x_in_y(elements[0], synergy[0][0]) and x_in_y(elements[1], synergy[0][1]): # if present

            if synergy[1] == "No Change":   # if the reaction is an adjacency bonus
                return (True, (elements, elements, synergy[2]))   

            else:                           # if the reaction is a transformation reaction

                # checking to see if either aren't meant to be changed
                if synergy[1][0] == "No Change":
                    return (True, (elements, (elements[0], synergy[1][1]), synergy[2]))  
                if synergy[1][1] == "No Change":
                    return (True, (elements, (synergy[1][0], elements[1]), synergy[2]))    
                
                # otherwise does the normal transformation reaction
                return (True, (elements, synergy[1], synergy[2])) 

    return (False, None)        # returns that no synergy is present if none was found.

# TODO / future plans:

# remove doubling of reactions of same element

# showing the "press TAB to show shortcuts" but with TAB in key-looking font

# potentially add food combinations
#   humans eat food
#   food buffs other food
#   beast + human --> cow + farmer
#   cow + water/milk/plants --> cow + milk
#   farmer + cow/bird/penguin/beast/turtle --> farmer + meat
#   hero + phoenix/dragon --> hero + meat (instead of empty)
#   milk + ice/snow --> ice cream
#   milk + fire --> cheese
#   egg + cheese --> omelette
#   human + seeds --> wheat             (not food, used to make some though)
#   wheat + wheat/fire --> bread
#   bread + meat --> sandwich
#   bread + cheese --> pizza
#   water + wheat/meat/egg --> soup
#   ocean + fire --> salt
#   ocean + sun (see: later) --> salt + sun
#   salt is eaten by foods.
# likely won't do food. it'd fill up the shop a lot.
# would likely only have some general food instead of multiple, or none at all.

# magnetic field
# would need more reactions to be added
#   electricity + metal --> magnetic field
#   magnetic field + metal --> electricity
#
#   magnetic field + rock --> metal
#
#   magnetic field + robot/ai/android/vocaloid --> electricity + metal
#
#   electricity + electricity --> no change (7g)
#   magnetic field + magnetic field --> no change (7g)
#   magnetic field + electricity --> no change (18g)
# 
#   sun + magnetic field --> sun + aurora borealis

# sulfur
# would need more reactions to be added
#   miner + volcano --> miner + sulfur
#   sulfur + coal --> explosive powder
#       explosive powder + fire --> energy + energy (x00g)
#   lake + fire/lava/sulfur --> hotspring
#   lake + phoenix/volcano --> hotspring + no change
#   sulfur + cloud/rain --> acid rain
#       could harm living, not sure.

# mythological creatures
#   bird + electricity --> thunderbird
#   electricity + life --> raiju
#   thunderbird/raiju + electricity --> no change
#       might not do thunderbird, already a mythical bird.
#   ___ + ___ --> kumiho
#   kumiho + human --> kumiho
#       slain by hero
#   human + fire --> demon
#       demon + fire/lava --> no change
#       slays all living things
#       sets everything nearby ablaze
#           this part is kind of a pain to add
#       slain by hero
#       demon + angel --> empty + empty
#       demon + boat --> charon
#       should look like s-tier husbando material to compensate for miku being waifu material

#   tree + life --> world tree
#       world tree + human --> elf + world tree
#       elf + plants/tree/forest/swamp/mangrove/world tree/beast/bird/penguin/turtle/fish --> no change

# dust expansion
#   coal dust
#       burns
#   sawdust
#       burns
#   metal dust
#   volcanic dust
#   magic dust
# all can form dust storm

# other ideas:
#   something that spreads to empty tiles
#   group of things that all eat a fraction of everything, all of them sum to eat everything

#####

# Types of elements.
#   This list is used so I can see what I have already made and what I could make.

# Main expected strategies:     [Normally what carries a run.]
#   Living
#       Robotics (partially living)
#   Burning
#   Oceanic
#   Snowing
#   Desert
#   Environmentalist

# Side strategies:              [Useful to assist a run though could carry it, too.]
#   Mountainous 
#   Gold
#   Clouds

# Additional tools:             [Things that come and go.]
#   Ceramic/glassware
#   Black Hole
#   Dust + Duststorm
