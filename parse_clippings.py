from pathlib import Path

# import ordererdict
from collections import OrderedDict

from loguru import logger

from src.clippings import parse_clipping, Clipping, Note, Highlight, Bookmark


# read the txt file
file = Path("My Clippings.txt")

file_content = file.read_text(encoding="utf-8")
# split the content into clippings
clippings = file_content.split("==========\n")
# parse the clippings
parsed_clippings = [parse_clipping(clipping) for clipping in clippings if clipping]
# print the parsed clippings
for clipping in parsed_clippings:
    if not isinstance(clipping, Clipping):
        raise ValueError("Clipping is not of type Clipping")

    # get all the different book titles
books = set(clipping.book_title for clipping in parsed_clippings)

logger.info(f"Number of Books found: {len(books)}")

# divide the clippings into books
clippings_by_book = OrderedDict()
for book in books:
    clippings_by_book[book] = [
        clipping for clipping in parsed_clippings if clipping.book_title == book
    ]


def save_book_clippings_to_file(clippings: list[Clipping]):
    book_title = clippings[0].book_title
    author = clippings[0].author

    #  make sure that all clippings have the same book title and author
    for clipping in clippings:
        assert clipping.book_title == book_title
        if not clipping.author == author:
            print(
                f"Clipping author {clipping.author} does not match the book title {book_title} author {author}"
            )
    file_name = f"{book_title} - {author}.txt"
    file_path = Path(file_name)

    notes = [clipping for clipping in clippings if isinstance(clipping, Note)]

    highlights = [clipping for clipping in clippings if isinstance(clipping, Highlight)]

    bookmarks = [clipping for clipping in clippings if isinstance(clipping, Bookmark)]
    matched_notes_and_highlights, unmatched_notes = match_notes_and_hightlights(
        notes, highlights
    )

    if len(unmatched_notes) > 0:
        logger.warning(
            f"did not match {len(unmatched_notes)} with highlights in {book_title} by {author}"
        )
        print(f"book_title: {book_title}")
        for note in unmatched_notes:
            print(f"UNMTACHED note: {note}\n position: {note.position}\n")

        # for highlight in highlights:
        #     print(f"highlight: {highlight}\n position: {highlight.position}\n")
    if len(matched_notes_and_highlights) == len(notes) and len(notes) > 0:
        logger.success(
            f"All {len(matched_notes_and_highlights)} notes matched with highlights in {book_title} by {author}"
        )

    print(f"\n\n\n")

    logger.info(
        f'Found {len(notes)} notes, {len(highlights)} highlights and {len(bookmarks)} bookmarks in "{book_title}" by {author}'
    )


def match_notes_and_hightlights(notes: list[Note], highlights: list[Highlight]):
    """match the notes and hightlights that belong togehter and return the in the tuple, return the rest of the highlights as a list, reutrn the rest of the notes as a list

    Args:
        notes (list[Note]): _description_
        highlights (list[Highlight]): _description_

    """
    matched_notes_and_highlights = []
    unmatched_notes = []
    for note in notes:
        # print(f"note: {note}\n position: {note.position}\n")
        for highlight in highlights:
            if note.position in range(
                highlight.position[0],
                highlight.position[1] + 1,
            ):
                matched_notes_and_highlights.append((note, highlight))
                break
                # highlights.remove(highlight)
        else:
            unmatched_notes.append(note)

    unmatched_highlights = highlights
    return matched_notes_and_highlights, unmatched_notes


book_titles = list(clippings_by_book.keys())

for book_title in book_titles:
    clippings = clippings_by_book[book_title]
    save_book_clippings_to_file(clippings)
