import logging
import os
import re
import sys
import time
import requests


LOG_FILE = 'application.log'
URL = os.environ['BOT_URL']
EVENTS = [
    {
        'name': 'Successful Login',
        'regex': re.compile(
            r'(?P<date>\w+ \d{1,2}, \d{4} \d{2}:\d{2}): Successful Login: username=(?P<user>\w+) ip=(?P<ip>[\w.:]+) '
            r'method=(?P<type>[\w-]+)'
        ),
        'message': 'Hi {user}, I logged a successful {type}-login on your gitlab account from ip={ip} at {date}',
        'channel': '@{user}'
    },
    {
        'name': 'Failed Login',
        'regex': re.compile(
            r'(?P<date>\w+ \d{1,2}, \d{4} \d{2}:\d{2}): Failed Login: (user)(name)?=(?P<user>\w+) ip=(?P<ip>[\w.:]+)'
        ),
        'message': 'Hi {user}, I logged a failed login on your gitlab account from ip={ip} at {date} :grimacing:',
        'channel': '@{user}'
    }
]


def monitor_file(file, update_sleep_time=1, max_time=3600):
    """ Generator yielding added lines to a file (locking). Terminate after max_time seconds.

    Args:
        file: stream
        update_sleep_time: Update each update_sleep_time for new lines.
        max_time: Terminate after max_time seconds.
    """
    file.seek(0, 2)
    start = time.time()
    while True:
        line = file.readline()
        if not line:
            if time.time() - start > max_time:
                return
            time.sleep(update_sleep_time)
            continue
        yield line


def process_log_line(line):
    """ Parse the events against a log file line. Sent a notification to the affected user.

    Args:
        line (str): A line from the gitlab application log.
    """
    for event in EVENTS:
        payload = dict()
        match = event['regex'].search(line)
        if match:
            match_dict = match.groupdict()
            payload['channel'] = event['channel'].format(**match_dict).lower()
            payload['text'] = event['message'].format(**match_dict)
            logging.info('Sent match: {}'.format(payload))
            requests.post(URL, json=payload)


def setup():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    """ Run a single bot loop.

        A Loop:
            1. Open the LOG_FILE stream.
            2. Fetch newly added lines to the LOG_FILE for max_time seconds (monitor_file).
            2.1. process_log_line for each newly added line.
    """
    with open(LOG_FILE, mode='r', encoding='utf-8') as file:
        for line in monitor_file(file):
            process_log_line(line)


if __name__ == '__main__':
    setup()
    while True:
        logging.info('Start the bot.')
        main()

