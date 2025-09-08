from pathlib import Path
from collections import OrderedDict

from loguru import logger
import mdutils  # type: ignore

from src.clippings import parse_clipping, Clipping, Note, Highlight

OUTOUT_DIR = Path("output")
if not OUTOUT_DIR.exists():
    OUTOUT_DIR.mkdir(parents=True, exist_ok=True)


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
    # Replace forward slashes and colons in both title and author to avoid file path issues
    safe_book_title = book_title.replace("/", "-").replace(":", " -")
    safe_author = author.replace("/", "-").replace(":", " -")
    file_name = f"{safe_book_title} - {safe_author}.md"
    file_path = OUTOUT_DIR / file_name
    if file_path.exists():
        file_path.unlink()
    # create a new file
    md_file = mdutils.MdUtils(file_name=str(file_path))
    # add the clippings to the file

    notes = [clipping for clipping in clippings if isinstance(clipping, Note)]

    highlights = [clipping for clipping in clippings if isinstance(clipping, Highlight)]

    matched_notes_and_highlights, unmatched_notes, unmatched_highlights = (
        match_notes_and_hightlights(notes, highlights)
    )
    if len(unmatched_notes) > 0:
        logger.warning(
            f"did not match {len(unmatched_notes)} with highlights in {book_title} by {author}"
        )
    if len(matched_notes_and_highlights) == 0:
        return

    sorted_highlights_with_matched_notes = sorted(
        matched_notes_and_highlights
        + [(None, highlight) for highlight in unmatched_highlights],
        key=lambda x: x[1].position[0],
    )

    for note, highlight in sorted_highlights_with_matched_notes:
        if highlight.page:
            md_file.new_line(f"S {highlight.page}")
        else:
            md_file.new_line(f"P {highlight.position[0]}")

        md_file.new_line(highlight.created_at.strftime("%A, %d. %B %Y %H:%M"))
        md_file.new_line(f">{highlight.text}\n")
        if note:
            md_file.new_line(note.text)
        md_file.new_line("\n---\n")

    if unmatched_notes:
        md_file.new_line(f"## Unmatched Notes ({len(unmatched_notes)})\n")
        # add the unmatched notes to the file
        for note in unmatched_notes:
            if note.page:
                md_file.new_line(f"S {note.page}")
            else:
                md_file.new_line(f"P {note.position}")
            md_file.new_line(note.created_at.strftime("%A, %d. %B %Y %H:%M"))
            md_file.new_line(note.text)
            md_file.new_line("\n---\n")

    # save the file
    md_file.create_md_file()


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
            if note.position == highlight.position[1]:
                matched_notes_and_highlights.append((note, highlight))
                break
                # highlights.remove(highlight)
        else:
            unmatched_notes.append(note)
    matched_highlights = {highlight for note, highlight in matched_notes_and_highlights}
    unmatched_highlights = set(highlights) - matched_highlights
    return matched_notes_and_highlights, unmatched_notes, unmatched_highlights


book_titles = list(clippings_by_book.keys())

for book_title in book_titles:
    parsed_clippings = clippings_by_book[book_title]
    save_book_clippings_to_file(parsed_clippings)
