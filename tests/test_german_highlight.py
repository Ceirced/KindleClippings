from src.clippings import Highlight, Bookmark, Note, parse_clipping

example_highlights = """==========
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

example_bookmarks = """The 80/20 Principle: The Secret to Achieving More with Less (Richard Koch)
- Dein Lesezeichen bei Position 2993 | Hinzugefügt am Mittwoch, 11. Oktober 2023 08:02:00


==========
The 80/20 Principle: The Secret to Achieving More with Less (Richard Koch)
- Dein Lesezeichen bei Position 3015 | Hinzugefügt am Mittwoch, 11. Oktober 2023 13:20:08


==========
The 80/20 Principle: The Secret to Achieving More with Less (Richard Koch)
- Dein Lesezeichen bei Position 3039 | Hinzugefügt am Mittwoch, 11. Oktober 2023 14:10:10
"""

example_notes = """Die 24 Gesetze der Verführung (Robert Greene)
- Deine Notiz auf Seite 139 | bei Position 2128 | Hinzugefügt am Donnerstag, 10. Oktober 2024 08:40:08

Interessant, vielleicht immer mal wieder oasch sein
==========
Die 24 Gesetze der Verführung (Robert Greene)
- Deine Notiz auf Seite 148 | bei Position 2268 | Hinzugefügt am Donnerstag, 10. Oktober 2024 09:15:53

Warum lässt die Eigenschaft des ersten nach wenn der andere auf Trab ist?
==========
Die 24 Gesetze der Verführung (Robert Greene)
- Deine Notiz auf Seite 148 | bei Position 2268 | Hinzugefügt am Donnerstag, 10. Oktober 2024 09:17:20

Warum lässt die Eigenschaft nach wenn man auf auf Trab ist?
==========
"""


def test_detect_clipping_type():
    clipping_examples = [
        example_highlights,
        example_bookmarks,
        example_notes,
    ]
    for clipping in clipping_examples:
        clippings = clipping.split("==========\n")
        for example in clippings:
            if example:
                assert parse_clipping(example) is not None


def test_notes():
    clippings = example_notes.split("==========\n")
    notes = [Note.from_clipping(clipping) for clipping in clippings if clipping]
    assert len(notes) == 3
    assert notes[0].book_title == "Die 24 Gesetze der Verführung"
    assert notes[0].author == "Robert Greene"
    assert notes[0].position == 2128
    assert notes[0].page == 139
    assert notes[0].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-10-10 08:40:08"
    assert notes[0].text == "Interessant, vielleicht immer mal wieder oasch sein"

    assert notes[1].book_title == "Die 24 Gesetze der Verführung"
    assert notes[1].author == "Robert Greene"
    assert notes[1].position == 2268
    assert notes[1].page == 148
    assert notes[1].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-10-10 09:15:53"
    assert (
        notes[1].text
        == "Warum lässt die Eigenschaft des ersten nach wenn der andere auf Trab ist?"
    )
    assert notes[2].book_title == "Die 24 Gesetze der Verführung"
    assert notes[2].author == "Robert Greene"
    assert notes[2].position == 2268
    assert notes[2].page == 148
    assert notes[2].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-10-10 09:17:20"


def test_bookmarks():
    clippings = example_bookmarks.split("==========\n")
    bookmarks = [Bookmark.from_clipping(clipping) for clipping in clippings if clipping]
    assert len(bookmarks) == 3
    assert (
        bookmarks[0].book_title
        == "The 80/20 Principle: The Secret to Achieving More with Less"
    )
    assert bookmarks[0].author == "Richard Koch"
    assert bookmarks[0].position == 2993
    assert (
        bookmarks[0].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2023-10-11 08:02:00"
    )
    assert (
        bookmarks[1].book_title
        == "The 80/20 Principle: The Secret to Achieving More with Less"
    )
    assert bookmarks[1].author == "Richard Koch"
    assert bookmarks[1].position == 3015
    assert (
        bookmarks[1].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2023-10-11 13:20:08"
    )
    assert (
        bookmarks[2].book_title
        == "The 80/20 Principle: The Secret to Achieving More with Less"
    )
    assert bookmarks[2].author == "Richard Koch"
    assert bookmarks[2].position == 3039
    assert (
        bookmarks[2].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2023-10-11 14:10:10"
    )
    assert (
        repr(bookmarks[0])
        == "Bookmark(book_title=The 80/20 Principle: The Secret to Achieving More with Less, created_at=2023-10-11 08:02:00, position=2993, page=None, author=Richard Koch, text=None)"
    )


def test_highlights():
    clippings = example_highlights.split("==========\n")
    highlights = [
        Highlight.from_clipping(clipping) for clipping in clippings if clipping
    ]
    assert len(highlights) == 3
    assert highlights[0].book_title == "The Game"
    assert highlights[0].author == "Neil Strauss"
    assert highlights[0].position == (6470, 6471)
    assert (
        highlights[0].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2023-09-25 22:42:15"
    )

    assert highlights[1].book_title == "The Game"
    assert highlights[1].author == "Neil Strauss"
    # assert highlights[1].position == (6520, 6520)
    assert (
        highlights[1].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2023-09-25 22:48:35"
    )

    assert (
        highlights[2].book_title
        == "Permanent Record · Meine Geschichte (German Edition)"
    )
    assert highlights[2].author == "Edward Snowden"
    assert highlights[2].page == 49
    # assert highlights[2].position == 738, 740
    assert (
        highlights[2].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-09-16 22:36:09"
    )
    assert (
        repr(highlights[0])
        == "Highlight(book_title=The Game, created_at=2023-09-25 22:42:15, position=(6470, 6471), page=None, author=Neil Strauss, text=The secret to making someone think they’re in love with you is to occupy their thoughts,)"
    )
