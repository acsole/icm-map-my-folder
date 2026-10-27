#!/usr/bin/env python3
"""Cold-run runner — the online half of the cold-run gate. It records walks; it does not judge them.

One question, a fresh session, no memory and no coaching. The model gets two folders (the map and the
repository it maps) behind a free `list_dir` and a metered `read_file`. A hop is a file opened;
`list_dir` is free, as a project file listing is.

Each run is written to walks/transcripts/ as JSON: the question, the configuration, the model and
effort, both commits, every file opened with its SHA-256, the final answer, why it stopped, and the
API message ids. **Judging is `score-walk.py`'s job, offline** — a reader without a key verifies the
walk from the transcript the same way they verify a card from the territory.

    pip install anthropic            # this script only; the scorer needs nothing
    QUESTION_FILE=walks/questions/q01-services.md RUNS=5 \
        TERRITORY_DIR=./your-market-realtor python3 reference/checks/cold-run.py

QUESTION_FILE carries the question and its configuration (see walks/CONTEXT.md):
  catalog_in_context — the map's catalog is in the project, which is what the README tells a reader of
                       an existing map to load, and the one the "catalog + one card" claim is measured in.
  unframed           — the session sees two folder names and must find the map itself; expect more reads.
Both numbers are real; they answer different questions, so the configuration travels with every run.

Without QUESTION_FILE, QUESTION and CATALOG_IN_CONTEXT=1 still work, recorded as question_id `adhoc`;
the scorer only judges transcripts whose question_id matches a question file.

Other settings: MAP_DIR (default: this repo), TERRITORY_DIR, OUT_DIR (default: <map>/walks/transcripts),
MODEL (default claude-opus-5-5), EFFORT (default high), RUNS (default 1), MAX_TURNS (default 12).
Credentials come from ANTHROPIC_API_KEY or an `ant auth login` profile.

Original runner by Gabriel Azoulay. Revised by Andrés Curcio — recording, hashes, question files,
model and effort as settings — from the Comp #11 feedback, with the original author's permission.
The tools, the system prompts and the two configurations are his, unchanged. See CHANGES.md.
"""

import datetime
import hashlib
import json
import os
import posixpath
import subprocess
import sys

from anthropic import Anthropic

MAP = os.path.abspath(os.environ.get("MAP_DIR", os.path.join(os.path.dirname(__file__), "..", "..")))
TERRITORY = os.path.abspath(os.environ.get("TERRITORY_DIR", "./your-market-realtor"))
OUT_DIR = os.environ.get("OUT_DIR", os.path.join(MAP, "walks", "transcripts"))
MODEL = os.environ.get("MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("EFFORT", "high")
RUNS = int(os.environ.get("RUNS", "1"))
MAX_TURNS = int(os.environ.get("MAX_TURNS", "12"))
DEFAULT_CATALOG = "reference/worked-example/CATALOG.md"

ROOTS = {"map": MAP, "repo": TERRITORY}


def file_sha256(path):
    """Same function as in score-walk.py — keep the two in step."""
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def read_frontmatter(path):
    """Same format score-walk.py reads: `key: value`, value parsed as JSON when it parses."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    q = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if not key.strip() or key.lstrip().startswith("#"):
            continue
        try:
            q[key.strip()] = json.loads(value.strip())
        except ValueError:
            q[key.strip()] = value.strip()
    return q


def load_question():
    qfile = os.environ.get("QUESTION_FILE", "").strip()
    if qfile:
        q = read_frontmatter(qfile if os.path.isfile(qfile) else os.path.join(MAP, qfile))
        return q["id"], q["question"], q["configuration"], q.get("catalog", DEFAULT_CATALOG)
    cic = os.environ.get("CATALOG_IN_CONTEXT", "").strip()
    in_context = cic not in ("", "0", "false", "False", "no")
    catalog = DEFAULT_CATALOG if cic in ("", "1", "true", "True", "yes") else cic
    return ("adhoc", os.environ.get("QUESTION", "What is Services?"),
            "catalog_in_context" if in_context else "unframed", catalog)


QUESTION_ID, QUESTION, CONFIGURATION, CATALOG_REL = load_question()
if CONFIGURATION not in ("catalog_in_context", "unframed"):
    sys.exit(f"unknown configuration {CONFIGURATION!r}")

CATALOG_PATH = ""
if CONFIGURATION == "catalog_in_context":
    CATALOG_PATH = CATALOG_REL if os.path.isabs(CATALOG_REL) else os.path.join(MAP, CATALOG_REL)
    if not os.path.isfile(CATALOG_PATH):
        sys.exit(f"configuration is catalog_in_context but there is no catalog at {CATALOG_PATH}")
    with open(CATALOG_PATH, encoding="utf-8") as _fh:
        _CATALOG = _fh.read()
    SYSTEM = (
        "You are in a fresh session. You have no memory of any previous conversation and no notes.\n\n"
        "Your project contains one file, a map of a repository. It is reproduced below.\n\n"
        "Two folders are also available to you through tools:\n"
        f"  map  — {MAP}   (the map folder; the catalog below lives at "
        f"{os.path.relpath(os.path.dirname(CATALOG_PATH), MAP)}/)\n"
        f"  repo — {TERRITORY}   (the repository the map describes)\n\n"
        "Use `list_dir` to see what is there and `read_file` to read something. Answer the user's "
        "question.\n\n"
        "--- CATALOG.md ---\n" + _CATALOG
    )
else:
    SYSTEM = (
        "You are in a fresh session. You have no memory of any previous conversation and no notes.\n\n"
        "Two folders are available to you through tools:\n"
        f"  map  — {MAP}\n"
        f"  repo — {TERRITORY}\n\n"
        "Use `list_dir` to see what is there and `read_file` to read something. Answer the user's "
        "question."
    )

TOOLS = [
    {
        "name": "list_dir",
        "description": "List the entries of a directory. Path is relative to a root: "
                       "'map' or 'repo'. Use '.' for the root itself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "enum": ["map", "repo"]},
                "path": {"type": "string"},
                "recursive": {"type": "boolean"},
            },
            "required": ["root", "path"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a file. Path is relative to a root: 'map' or 'repo'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "enum": ["map", "repo"]},
                "path": {"type": "string"},
            },
            "required": ["root", "path"],
        },
    },
]


def safe(root, path):
    base = ROOTS[root]
    full = os.path.normpath(os.path.join(base, path))
    if os.path.commonpath([base, full]) != base:
        raise ValueError("outside root")
    return full


def rel(root, full):
    r = posixpath.normpath(os.path.relpath(full, ROOTS[root]).replace(os.sep, "/"))
    return "." if r in ("", ".") else r


def do_list(listings, root, path, recursive=False):
    full = safe(root, path)
    listings.append(f"{root}:{rel(root, full)}")
    if not os.path.isdir(full):
        return f"not a directory: {path}"
    out = []
    if recursive:
        for dirpath, dirnames, names in os.walk(full):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            r = os.path.relpath(dirpath, full)
            for n in sorted(names):
                p = n if r == "." else os.path.join(r, n)
                out.append(f"{p}  ({os.path.getsize(os.path.join(dirpath, n))} B)")
    else:
        for n in sorted(os.listdir(full)):
            if n == ".git":
                continue
            p = os.path.join(full, n)
            out.append(f"{n}/" if os.path.isdir(p) else f"{n}  ({os.path.getsize(p)} B)")
    return "\n".join(out) or "(empty)"


def do_read(reads, root, path):
    full = safe(root, path)
    found = os.path.isfile(full)
    reads.append({"root": root, "path": rel(root, full), "sha256": file_sha256(full) if found else None})
    if not found:
        return f"no such file: {path}"
    with open(full, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def commit_of(folder):
    """HEAD, with +dirty when the tree has uncommitted changes; 'unknown' outside git."""
    try:
        sha = subprocess.run(["git", "-C", folder, "rev-parse", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", folder, "status", "--porcelain"], capture_output=True,
                               text=True, check=True).stdout.strip()
        return sha + ("+dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def walk(client):
    messages = [{"role": "user", "content": QUESTION}]
    transcript, reads, listings, message_ids = [], [], [], []
    stop_reason, answer = None, ""

    for turn in range(MAX_TURNS):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            thinking={"type": "adaptive"},
            output_config={"effort": EFFORT},
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})
        message_ids.append(resp.id)

        text_blocks = [b.text for b in resp.content if b.type == "text"]
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        transcript.append({
            "turn": turn,
            "stop_reason": resp.stop_reason,
            "text": "\n".join(text_blocks),
            "tool_calls": [{"name": b.name, "input": b.input} for b in tool_uses],
            "usage": {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens},
        })
        stop_reason, answer = resp.stop_reason, "\n".join(text_blocks)

        if resp.stop_reason != "tool_use":
            break

        results = []
        for b in tool_uses:
            try:
                if b.name == "list_dir":
                    content = do_list(listings, b.input["root"], b.input["path"],
                                      b.input.get("recursive", False))
                else:
                    content = do_read(reads, b.input["root"], b.input["path"])
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": content})
            except Exception as exc:  # noqa: BLE001 — surfaced to the model as an error result
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": str(exc), "is_error": True})
        messages.append({"role": "user", "content": results})
    else:
        stop_reason = "max_turns"  # still asking for tools when the turns ran out

    return {
        "schema": "map-my-folder/walk/1",
        "harness": "api-runner",
        "question_id": QUESTION_ID,
        "question": QUESTION,
        "configuration": CONFIGURATION,
        "model": MODEL,
        "effort": EFFORT,
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "map_commit": commit_of(MAP),
        "territory_commit": commit_of(TERRITORY),
        "catalog": ({"path": rel("map", CATALOG_PATH), "sha256": file_sha256(CATALOG_PATH)}
                    if CATALOG_PATH else None),
        "file_reads": reads,
        "listings": listings,
        "turns": len(transcript),
        "max_turns": MAX_TURNS,
        "final_stop_reason": stop_reason,
        "final_answer": answer,
        "message_ids": message_ids,
        "transcript": transcript,
    }


def main():
    client = Anthropic(max_retries=8)
    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for i in range(1, RUNS + 1):
        record = walk(client)
        path = os.path.join(OUT_DIR, f"{QUESTION_ID}.{stamp}.r{i}.json")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(record, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"run {i}/{RUNS}  {len(record['file_reads'])} read(s)  "
              f"stop={record['final_stop_reason']}  -> {os.path.relpath(path)}")
    print(f"\nScore offline:  python3 reference/checks/score-walk.py --walks walks/ --map . "
          f"--territory {os.path.relpath(TERRITORY)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
