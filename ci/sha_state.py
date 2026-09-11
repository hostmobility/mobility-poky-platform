import argparse
import json
import os
import sys
from pathlib import Path


STATE_DIR = Path.home() / "mobility-ci-state"
STATE_FILE = STATE_DIR / "sha-state.json"


def load_state():
    if not STATE_FILE.exists():
        return {}

    with STATE_FILE.open("r") as f:
        return json.load(f)


def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    temporary_file = STATE_FILE.with_suffix(".tmp")

    with temporary_file.open("w") as f:
        json.dump(state, f, indent=2, sort_keys=True)

    temporary_file.replace(STATE_FILE)


def get_status(sha):
    state = load_state()
    entry = state.get(sha)

    if entry is None:
        print("missing")
        return

    print(entry["status"])


def set_status(sha, status, pr=None, build_number=None):
    state = load_state()

    entry = state.get(sha, {})

    entry["status"] = status

    if pr is not None:
        entry["pr"] = int(pr)

    if build_number is not None:
        entry["build_number"] = int(build_number)

    state[sha] = entry

    save_state(state)

    print(f"{sha}: {status}")


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("--sha", required=True)

    set_parser = subparsers.add_parser("set")
    set_parser.add_argument("--sha", required=True)
    set_parser.add_argument(
        "--status",
        required=True,
        choices=["running", "success", "failed"]
    )
    set_parser.add_argument("--pr")
    set_parser.add_argument("--build-number")

    args = parser.parse_args()

    if args.command == "get":
        get_status(args.sha)

    elif args.command == "set":
        set_status(
            sha=args.sha,
            status=args.status,
            pr=args.pr,
            build_number=args.build_number,
        )


if __name__ == "__main__":
    main()