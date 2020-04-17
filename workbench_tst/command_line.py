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
        result = urlopen(url, urlencode(data or ()).encode("utf-8")).read()
    except HTTPError as exc:
        sys.stderr.write("FAILURE: {}\n".format(exc))
        sys.exit(1)
    else:
        return json.loads(result.decode("utf-8"))


def main():
    config = configparser.ConfigParser()
    try:
        config.read_string(pathlib.Path("~/.workbench").expanduser().read_text())
    except FileNotFoundError:
        sys.stderr.write("Config file ~/.workbench is missing\n")
        sys.exit(1)

    user = config.get("workbench", "user")
    url = config.get("workbench", "url")

    if len(sys.argv) < 2:
        sys.stderr.write(
            "Usage: %s [{start|stop|split}] [12:34|+5|-6] [notes...]\n" % sys.argv[0]
        )
        sys.exit(1)

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

    data = fetch_json(url, data)
    sys.stdout.write("SUCCESS: {}\n".format(data["success"]))


if __name__ == "__main__":
    main()
