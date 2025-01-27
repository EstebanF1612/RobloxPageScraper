import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
import joblib

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

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
    ("[UPD] ❄️ Fisch", "Simulation"),
    ("[WINTER❄️] Adopt Me!", "Roleplay"),
    ("Carry an Egg [2 Player Obby]", "Obby"),
    ("[UPD] Blue Lock: Rivals", "Sports"),
    ("[UPD]🐟GO FISHING", "Simulation"),
    ("Insomnia", "Survival"),
    ("Pet Simulator 99! 🎁", "Simulation"),
    ("Musical Chairs 🎵🪑", "Casual"),
    ("Short Horror Games", "Survival"),
    ("NewSmith🏠RP Update 19🎄!", "Roleplay"),
    ("🎁 XMAS & SHELBY! Car Dealership Tycoon", "Simulation"),
    ("Team Soccer (3 vs. 3)", "Sports"),
    ("Impossible Squid Game! Glass Bridge 2", "Survival"),
    ("[SUPER SHADOW 1] Sonic Speed Simulator", "Racing"),
    ("[SONIC 3] Obby But You Can't Jump", "Obby"),
    ("[XMAS] Find The Button! 🔴", "Puzzle"),
    ("⚽ Car Suspension Test", "Simulation"),
    ("Sprunki Simulator 🎤", "Entertainment"),
    ("Drive it! [2 Player Obby]", "Racing"),
    ("[APT DANCE | +9] ❄️ TTD 3", "Entertainment"),
    ("[🎁 FREE SOTANO 6!] Vigevani Faith House 2", "Survival"),
    ("Be A Food [NEW]", "Simulation"),
    ("Speedhaven 🏡RNG RP - FREE VIP", "Roleplay"),
    ("Throw Me [2 Player Obby]", "Obby"),
    ("Generic Cooking Game [BETA][UPD2.16]", "Simulation"),
    ("[WINTER❄️] Bike Obby", "Obby"),
    ("[2X COINS] Gym Star Simulator", "Simulation"),
    ("Ultimate Horse Race [ Xmas🎅]", "Sports"),
    ("Build to Survive Block City! 🎄", "Survival"),
    ("Eat Pizza to Grow GIGACHAD [BIG UPD]", "Casual"),
    ("Doge Story", "Adventure"),
    ("Age of Titans", "RPG"),
    ("Pass or Die 💣", "Puzzle"),
    ("PLAY OR DIE", "Puzzle"),
    ("oMega Obby 🌟 725 Stages! [UPD]", "Obby"),
    ("Answer or Die", "Puzzle"),
    ("Draw Tower Race", "Puzzle"),
    ("🗝️Lootify[🎄UPD]", "Simulation"),
    ("Pacific Gymnastics 🤸 RP", "Roleplay"),
    ("[UPD] Create a Cart Ride! 🎅", "Simulation"),
    ("Find the Buttons! 🔎🔴", "Puzzle"),
    ("SPLASH ⭐ Skate & Music", "Entertainment"),
    ("Hug People Simulator", "Simulation"),
    ("Club Roblox RP 🏡", "Roleplay"),
    ("Basically FNF: Remix", "Entertainment"),
    ("Yogurt Stage Tower", "Obby"),
    ("(NEW) Sunshine Islands Bus Simulator", "Simulation"),
    ("[🔥NEW CARS!]🚗Midnight Chasers: Highway Racing", "Racing"),
    ("Block Puzzle", "Puzzle"),
    ("Field Trip Z", "Adventure"),
    ("Sell Water to RULE THE WORLD 💧🌎", "Strategy"),
    ("Sleigh Ride to the North Pole!", "Adventure"),
    ("[🎄Event!][🚽Free Titan!]⚔Sword Warriors!", "Action"),
    ("Cook Burgers", "Simulation"),
    ("Forgotten Worlds", "Adventure"),
    ("Road Rage Simulator", "Racing"),
    ("YouTube Race Simulator", "Racing"),
    ("Salon Makeover 💅", "Casual"),
    ("Crack It!💆", "Puzzle"),
    ("[NEW CARS] Drive X 🏎️ CARS", "Racing"),
    ("[NEW] Skyblock Tycoon🗡️", "Simulation"),
    ("Makeup Contest 💄", "Casual"),
    ("Carousel - World School 🏫", "Education"),
    ("Plane Race", "Racing"),
    ("❄️⛄ Wild Horse Islands", "Simulation"),
    ("[💥UPD] Deep Descent", "Adventure"),
    ("[🎄XMAS] Anime Slashing Simulator", "Action"),
    ("Drive Cars Down A Hill!", "Racing"),
    ("🏈create your own NFL team and prove them wrong!", "Sports"),
    ("[ PHASE 4 ] Sprunki Tower Defense", "Strategy"),
    ("🍔 Burgeria Tycoon", "Simulation"),
    ("Warrior Cats: Ultimate Edition", "Roleplay"),
    ("Metro Life ❄️ City RP","Roleplay"),
    ("[BENTLEY] Driving Empire 🏎️ Car Racing", "Racing"),
    ("Every Jump +1 Jump Power 🚀 ","Adventure"),
    ("Backrooms Drift [NEW LEVEL 🚗]", "Racing"),
    ("⚡Race Clicker", "Racing"),
    ("Carry A Friend! (Teamwork Obby)", "Obby"),
    ("Racing Simulator 🏎️", "Racing"),
    ("Merge for SPEED!", "Racing"),
]


# split of data into game names and topics
game_names, topics = zip(*data)

# Preprocess game names
preprocessed_game_names = [preprocess_text(name) for name in game_names]

# Encode topics
label_encoder = LabelEncoder()
encoded_topics = label_encoder.fit_transform(topics)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(preprocessed_game_names, encoded_topics, test_size=0.2, random_state=42)

# Pipeline
model = make_pipeline(TfidfVectorizer(), LogisticRegression())

# Model training
model.fit(X_train, y_train.ravel())

# Evaluate the model using cross-validation (Stratified)
stratified_kfold = StratifiedKFold(n_splits=5)
scores = cross_val_score(model, X_train, y_train.ravel(), cv=stratified_kfold)
print(f"Cross-validation scores: {scores}")
print(f"Mean cross-validation score: {scores.mean()}")

# Save model
joblib.dump(model, 'game_topic_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
joblib.dump(TfidfVectorizer(), 'vectorizer.pkl')

print("Model and label encoder have been saved.")