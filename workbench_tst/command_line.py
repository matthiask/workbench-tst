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


def ansi(code):
    return lambda s: "\033[{}m{}\033[0m".format(code, s)


underline = ansi("4")
red = ansi("31")
green = ansi("32")


def show_help():
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


def list_timestamps(*, url, user):
    url = url.replace("create-timestamp", "list-timestamps")
    data = fetch_json(url + "?user={}".format(user), None)
    sys.stdout.write(green("Timestamps\n"))
    sys.stdout.write(
        "\n".join(
            "{} {}".format(
                row["timestamp"],
                underline(row["comment"]) if row["comment"] else "",
            )
            for row in data["timestamps"]
        )
    )
    sys.stdout.write("\n{}\n".format(green("Logged: {}h".format(data["hours"]))))


def create_timestamp(*, url, user, projects):
    args = deque(sys.argv[1:])
    data = {
        "type": args.popleft() if args[0] in {"start", "stop", "split"} else "split",
        "user": user,
    }
    while True:
        if not args:
            break
        if re.match(r"^[0-9]{1,2}:[0-9]{2}$", args[0]):
            data["time"] = args.popleft()
        elif re.match(r"^[-+][0-9]+$", args[0]):
            time = dt.datetime.now() + dt.timedelta(minutes=int(args.popleft()))
            data["time"] = time.replace(microsecond=0).time().isoformat()
        elif args[0] in projects:
            data["project"] = projects[args.popleft()]
        else:
            break

    data["notes"] = " ".join(args)

    data = fetch_json(url, urlencode(data).encode("utf-8"))
    sys.stdout.write(green(data["success"]))
    sys.stdout.write("\n")


def main():
    config = configparser.ConfigParser()
    try:
        config.read_string(pathlib.Path("~/.workbench").expanduser().read_text())
    except FileNotFoundError:
        sys.stderr.write(red("Config file ~/.workbench is missing\n"))
        sys.exit(1)

    user = config.get("workbench", "user")
    url = config.get("workbench", "url")

    try:
        projects = dict(config.items("projects"))
    except configparser.NoSectionError:
        projects = {}

    if len(sys.argv) < 2 or sys.argv[1] == "help":
        show_help()
    elif sys.argv[1] == "list":
        list_timestamps(url=url, user=user)
    else:
        create_timestamp(url=url, user=user, projects=projects)


if __name__ == "__main__":
    main()
