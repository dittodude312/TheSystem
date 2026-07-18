from dotenv import load_dotenv
from os import getenv
from system_functions import utilfunctions

_ = [1]
requests = [x for x in _]
requests = list(enumerate(requests[1:]))
print(requests)

#print([x for x in range(10) if x%2==0])