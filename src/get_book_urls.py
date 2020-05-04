#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from concurrent.futures import ThreadPoolExecutor
from itertools import count, cycle, repeat
from pathlib import Path

from cachecontrol import CacheControl
from lxml import html
from requests import Session
from tqdm import tqdm

from utils import dump, get, get_headers, mkdirs

NB_RETRIES = 3


def main():
    # create dirs
    root_dir = Path(__file__).resolve().parents[1]
    dump_dir = root_dir / 'dump'
    mkdirs(dump_dir)

    # determine search_urls (should be roughly 0.9B words in total)
    search_urls = [f'https://www.smashwords.com/books/category/1/downloads/0/free/medium/{i}' for i in range(0, 30000 + 1, 20)]

    # get headers (user-agents)
    headers = get_headers(root_dir / 'user-agents.txt')

    # initialize cache-controlled session
    session = CacheControl(Session())

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        # get/write book_page_urls
        book_page_urls = []

        with open(dump_dir / 'book_page_urls.txt', 'w') as f:
            for nb_retry in count(1):
                # break if all search_urls successful
                if not search_urls:
                    break

                # break if max number of retries exceeded
                if nb_retry > NB_RETRIES:
                    print(f'Could not get {len(search_urls)} search pages after {NB_RETRIES} retries.')
                    break

                # maintain a list of failed searches (for future retries)
                failed_search_urls = []

                # get the search_responses
                search_responses = list(tqdm(executor.map(get, search_urls, repeat(session), cycle(headers)), total=len(search_urls), desc='Getting searches'))

                # dump the search_responses
                dump(search_responses, 'search_responses.pkl')

                for search_url, search_r in zip(search_urls, search_responses):
                    if search_r is not None:
                        if search_r.status_code == 200:
                            search_r.encoding = 'utf-8'
                            search_tree = html.fromstring(search_r.content)

                            try:
                                for book_page_url in search_tree.xpath('//a[@class="library-title"]/@href'):
                                    book_page_urls.append(book_page_url)
                                    f.write(book_page_url + '\n')
                            except IndexError:
                                failed_search_urls.append(search_url)
                                print(f'Request failed for {search_url}')
                        else:
                            failed_search_urls.append(search_url)
                            print(
                                f'Request failed for {search_url}: status code [{search_r.status_code}]')

                search_urls = failed_search_urls

        # write book_download_urls.txt
        with open(root_dir / 'book_download_urls.txt', 'w') as f:
            for nb_retry in count(1):
                # break if all book_page_urls successful
                if not book_page_urls:
                    break

                # break if max number of retries exceeded
                if nb_retry > NB_RETRIES:
                    print(
                        f'Could not get {len(book_page_urls)} book pages after {NB_RETRIES} retries.')
                    break

                # maintain a list of failed book_pagees (for future retries)
                failed_book_page_urls = []

                # get the book_page_responses
                book_page_responses = list(tqdm(executor.map(get, book_page_urls, repeat(session), cycle(headers)), total=len(book_page_urls), desc='Getting book pages'))

                # dump the book_page_responses
                dump(book_page_responses, 'book_page_responses.pkl')

                for book_page_url, book_page_r in zip(book_page_urls, book_page_responses):
                    if book_page_r is not None:
                        if book_page_r.status_code == 200:
                            book_page_r.encoding = 'utf-8'
                            book_page_tree = html.fromstring(
                                book_page_r.content)

                            try:
                                # get relevant data
                                script_text = book_page_tree.xpath('//div[@id="contentArea"]/script/text()')[0]
                                _json = json.loads(script_text.split('window.angularData.book = ')[1].split('};')[0] + '}')
                                try:
                                    language = _json['language']['name']

                                    if language == 'English':
                                        formats = _json['formats']

                                        if 'TXT' in formats:
                                            f.write(book_page_tree.xpath('//a[@title="Plain text; contains no formatting"]/@href')[0] + '\n')
                                        else:
                                            continue
                                except KeyError:
                                    continue
                            except IndexError:
                                failed_book_page_urls.append(book_page_url)
                                print(f'Request failed for {book_page_url}')
                        else:
                            failed_book_page_urls.append(book_page_url)
                            print(f'Request failed for {book_page_url}: status code [{book_page_r.status_code}]')

                book_page_urls = failed_book_page_urls


if __name__ == '__main__':
    main()
