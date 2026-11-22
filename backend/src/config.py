from decouple import UndefinedValueError, config
from dotenv import load_dotenv


def PORT():
    try:
        return int(config("PORT"))
    except UndefinedValueError:
        return 4000


load_dotenv()
CONFIG = {"PORT": PORT()}
