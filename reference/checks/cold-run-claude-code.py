#!/usr/bin/env python3
"""Cold-run recorder, second harness — the walk run through the Claude Code CLI instead of the API.

Same question files, same system prompt, same transcript format as `cold-run.py`, so `score-walk.py`
judges both. What differs is who carries the model: here `claude -p` (headless Claude Code, signed in
with a Claude subscription) instead of a direct API call with a key. Its tools are Claude Code's own
`Read` (a hop) and `Glob` (a listing, free), restricted to those two.

**This is a different harness, and every transcript says so** (`"harness": "claude-code-headless"`).
The scorer gives each harness its own verdict and never pools them: a walk through Claude Code is
real evidence about the map, but it is not the API run under another name.

    QUESTION_FILE=walks/questions/q01-services.md RUNS=5 \
        TERRITORY_DIR=../your-market-realtor python3 reference/checks/cold-run-claude-code.py

Isolation — the walk must start cold. The CLI would otherwise load the user's own CLAUDE.md files,
auto-memory, settings, hooks and MCP servers into the reader's context. Every run therefore sets
CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 and CLAUDE_CODE_DISABLE_AUTO_MEMORY=1, drops the variables a parent
Claude session exports, and passes --setting-sources "" --strict-mcp-config --disable-slash-commands
--exclude-dynamic-system-prompt-sections --no-session-persistence, with --system-prompt replacing the
default one. Check it yourself with ISOLATION_PROBE=1, which asks the reader what context it was
given and prints the answer instead of running the walk.

One thing this cannot remove: the CLI still tells the reader the signed-in account's email and some
environment facts (platform, date, working folders). Only an API key with --bare turns that off,
which is cold-run.py's job. The email is not about the map, so it does not help the walk; and any
email address the reader repeats is replaced with "[email redacted]" before the transcript is
written, with the count kept in "redactions".

Settings: MAP_DIR, TERRITORY_DIR, OUT_DIR, MODEL (default claude-opus-5-5), EFFORT (default high),
RUNS (default 1), CLAUDE_BIN (default `claude` on PATH), TIMEOUT seconds per run (default 600).

Written by Andrés Curcio for the revision of Map My Folder (original by Gabriel Azoulay), with the
original author's permission. See CHANGES.md.
"""

import datetime
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys

MAP = os.path.abspath(os.environ.get("MAP_DIR", os.path.join(os.path.dirname(__file__), "..", "..")))
TERRITORY = os.path.abspath(os.environ.get("TERRITORY_DIR", "../your-market-realtor"))
OUT_DIR = os.environ.get("OUT_DIR", os.path.join(MAP, "walks", "transcripts"))
MODEL = os.environ.get("MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("EFFORT", "high")
RUNS = int(os.environ.get("RUNS", "1"))
TIMEOUT = int(os.environ.get("TIMEOUT", "600"))
CLAUDE = os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude"
DEFAULT_CATALOG = "reference/worked-example/CATALOG.md"
HARNESS = "claude-code-headless"

ROOTS = {"map": MAP, "repo": TERRITORY}


def file_sha256(path):
    """Same function as in score-walk.py and cold-run.py — keep the three in step."""
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


def commit_of(folder):
    try:
        sha = subprocess.run(["git", "-C", folder, "rev-parse", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", folder, "status", "--porcelain"], capture_output=True,
                               text=True, check=True).stdout.strip()
        return sha + ("+dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def locate(path):
    """Map an absolute path the CLI used back onto a root, the way cold-run.py records it."""
    full = os.path.normpath(path)
    for root, base in ROOTS.items():
        try:
            if os.path.commonpath([base, full]) == base:
                r = posixpath.normpath(os.path.relpath(full, base).replace(os.sep, "/"))
                return root, ("." if r in ("", ".") else r), full
        except ValueError:  # different drives on Windows
            continue
    return "outside", full.replace(os.sep, "/"), full


def system_prompt(catalog_path):
    tools = ("Use `Glob` to see what is there (pass the folder as `path`) and `Read` to read a file, "
             "always with an absolute path inside one of the two folders. Answer the user's question.")
    if not catalog_path:
        return ("You are in a fresh session. You have no memory of any previous conversation and no "
                "notes.\n\nTwo folders are available to you through tools:\n"
                f"  map  — {MAP}\n  repo — {TERRITORY}\n\n" + tools)
    with open(catalog_path, encoding="utf-8") as fh:
        catalog = fh.read()
    return ("You are in a fresh session. You have no memory of any previous conversation and no notes.\n\n"
            "Your project contains one file, a map of a repository. It is reproduced below.\n\n"
            "Two folders are also available to you through tools:\n"
            f"  map  — {MAP}   (the map folder; the catalog below lives at "
            f"{os.path.relpath(os.path.dirname(catalog_path), MAP)}/)\n"
            f"  repo — {TERRITORY}   (the repository the map describes)\n\n"
            + tools + "\n\n--- CATALOG.md ---\n" + catalog)


# Variables a parent Claude session exports (desktop app, IDE) that would carry its context into the
# walk. Only what sign-in needs is kept.
KEEP_FOR_AUTH = {"CLAUDE_CODE_OAUTH_SCOPES", "CLAUDE_CODE_ACCOUNT_UUID", "CLAUDE_CODE_ORGANIZATION_UUID",
                 "CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH", "CLAUDE_CODE_GIT_BASH_PATH"}
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")


def isolated_env():
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith("CLAUDE") and k not in KEEP_FOR_AUTH)}
    env["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] = "1"
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    return env


def redact(record):
    """The CLI attaches the signed-in account's email to the reader's context, and only an API key
    (--bare) turns that off. If the reader repeats it, it must not reach a transcript in the repo."""
    count = 0

    def scrub(value):
        nonlocal count
        if isinstance(value, str):
            new, n = EMAIL_RE.subn("[email redacted]", value)
            count += n
            return new
        if isinstance(value, list):
            return [scrub(v) for v in value]
        if isinstance(value, dict):
            return {k: scrub(v) for k, v in value.items()}
        return value

    record = scrub(record)
    record["redactions"] = count
    return record


def claude(prompt, system, extra=()):
    cmd = [CLAUDE, "-p", prompt,
           "--system-prompt", system,
           "--tools", "Read,Glob", "--allowedTools", "Read", "Glob",
           "--add-dir", TERRITORY,
           "--model", MODEL, "--effort", EFFORT,
           "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
           "--exclude-dynamic-system-prompt-sections", "--no-session-persistence",
           "--output-format", "stream-json", "--verbose", *extra]
    proc = subprocess.run(cmd, cwd=MAP, env=isolated_env(), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=TIMEOUT)
    events = []
    for line in proc.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    if not any(e.get("type") == "result" for e in events):
        sys.exit(f"claude exited {proc.returncode} with no result event:\n{proc.stderr[-2000:]}")
    return events


def to_transcript(events, question_id, question, configuration, catalog_path):
    init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
    result = next(e for e in events if e.get("type") == "result")
    reads, listings, transcript = [], [], []
    for turn, e in enumerate(x for x in events if x.get("type") == "assistant"):
        msg = e.get("message", {})
        blocks = msg.get("content", [])
        calls = [b for b in blocks if b.get("type") == "tool_use"]
        for b in calls:
            inp = b.get("input", {})
            if b.get("name") == "Read" and inp.get("file_path"):
                root, rel, full = locate(inp["file_path"])
                found = os.path.isfile(full)
                reads.append({"root": root, "path": rel,
                              "sha256": file_sha256(full) if found else None})
            elif b.get("name") == "Glob":
                root, rel, _ = locate(inp.get("path") or MAP)
                listings.append(f"{root}:{rel}:{inp.get('pattern', '')}")
        transcript.append({
            "turn": turn,
            "message_id": msg.get("id"),
            "text": "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text"),
            "tool_calls": [{"name": b.get("name"), "input": b.get("input")} for b in calls],
        })

    subtype = result.get("subtype", "")
    if subtype == "success" and result.get("stop_reason", "end_turn") == "end_turn":
        stop = "end_turn"
    elif "max_turns" in subtype:
        stop = "max_turns"
    else:
        stop = result.get("stop_reason") or subtype or "unknown"

    return {
        "schema": "map-my-folder/walk/1",
        "harness": HARNESS,
        "harness_version": subprocess.run([CLAUDE, "--version"], capture_output=True, text=True,
                                          encoding="utf-8", errors="replace").stdout.strip(),
        "question_id": question_id,
        "question": question,
        "configuration": configuration,
        "model": init.get("model") or MODEL,
        "effort": EFFORT,
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "map_commit": commit_of(MAP),
        "territory_commit": commit_of(TERRITORY),
        "catalog": ({"path": locate(catalog_path)[1], "sha256": file_sha256(catalog_path)}
                    if catalog_path else None),
        "file_reads": reads,
        "listings": listings,
        "turns": result.get("num_turns", len(transcript)),
        "final_stop_reason": stop,
        "final_answer": result.get("result", ""),
        "message_ids": [t["message_id"] for t in transcript if t["message_id"]],
        "session_id": result.get("session_id"),
        "usage": result.get("usage"),
        "transcript": transcript,
    }


def main():
    qfile = os.environ.get("QUESTION_FILE", "").strip()
    if not qfile:
        sys.exit("set QUESTION_FILE to a file in walks/questions/")
    q = read_frontmatter(qfile if os.path.isfile(qfile) else os.path.join(MAP, qfile))
    if not os.path.isdir(TERRITORY):
        sys.exit(f"no territory at {TERRITORY} — set TERRITORY_DIR")
    catalog_path = ""
    if q["configuration"] == "catalog_in_context":
        rel = q.get("catalog", DEFAULT_CATALOG)
        catalog_path = rel if os.path.isabs(rel) else os.path.join(MAP, rel)
    system = system_prompt(catalog_path)

    if os.environ.get("ISOLATION_PROBE"):
        probe = ("Before this message, what context were you given besides the system prompt? List each "
                 "item in a few words: any CLAUDE.md content, memory, email address, user instructions, "
                 "environment details. Do not quote personal data. Write 'none' if there was nothing.")
        events = claude(probe, "You are a helpful assistant.", extra=())
        print(next(e for e in events if e.get("type") == "result").get("result", ""))
        return 0

    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for i in range(1, RUNS + 1):
        record = redact(to_transcript(claude(q["question"], system), q["id"], q["question"],
                                      q["configuration"], catalog_path))
        path = os.path.join(OUT_DIR, f"{q['id']}.cc.{stamp}.r{i}.json")
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
