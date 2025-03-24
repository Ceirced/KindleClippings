from src.clippings import Highlight

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


def test_highlight():
    clippings = example.split("==========\n")
    highlights = [
        Highlight.from_clipping(clipping) for clipping in clippings if clipping
    ]
    assert len(highlights) == 3
    assert highlights[0].book_title == "The Game"
    assert highlights[0].author == "Neil Strauss"
    assert highlights[0].start_position == 6470
    assert highlights[0].end_position == 6471
    assert highlights[0].created_at == "2023-09-25 22:42:15"

    assert highlights[1].book_title == "The Game"
    assert highlights[1].author == "Neil Strauss"
    assert highlights[1].start_position == 6520
    assert highlights[1].end_position == 6520
    assert highlights[1].created_at == "2023-09-25 22:48:35"

    assert (
        highlights[2].book_title
        == "Permanent Record · Meine Geschichte (German Edition)"
    )
    assert highlights[2].author == "Edward Snowden"
    assert highlights[2].page == 49
    assert highlights[2].start_position == 738
    assert highlights[2].end_position == 740
    assert highlights[2].created_at == "2024-09-16 22:36:09"
