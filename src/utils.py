#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle as pkl
import re
import time
import unicodedata
from pathlib import Path
from typing import Dict, List

import requests
from requests import (ConnectionError, RequestException, Response, Session,
                      Timeout)

ALLOWED_SUFFIXES = {'.json', '.pkl'}
SUCCESS_SLEEP = 0.5
RETRY_SLEEP = 1.0


def dump(obj: object, name: str, dump_dir: Path = Path(__file__).resolve().parent / 'dump') -> None:
    file = dump_dir / name

    # check if file suffix in ALLOWED_SUFFIXES
    if file.suffix not in ALLOWED_SUFFIXES:
        raise ValueError(f'Suffix not allowed: {file.suffix}')

    # create dump_dir (if not exists)
    dump_dir.mkdir(parents=True, exist_ok=True)

    if file.suffix.lower() == '.pkl':
        pkl.dump(obj, open(file, 'wb'))
    elif file.suffix.lower() == '.json':
        json.dump(obj, open(file, 'w'))


def get(url: str, session: Session = None, headers: Dict[str, str] = None, cookies: Dict[str, str] = None, timeout: Dict = None) -> Response:
    try:
        # make the request and get the response
        if session is None:
            r = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
        else:
            r = session.get(url, headers=headers, cookies=cookies, timeout=timeout)

        # sleep
        if r.status_code != 200:
            time.sleep(RETRY_SLEEP)
        else:
            time.sleep(SUCCESS_SLEEP)

        # return the response
        return r
    except (ConnectionError, Timeout, RequestException):
        # sleep
        time.sleep(RETRY_SLEEP)


def get_headers(file: Path) -> List[Dict[str, str]]:
    user_agents = read(file).splitlines()
    return [{'User-Agent': user_agent.strip()} for user_agent in user_agents]


def get_book_id(url: str) -> str:
    return url.split('/download/')[1].split('/')[0]


def load(file: Path) -> object:
    # check if file exists
    if not file.exists():
        raise ValueError(f'File does not exist: {file}')

    # check if file suffix in ALLOWED_SUFFIXES
    if file.suffix not in ALLOWED_SUFFIXES:
        raise ValueError(f'Suffix not allowed: {file.suffix}')

    if file.suffix.lower() == '.pkl':
        return pkl.load(open(file, 'rb'))
    elif file.suffix.lower() == '.json':
        return json.load(open(file, 'r'))


def mkdirs(*args: Path) -> None:
    for dir in args:
        dir.mkdir(parents=True, exist_ok=True)


def read(file: Path) -> str:
    # check if file exists
    if not file.exists():
        print(f'File does not exist: {file}')

    with open(file, 'r') as f:
        return f.read()


def sanitize_file(file: str) -> str:
    file = str(file)
    file = unicodedata.normalize('NFKD', file).encode('ascii', 'ignore').decode('ascii')
    file = re.sub(r'[^\w\s-]', '', file).strip().lower()
    return re.sub(r'[-\s]+', '-', file)


def write(text: str, file: Path) -> None:
    # check if file exists
    if file.exists():
        print(f'File already exists: {file}')

    with open(file, 'w') as f:
        f.write(text)
