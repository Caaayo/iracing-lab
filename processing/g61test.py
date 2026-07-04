from garage61api.client import Garage61Client
from dotenv import load_dotenv
load_dotenv()

# My G61 Token
GARAGE61_TOKEN = int(os.getenv('GARAGE61_TOKEN'))
g61 = Garage61Client(GARAGE61_TOKEN)
print(g61.me())



