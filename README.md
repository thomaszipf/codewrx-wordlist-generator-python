# codewrx-wordlist-generator-python

Another word list generator using Python.

It takes groups of token variants and writes every ordered concatenation
(the Cartesian product across all groups), one per line. Output is streamed
to disk, so memory stays flat no matter how large the result gets — 1,000,000
combinations run in about 0.15 s at ~15 MB peak.

## Requirements

Python 3.9+ (standard library only, no dependencies).

## Usage

```sh
# built-in demo groups
python3 wordlist-generator.py

# from your own config file(s)
python3 wordlist-generator.py groups.cfg -o out.txt

# only count how many combinations would be generated, write nothing
python3 wordlist-generator.py groups.cfg --dry-run
```

| Option | Meaning |
| --- | --- |
| `config...` | One or more config files. Omit to use the built-in demo. |
| `-o`, `--output` | Output file (default: `wordlist_<timestamp>.txt`). |
| `-n`, `--dry-run` | Print the combination count only, write nothing. |

Progress messages go to stderr, so the wordlist stays clean if you redirect
stdout.

## Config format

One group per line; variants are comma-separated. Order is preserved and
drives the output order. A trailing comma adds an empty variant, meaning
"this group may be skipped". Lines starting with `#` are comments.

```
# groups.cfg
Word1-V1, Word1-V2, Word1-V3,
Word2-V1, Word2-V2, Word2-V3
```

The first group above has a trailing comma, so it may be skipped; the second
is always present. Combinations that come out completely empty are dropped,
so the output never contains a blank line.

See [`example-output/`](example-output/) for a sample `demo.cfg` and the
1023-line `wordlist.txt` generated from it.
