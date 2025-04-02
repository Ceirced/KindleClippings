from __future__ import annotations

import re
import locale

from datetime import datetime

WORDS_FOR_BOOKMARK = ["Lesezeichen", "Bookmark", "Bookmarklet"]
WORDS_FOR_HIGHLIGHT = ["Markierung", "Highlight"]
WORDS_FOR_NOTE = ["Notiz", "Note", "Anmerkung", "Annotation"]

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


def parse_clipping(text: str) -> Clipping:
    """
    Parses a clipping text and returns a Clipping object.
    """
    # check if the text is a note or a highlight or a bookmark
    first_line = text.split("\n")[1]
    if any(word in first_line for word in WORDS_FOR_BOOKMARK):
        return Bookmark.from_clipping(text)

    elif any(word in first_line for word in WORDS_FOR_HIGHLIGHT):
        return Highlight.from_clipping(text)

    elif any(word in first_line for word in WORDS_FOR_NOTE):
        return Note.from_clipping(text)

    else:
        print("first line:::", first_line.split())
        raise ValueError("Unknown clipping type. Cannot parse the text.")


class Clipping:
    def __init__(
        self,
        book_title: str,
        created_at: datetime,
        position: int | tuple[int, int],
        author: str,
        page: int | None = None,
        text: str | None = None,
    ):
        self.book_title = book_title
        self.created_at = created_at
        self.position = position
        self.page = page
        self.author = author
        self.text = text

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({', '.join([f'{key}={value}' for key, value in self.__dict__.items()])})"

    @classmethod
    def from_clipping(cls, text: str):
        lines = [line for line in text.split("\n") if line]

        title_and_author = lines[0]
        author = title_and_author.split("(")[-1].replace(")", "")
        title = title_and_author.split("(" + author)[0].strip().replace("\ufeff", "")
        meta = lines[1]
        meta_debugs = meta.split(" | ")

        if len(meta_debugs) == 2:
            first_meta, second_meta = meta_debugs
        else:
            page_meta, first_meta, second_meta = meta_debugs
            page = extract_page(page_meta)

        position = extract_positions(first_meta)
        created_at = extract_datetime(second_meta)
        if len(lines) > 2:
            clipping_text = lines[2]
        else:
            clipping_text = None

        return cls(
            book_title=title,
            created_at=created_at,
            position=position,
            author=author,
            page=page if "page" in locals() else None,
            text=clipping_text,
        )


class Note(Clipping):
    def __init__(
        self,
        book_title: str,
        created_at: datetime,
        text: str,
        position: int,
        author: str,
        page: int | None = None,
    ):
        self.text = text
        super().__init__(book_title, created_at, position, author, page, text)

    @classmethod
    def from_clipping(cls, text: str) -> Note:
        clipping = super().from_clipping(text)
        position = clipping.position

        if not isinstance(position, int):
            raise ValueError("Position should be a single integer for notes.")

        note = cls(
            book_title=clipping.book_title,
            created_at=clipping.created_at,
            text=clipping.text,
            position=position,
            author=clipping.author,
            page=clipping.page,
        )
        return note


class Bookmark(Clipping):
    def __init__(
        self,
        book_title: str,
        created_at: datetime,
        position: int,
        author: str,
        page: int | None = None,
        **kwargs,
    ):
        super().__init__(book_title, created_at, position, author, page)

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({', '.join([f'{key}={value}' for key, value in self.__dict__.items()])})"


class Highlight(Clipping):
    def __init__(
        self,
        position: tuple[int, int],
        book_title: str,
        created_at: datetime,
        author: str,
        text: str,
        page: int | None = None,
    ):
        super().__init__(book_title, created_at, position, author, page, text)


def extract_page(text: str) -> int:
    match = re.search(r"(\d+)", text)
    if match:
        return int(match.group())
    else:
        raise ValueError("Invalid page")


def extract_datetime(text: str) -> datetime:
    match = re.search(r"(\d{1,2}\. \w+ \d{4}) (\d{2}:\d{2}:\d{2})", text)
    if match:
        date_str, time_str = match.groups()
        return datetime.strptime(f"{date_str} {time_str}", "%d. %B %Y %H:%M:%S")
    else:
        raise ValueError("Invalid datetime")


def extract_positions(text: str) -> int | tuple[int, int]:
    """
    Extracts the start and end positions from the first meta part of the highlight"""
    range_match = re.search(r" (\d+)-(\d+)$", text)
    single_match = re.search(r" (\d+)$", text)
    if range_match:
        start, end = map(int, range_match.groups())
        return start, end
    elif single_match:
        position = int(single_match.group(1))
        return position
    else:
        raise ValueError("Invalid position")
