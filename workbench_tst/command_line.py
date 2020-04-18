import configparser
import datetime as dt
import json
import pathlib
import re
import sys
from collections import deque
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def fetch_json(url, data=None):
    try:
        result = urlopen(url, data).read()
    except HTTPError as exc:
        sys.stderr.write(red("FAILURE: {}\n".format(exc)))
        sys.exit(1)
    else:
        return json.loads(result.decode("utf-8"))


def underline(s):
    return "\033[4m{}\033[0m".format(s)


def red(s):
    return "\033[31m{}\033[0m".format(s)


def green(s):
    return "\033[32m{}\033[0m".format(s)


def format_timestamp_row(row):
    return "{} {}".format(
        row["timestamp"], underline(row["comment"]) if row["comment"] else "",
    )


def main():
    config = configparser.ConfigParser()
    try:
        config.read_string(pathlib.Path("~/.workbench").expanduser().read_text())
    except FileNotFoundError:
        sys.stderr.write(red("Config file ~/.workbench is missing\n"))
        sys.exit(1)

    user = config.get("workbench", "user")
    url = config.get("workbench", "url")

    if len(sys.argv) < 2 or sys.argv[1] == "help":
        sys.stderr.write(
            """\
Workbench timestamps command-line interface

Splitting right now:

    tst split              # Bare split
    tst one two three      # Including notes

Splitting some other time:

    tst -5                 # 5 Minutes ago
    tst 13:30              # At 13:30 exactly
    tst -10 one two three  # Splitting 10 minutes ago with notes
    tst +15                # Split in 15 minutes

Submitting other types:

    tst stop
    tst start
    tst start -5           # I started 5 minutes ago

Show today's timestamps:

    tst list

Show help:

    tst
    tst help
"""
        )
        sys.exit(1)

    if sys.argv[1] == "list":
        url = url.replace("create-timestamp", "list-timestamps")
        data = fetch_json(url + "?user={}".format(user), None)
        sys.stdout.write(green("Timestamps\n"))
        sys.stdout.write(
            "\n".join(format_timestamp_row(row) for row in data["timestamps"])
        )
        sys.stdout.write("\n{}\n".format(green("Logged: {}h".format(data["hours"]))))
        return

    args = deque(sys.argv[1:])
    data = {
        "type": args.popleft() if args[0] in {"start", "stop", "split"} else "split",
        "user": user,
    }
    if args and re.match(r"^[0-9]{1,2}:[0-9]{2}$", args[0]):
        data["time"] = args.popleft()
    elif args and re.match(r"^[-+][0-9]+$", args[0]):
        time = dt.datetime.now() + dt.timedelta(minutes=int(args.popleft()))
        data["time"] = time.replace(microsecond=0).time().isoformat()
    data["notes"] = " ".join(args)

    data = fetch_json(url, urlencode(data).encode("utf-8"))
    sys.stdout.write(green("SUCCESS: {}\n".format(data["success"])))


if __name__ == "__main__":
    main()
