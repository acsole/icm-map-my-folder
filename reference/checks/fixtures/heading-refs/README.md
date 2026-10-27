# Heading-refs fixture

A blank file with two headings, an engine file that reaches them three ways, and two decoys:

| Line | What it is | Must be |
|---|---|---|
| `engine/framework.md:3` | the whole heading, quoted, with the file named | found, exact |
| `engine/framework.md:5` | the heading as a phrase, with the file named | found, exact |
| `engine/framework.md:7` | only the heading's distinctive word, with the file named | found, topic |
| `engine/framework.md:9` | the heading, but no file named | not found |
| `other/note.md:3` | a reference outside the engine folder | not found |

*Added by Andrés Curcio in the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission.*
