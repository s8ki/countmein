import random
import time
import json
from datetime import datetime
import requests


ADD_RECORD_URL = 'http://localhost:80/api/record/1/1' 
TIMEOUT = 1

INSIDE = 25
MIN_INSIDE = 3
MAX_INSIDE = 60


def send_random_data():
    global INSIDE
    if INSIDE <= MIN_INSIDE:
        rand = random.randrange(1, 4)
    elif MAX_INSIDE <= INSIDE:
        rand = random.randrange(-4, -1)
    else:
        rand = random.randrange(-3, 3)
    INSIDE += rand
    d = {'timestamp': datetime.now().isoformat(), 'change':rand, 'inside':INSIDE}
    print(requests.post(ADD_RECORD_URL, data=json.dumps(d), headers={'content-type': 'application/json'}))


if __name__ == "__main__":
    now = time.time()

    while True:
        if time.time() - now > TIMEOUT:
            send_random_data()
        else:
            time.sleep(TIMEOUT)
