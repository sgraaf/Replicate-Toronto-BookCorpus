#!/usr/bin/env python
from pathlib import Path

from tqdm import tqdm

from utils import bytes_to_str, read_bytes, text_to_sentences


def main():
    # create dirs
    root_dir = Path(__file__).resolve().parents[1]
    data_dir = root_dir / "data"

    if not data_dir.exists():
        raise RuntimeError(f"data_dir does not exist: {str(data_dir)}")

    # get book_files
    book_files = sorted(data_dir.glob("*.txt"))

    with open("replica.txt", "w", encoding="utf-8") as out_f:
        for book_file in tqdm(
            book_files, total=len(book_files), desc="Pre-processing books"
        ):
            book_bytes = read_bytes(book_file)
            book_text = bytes_to_str(book_bytes)
            book_sentences = text_to_sentences(book_text)
            out_f.write(book_sentences)
            out_f.write("\n\n\n")  # 3 empty lines between distinct books


if __name__ == "__main__":
    main()
