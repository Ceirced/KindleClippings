from __future__ import annotations

import re

from datetime import datetime
from loguru import logger


class Highlight:
    def __init__(
        self,
        text: str,
        book_title: str,
        start_position: int | None,
        end_position: int | None,
        created_at: datetime,
        page: int | None = None,
        author: str | None = None,
    ):
        self.text = text
        self.book_title = book_title
        self.page = page
        self.start_position = start_position
        self.end_position = end_position
        self.created_at = created_at
        self.author = author

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Highlight(text={self.text}, book_title={self.book_title} page={self.page}, start_position={self.start_position}, end_position={self.end_position}, created_at={self.created_at})"

    @staticmethod
    def parse_clipping(text: str) -> Highlight:
        lines = [line for line in text.split("\n") if line]

        title_and_author = lines[0]
        author = title_and_author.split("(")[-1].replace(")", "")
        title = title_and_author.split("(" + author)[0].strip()
        meta = lines[1]
        meta_debugs = meta.split(" | ")

        if len(meta_debugs) == 2:
            first_meta, second_meta = meta_debugs
        else:
            page_meta, first_meta, second_meta = meta_debugs
            page = extract_page(page_meta)

        start_position, end_position = extract_positions(first_meta)
        created_at = extract_datetime(second_meta)
        highlight = lines[2]

        return Highlight(
            text=highlight,
            book_title=title,
            start_position=start_position,
            end_position=end_position,
            created_at=created_at,
            page=page if "page" in locals() else None,
            author=author,
        )


def extract_page(text: str) -> int:
    match = re.search(r'(\d+)', text)
    if match:
        return int(match.group())
    else:
        raise ValueError("Invalid page")


def extract_datetime(text: str) -> datetime:
    match = re.search(r'(\d{1,2}\. \w+ \d{4}) (\d{2}:\d{2}:\d{2})', text)
    if match:
        date_str, time_str = match.groups()
        return datetime.strptime(f"{date_str} {time_str}", "%d. %B %Y %H:%M:%S")
    else:
        raise ValueError("Invalid datetime")


def extract_positions(text: str) -> tuple[int, int]:
    """
    Extracts the start and end positions from the first meta part of the highlight"""
    match = re.search(r'(\d+)-(\d+)', text)
    if match:
        start, end = map(int, match.groups())
        return start, end
    else:
        raise ValueError("Invalid position")


example = """==========
﻿The Game (Neil Strauss)
- Deine Markierung bei Position 6470-6471 | Hinzugefügt am Montag, 25. September 2023 22:42:15

The secret to making someone think they’re in love with you is to occupy their thoughts,
==========
﻿The Game (Neil Strauss)
- Deine Markierung bei Position 6520-6520 | Hinzugefügt am Montag, 25. September 2023 22:48:35

Leave her better than you found her.
==========
Permanent Record · Meine Geschichte (German Edition) (Edward Snowden)
- Deine Markierung auf Seite 49 | bei Position 738-740 | Hinzugefügt am Montag, 16. September 2024 22:36:09

In den neunziger Jahren war das Internet noch nicht der größten Schandtat des Digitalzeitalters zum Opfer gefallen: den Bemühungen von Regierungen und Unternehmen, die Online-Identitäten eines Nutzers so eng wie möglich an seine tatsächliche Offline-Identität zu koppeln.
"""

if __name__ == "__main__":
    highlights = example.split("==========")
    for highlight_text in highlights:
        if not highlight_text:
            continue
        highlight = Highlight.parse_clipping(highlight_text)
        logger.info(
            f'parsed highlight from {highlight.book_title} by {highlight.author} on page {highlight.page} created at {highlight.created_at}'
        )
        print('*' * 50)
