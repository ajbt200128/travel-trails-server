#!/usr/bin/env python
import datetime
import subprocess

if __name__ == "__main__":
    now = datetime.datetime.now()
    print("==========[{}]==========".format(str(now)))

    out = subprocess.run(["echo", "hello world"], capture_output=True)
    print(out.returncode)
    print(out.stdout.decode("utf-8"))
