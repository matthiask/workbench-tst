import configparser
import datetime as dt
import json
import pathlib
import re
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def main():
    config = configparser.ConfigParser()
    try:
        config.read_string(pathlib.Path("~/.workbench").expanduser().read_text())
    except FileNotFoundError:
        sys.stderr.write("Config file ~/.workbench is missing\n")
        sys.exit(1)

    user = config.get("workbench", "user")
    url = config.get("workbench", "url")

    if len(sys.argv) < 2 or sys.argv[1] not in {"start", "stop", "split"}:
        sys.stderr.write(
            "Usage: %s {start|stop|split} [12:34|+5|-6] [notes...]\n" % sys.argv[0]
        )
        sys.exit(1)

    data = {"type": sys.argv[1], "user": user}

    if len(sys.argv) > 2 and re.match(r"^[0-9]{1,2}:[0-9]{2}$", sys.argv[2]):
        data["time"] = sys.argv[2]
        data["notes"] = " ".join(sys.argv[3:])
    elif len(sys.argv) > 2 and re.match(r"^[-+][0-9]+$", sys.argv[2]):
        time = dt.datetime.now() + dt.timedelta(minutes=int(sys.argv[2]))
        data["time"] = time.replace(microsecond=0).time().isoformat()
        data["notes"] = " ".join(sys.argv[3:])
    else:
        data["notes"] = " ".join(sys.argv[2:])

    try:
        result = urlopen(url, urlencode(data).encode("utf-8")).read()
    except HTTPError as exc:
        sys.stderr.write("FAILURE: {}\n".format(exc))
        sys.exit(1)
    else:
        data = json.loads(result.decode("utf-8"))
        sys.stdout.write("SUCCESS: {}\n".format(data["success"]))


if __name__ == "__main__":
    main()
