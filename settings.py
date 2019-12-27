from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = "mio "
TOKEN = os.getenv("TOKEN")
SQL_DATABASE = os.getenv("SQL_DATABASE")
PRIVATE_SERVER_ID = 656309437648338975
GENERAL_CHANNEL_ID = 656309437648338978

DEFAULT_ROLES = [
    659570001090576391, # DJ
    657786333959290880, # cool people
    657788661626306570, # default color
]