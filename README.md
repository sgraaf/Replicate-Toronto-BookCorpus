# Replicate Toronto BookCorpus

This repository contains code to replicate the no-longer-available Toronto BookCorpus dataset. To this end, it scrapes and downloads books from [Smashwords](https://www.smashwords.com/), the source of the original dataset. Similarly, all books are written in English and contain at least 20k words. 

## Requirements
- python 3.6+
- cachecontrol
- lxml
- requests
- tqdm

## Usage
Replicating the Toronto BookCorpus dataset consists of three parts:
1. Getting the download URLs of the plaintext books (optional)
2. Downloading the plaintext books
3. Pre-processing the plaintext books (WIP)

### 1. Getting the download URLs of the plaintext books (optional)
The first part is optional, as I have already provided a list of download URLS in `book_download_urls.txt` ready to use. Nonetheless, you can recreate this list as follows:
```python
python src/get_book_urls.py
```

### 2. Downloading the plaintext books
Provided you have a list of download URLS in `book_download_urls.txt`, you can download the plaintext book as follows:
```python
python src/download_books.py
```

Please note that you have to execute the above command multiple times (29 times to be exact), from multiple IP-addresses, as [Smashwords](https://www.smashwords.com/) (temporarily) blocks any IP-address after 500 downloads. If you know of a way to automate this through python, please submit a pull request!

### 3. Pre-processing the plaintext books (WIP)
After downloading the plaintext books, they need to be pre-processed in order to be a true replica of the Toronto BookCorpus dataset. This part is still WIP for the moment and will follow soon.

### Acknowledgement
This project builds upon [bookcorpus](https://github.com/soskek/bookcorpus).

### Disclaimer
Please read the Smashwords [Terms of Service](https://www.smashwords.com/about/tos) carefully. Furthermore, please use the code in this repository responsibly and adhere to any copyright (and related) laws. I am not responsible for any copyright / plagiarism / legal issues that may arise from using the code in this repository.

### License
Replicate Toronto BookCorpus is open-source and licensed under GNU GPL, Version 3.