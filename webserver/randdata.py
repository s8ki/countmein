import random
import time
import json
from datetime import datetime
import requests


ADD_RECORD_URL = 'http://localhost/api/record/1/1' 
TIMEOUT = 1

INSIDE = 48
MIN_INSIDE = 3
MAX_INSIDE = 50


def send_random_data():
    global INSIDE
    if INSIDE <= MIN_INSIDE:
        rand = random.randrange(1, 4)
    elif MAX_INSIDE <= INSIDE:
        rand = random.randrange(-1, 1)
    else:
        rand = random.randrange(-1, 1)
    INSIDE += 1
    d = {'timestamp': datetime.now().isoformat(), 'change':rand, 'inside':INSIDE, 'mask': random.choice([1,0,0,0,0,0,0,0,0,0,0,0,0])}
    print(d)
    print(requests.post(ADD_RECORD_URL, data=json.dumps(d), headers={'content-type': 'application/json'}))


if __name__ == "__main__":
    now = time.time()

    while True:
        if time.time() - now > TIMEOUT:
            send_random_data()
        else:
            time.sleep(TIMEOUT)
