from decouple import config
from dotenv import load_dotenv

load_dotenv();
CONFIG = {
  "PORT": config("PORT")
}
