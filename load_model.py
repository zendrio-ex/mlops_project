import os
from src.config import settings

command = f"mkdir model && cd model && gdown --folder '{settings['google_drive']}'"
os.system(command)