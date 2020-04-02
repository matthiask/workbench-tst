import configparser
import re
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def main():
    config = configparser.ConfigParser()
    config.read("~/.workbench")

    if len(sys.argv) < 2:
        sys.stderr.write(
            "Usage: %s {start|stop|split} [12:34] [notes...]\n" % sys.argv[0]
        )
        sys.exit(1)

    data = {"type": sys.argv[1], "user": config["workbench.user"]}

    if len(sys.argv) > 2 and re.match(r"[0-9]{1,2}:[0-9]{2}", sys.argv[2]):
        data["time"] = sys.argv[2]
        data["notes"] = " ".join(sys.argv[3:])
    else:
        data["notes"] = " ".join(sys.argv[2:])

    try:
        urlopen(config["workbench.url"], urlencode(data).encode("utf-8"))
    except HTTPError:
        sys.stderr.write("FAILURE\n")
        sys.exit(1)
    else:
        sys.stdout.write("SUCCESS\n")
