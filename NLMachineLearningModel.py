import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
import joblib

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

spell = SpellChecker()

# Text pre processing for misspelling, stopwords, and out of bound characters
def preprocess_text(text):
    text = ''.join([char for char in text if char.isalnum() or char.isspace()])
    
    text = text.lower()
    
    tokens = word_tokenize(text)
    
    corrected_tokens = [spell.correction(token) for token in tokens]
    
    filtered_tokens = [word for word in corrected_tokens if word and word not in stopwords.words('english')]
    
    return ' '.join(filtered_tokens)

# Data for training the model -> Update this every year for new data detection
data = [
    ("[UPD] ❄️ Fisch", "Fishing"),
    ("[WINTER❄️] Adopt Me!", "Roleplay"),
    ("Carry an Egg [2 Player Obby]", "Obby"),
    ("[UPD] Blue Lock: Rivals", "Soccer"),
    ("[UPD]🐟GO FISHING", "Fishing"),
    ("Insomnia", "Horror"),
    ("Pet Simulator 99! 🎁", "Pet Simulation"),
    ("Musical Chairs 🎵🪑", "Party Game"),
    ("Short Horror Games", "Horror"),
    ("NewSmith🏠RP Update 19🎄!", "Roleplay"),
    ("🎁 XMAS & SHELBY! Car Dealership Tycoon", "Car Simulation"),
    ("Team Soccer (3 vs. 3)", "Soccer"),
    ("Impossible Squid Game! Glass Bridge 2", "Obstacle Challenge"),
    ("[SUPER SHADOW 1] Sonic Speed Simulator", "Sonic Adventure"),
    ("[SONIC 3] Obby But You Can't Jump", "Obby"),
    ("[XMAS] Find The Button! 🔴", "Puzzle"),
    ("⚽ Car Suspension Test", "Car Simulation"),
    ("Sprunki Simulator 🎤", "Music"),
    ("Drive it! [2 Player Obby]", "Driving"),
    ("[APT DANCE | +9] ❄️ TTD 3", "Dancing"),
    ("[🎁 FREE SOTANO 6!] Vigevani Faith House 2", "Horror"),
    ("Be A Food [NEW]", "Comedy Simulation"),
    ("Speedhaven 🏡RNG RP - FREE VIP", "Roleplay"),
    ("Throw Me [2 Player Obby]", "Obby"),
    ("Generic Cooking Game [BETA][UPD2.16]", "Cooking"),
    ("[WINTER❄️] Bike Obby", "Obby"),
    ("[2X COINS] Gym Star Simulator", "Fitness Simulation"),
    ("Ultimate Horse Race [ Xmas🎅]", "Horse Racing"),
    ("Build to Survive Block City! 🎄", "Survival"),
    ("Eat Pizza to Grow GIGACHAD [BIG UPD]", "Humor"),
    ("Doge Story", "Adventure"),
    ("Age of Titans", "Fantasy Adventure"),
    ("Pass or Die 💣", "Trivia"),
    ("PLAY OR DIE", "Trivia"),
    ("oMega Obby 🌟 725 Stages! [UPD]", "Obby"),
    ("Answer or Die", "Trivia"),
    ("Draw Tower Race", "Drawing"),
    ("🗝️Lootify[🎄UPD]", "Loot Game"),
    ("Pacific Gymnastics 🤸 RP", "Roleplay"),
    ("[UPD] Create a Cart Ride! 🎅", "Riding"),
    ("Find the Buttons! 🔎🔴", "Puzzle"),
    ("SPLASH ⭐ Skate & Music", "Skating"),
    ("Hug People Simulator", "Simulation"),
    ("Club Roblox RP 🏡", "Roleplay"),
    ("Basically FNF: Remix", "Music"),
    ("Yogurt Stage Tower", "Obby"),
    ("(NEW) Sunshine Islands Bus Simulator", "Driving"),
    ("[🔥NEW CARS!]🚗Midnight Chasers: Highway Racing", "Racing"),
    ("Block Puzzle", "Puzzle"),
    ("Field Trip Z", "Adventure"),
    ("Sell Water to RULE THE WORLD 💧🌎", "Strategy"),
    ("Sleigh Ride to the North Pole!", "Adventure"),
    ("[🎄Event!][🚽Free Titan!]⚔Sword Warriors!", "Action"),
    ("Cook Burgers", "Cooking"),
    ("Forgotten Worlds", "Fantasy Adventure"),
    ("Road Rage Simulator", "Driving"),
    ("YouTube Race Simulator", "Racing"),
    ("Salon Makeover 💅", "Makeover"),
    ("Crack It!💆", "Puzzle"),
    ("[NEW CARS] Drive X 🏎️ CARS", "Racing"),
    ("[NEW] Skyblock Tycoon🗡️", "Tycoon"),
    ("Makeup Contest 💄", "Makeover"),
    ("Carousel - World School 🏫", "Roleplay"),
    ("Plane Race", "Racing"),
    ("❄️⛄ Wild Horse Islands", "Horse Simulation"),
    ("[💥UPD] Deep Descent", "Adventure"),
    ("[🎄XMAS] Anime Slashing Simulator", "Anime Action"),
    ("Drive Cars Down A Hill!", "Driving"),
    ("🏈create your own NFL team and prove them wrong!", "Sports"),
    ("[ PHASE 4 ] Sprunki Tower Defense", "Tower Defense"),
    ("🍔 Burgeria Tycoon", "Tycoon"),
    ("Warrior Cats: Ultimate Edition", "Animal Roleplay"),
]

# split of data into game names and topics
game_names, topics = zip(*data)

# Preprocess game names
preprocessed_game_names = [preprocess_text(name) for name in game_names]

# Encode topics
label_encoder = LabelEncoder()
encoded_topics = label_encoder.fit_transform(topics)

'''
# Text data -> numerical features
vectorizer = TfidfVectorizer(stop_words=nltk.corpus.stopwords.words('english'))
X = vectorizer.fit_transform(preprocessed_game_names)
'''

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(preprocessed_game_names, encoded_topics, test_size=0.2, random_state=42)

# Pipeline
model = make_pipeline(TfidfVectorizer(), LogisticRegression())

# Model training
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'game_topic_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Model trained and saved!")