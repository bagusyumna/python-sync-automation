from dotenv import load_dotenv
from os import getenv


def get_var_env(key, value):
    load_dotenv()
    data = getenv(key)
    return data if data else value
