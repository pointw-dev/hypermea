#! /usr/bin/env python3

import requests
import json
from datetime import datetime, UTC, timezone
from time import sleep, perf_counter

NUM_REQUESTS = 130
DELAY_SECONDS = 0.5
HEADERS = {
    'Authorization': 'Basic cm9vdDpwYXNzd29yZA=='
}


def main():
    print(f'Making {NUM_REQUESTS} requests with {int(DELAY_SECONDS * 1000)} millisecond delay after each\n')

    start_time = perf_counter()

    last_reset_time = None

    for i in range(NUM_REQUESTS):
        request_number = i + 1
    
        url = 'http://localhost:2112/'
        elapsed = f'{perf_counter() - start_time:.2f}'
        print(f'#{request_number:<4} (after {elapsed:>8}s)  {url}',  end=" ")
    
        result = requests.get(url, headers=HEADERS)
        print(f'- {result.status_code} {result.reason} ', end=" ")

        headers = dict(result.headers)
        if 'X-RateLimit-Remaining' in headers:
            remaining = headers['X-RateLimit-Remaining']
            limit = headers['X-RateLimit-Limit']
            last_reset_time = datetime.fromtimestamp(int(headers['X-RateLimit-Reset']), UTC)
            print(f'- {remaining}/{limit}')
        else:
            print('- rate limiting not enabled' if not result.status_code == 429 else '' )

        if result.status_code == 429:
            print(json.dumps(dict(result.headers), indent=2))
            print()
            if last_reset_time:
                print(f'- waiting until {last_reset_time}')
                while last_reset_time > datetime.now(timezone.utc):
                    pass
            else:
                quit(1)
            sleep(DELAY_SECONDS)

    
        sleep(DELAY_SECONDS)


if __name__ == '__main__':
    main()
