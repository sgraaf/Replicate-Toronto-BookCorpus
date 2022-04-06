# Replicate Toronto BookCorpus

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This repository contains code to replicate the no-longer-available Toronto BookCorpus dataset. To this end, it scrapes and downloads books from [Smashwords](https://www.smashwords.com/), the source of the original dataset. Similarly, all books are written in English and contain at least 20k words.

## Usage

Replicating the Toronto BookCorpus dataset consists of three steps:

1. Getting the URLs of the plaintext books to download (optional)
2. Downloading the plaintext books
3. Pre-processing the plaintext books

### 1. Getting the URLs of the plaintext books to download (optional)

The first step is optional, as I have already provided a list of download URLS in [data/book_urls.txt](./data/book_urls.txt) ready to use. Nonetheless, you can recreate this list as follows:

```python
python src/get_book_urls.py
```

### 2. Downloading the plaintext books

Provided you have a list of book URLs in [data/book_urls.txt](./data/book_urls.txt), you can download the plaintext books as follows:

```python
python src/download_books.py
```

Please note that you have to execute the above command multiple times (~30 times to be more precise), from multiple IP-addresses, as [Smashwords](https://www.smashwords.com/) (temporarily) blocks any IP-address after 500 downloads. If you know of a way to automate this through Python, please submit a PR!

### 3. Pre-processing the plaintext books

After downloading the plaintext books, they need to be pre-processed in order to be a true replica of the Toronto BookCorpus dataset (sentence tokenized and one sentence per line). This can be accomplished as follows:

```python
python src/preprocess_books.py
```

## Acknowledgement

This project builds upon [bookcorpus](https://github.com/soskek/bookcorpus).

## Disclaimer

Please read the Smashwords [Terms of Service](https://www.smashwords.com/about/tos) carefully. Furthermore, please use the code in this repository responsibly and adhere to any copyright (and related) laws. I am not responsible for any copyright / plagiarism / legal issues that may arise from using the code in this repository.

## License

Replicate Toronto BookCorpus is open-source and licensed under GNU GPL, Version 3.
