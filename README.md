# password_gen

A lightweight **Python CLI password generator**.

It can generate:
- a single random password,
- a fixed number of passwords, or
- **all permutations** of a given character set (use with care).

It supports a configurable length range, optional starting/prefix characters, optional output to a file, and writes runtime details to a log file.

> Security note: this project can write generated passwords to disk (`password.txt` or a custom output file). Treat any generated passwords as secrets.

---

## Features

- CLI interface built with `argparse`
- Configurable **password length range** (`--length MIN MAX`)
- Optional **prefix / starting characters** (`--testWords ...`)
- Character set can be user-provided (`--words ...`) or randomly sampled from an internal allowed set
- Three generation modes (mutually exclusive):
  - `-L` generate **one** password
  - `+L` generate **all permutations** within the length range
  - `/L N` generate **N unique** passwords
- Optional output redirection to a file (`--output FILE`)
- Logging to `password.log`

---

## Project layout

| Path | Purpose |
|------|---------|
| `program.py` | Main entry point. Defines the CLI, validates input, generates passwords, prints results, and logs events. |
| `requirements.txt` | Python dependencies for the project. |
| `password.txt` | Example output file committed to the repo (sample generated passwords). |
| `password.log` | **Generated at runtime**. Log file created/appended by `program.py`. |
| `program/` | Currently contains `.idea/` (JetBrains/PyCharm project metadata). Not used by the generator at runtime. |
| `.gitignore` | Standard Python ignores. Note: `.idea/` is *not* ignored by default (it’s commented out). |
| `.gitattributes` | Git line-ending normalization (`* text=auto`). |
| `LICENSE` | MIT License. |

---

## Requirements

- Python 3.x
- pip

Dependencies are listed in `requirements.txt`.

> Note: `requirements.txt` in this repo appears to be saved with a non-UTF8 encoding (it contains NUL characters when viewed as text). If `pip install -r requirements.txt` fails, see **Troubleshooting**.

---

## Installation

Create a virtual environment and install dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, you can either adjust execution policy or use `cmd.exe`:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## Usage

Run from the repository root:

```powershell
python program.py
```

### Important: CLI prefix characters

This script configures argparse with:

- `prefix_chars="-+/"`

That means options can start with `-`, `+`, or `/`.

In particular, generation mode flags include **`+L`** and **`/L`** (Windows-style).

---

## Command-line options

### `-w`, `--words`
Provide the characters to use when generating passwords.

- Accepts one or more tokens, e.g. `-w a b c 1 2 3`
- Validation is strict: **every provided character must be in the allowed set**:
  - ASCII letters: `a-z`, `A-Z`
  - digits: `0-9`
  - symbols: `!@#$%^&*()`

If `--words` is omitted, the generator will create a random internal character list of a random length.

### `-t`, `--testWords`
Provide starting/prefix characters that will be prepended to every generated password.

Example: `-t b a n` makes passwords start with `ban`.

Validation uses the same allowed set as `--words`.

### `-l`, `--length MIN MAX`
Set the inclusive range for password length.

Default: `4 8`

Note: the script subtracts the length of `--testWords` from this range internally so that:

- total length (prefix + generated part) matches the requested min/max.

### `-o`, `--output FILE`
Append generated passwords to a file.

- Uses append mode (`a`)
- Prints to console *and* writes to the file

### Generation mode (mutually exclusive)
These options are mutually exclusive; pick at most one.

#### `-L`
Generate **one** password.

This sets the internal `L` flag using `store_false` and is effectively the “single password” mode.

#### `+L`
Generate **all permutations** of the provided `--words` character set for lengths in the requested range.

Warning: this grows extremely fast and can produce huge output.

#### `/L N`
Generate **N unique** passwords.

- `N` must be `>= 0`
- The script attempts to avoid duplicates by storing and checking already-produced passwords.

---

## Examples

### 1) Generate a single password (default behavior)

```powershell
python program.py -L
```

### 2) Generate 10 passwords and write them to `password.txt`

```powershell
python program.py /L 10 -o password.txt
```

### 3) Generate passwords that start with `ban`, length 6–10

```powershell
python program.py -t b a n -l 6 10 /L 5
```

### 4) Use a specific character set

```powershell
python program.py -w a b c 1 2 3 ! @ -l 8 12 /L 5
```

### 5) Generate all permutations (use cautiously)

```powershell
python program.py +L -w a b c -l 2 4
```

---

## Output files

### `password.log` (generated)

`program.py` configures a logger named `password_logger` and appends logs to:

- `password.log` (UTF-8)

It records:
- successful password generation events,
- invalid argument errors,
- interruptions (Ctrl+C / KeyboardInterrupt).

### `password.txt` (included)

This repo includes a `password.txt` file containing sample generated values. If you use `--output password.txt`, new lines will be appended.

---

## Known behavior and edge cases

- Allowed characters are limited to: letters, digits, and `!@#$%^&*()`.
- If `--testWords` length is greater than or equal to the maximum length, the script raises an error.
- Very small ranges after subtracting the prefix can be adjusted internally (if min becomes 0, it’s bumped to 1).
- `+L` (all permutations) can take a long time and generate massive output.

---

## Troubleshooting

### `pip install -r requirements.txt` fails / requirements file looks corrupted

`requirements.txt` appears to be saved with an unusual encoding (it contains NUL bytes). If pip can’t parse it:

- Open `requirements.txt` in an editor that can change encoding.
- Re-save it as **UTF-8** (no BOM).
- Ensure it contains the intended dependency line (it visually appears to be `quantumrandom==1.9.0`).

(Only do this if you intend to fix dependencies; this README documents the current repo state.)

### No output is produced

- Ensure you’re running from the repo root.
- Try explicit single-password mode:
  - `python program.py -L`

### “wrong value for words” error

Your `--words` or `--testWords` included a character outside the allowed set.

### Output file isn’t updated

- `--output` uses append mode. Check you’re looking at the right file.
- If you have permission issues, try writing to a path you own (like your user profile directory).

---

## License

MIT License. See `LICENSE`.
