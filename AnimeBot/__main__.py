import glob
from pathlib import Path
from AnimeBot import AnimeBot
from utils import load_plugins
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

path = "AnimeBot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
    
print("Search Anime Bot is Up!! !")
print("Enjoy")

if __name__ == "__main__":
    AnimeBot.run_until_disconnected()