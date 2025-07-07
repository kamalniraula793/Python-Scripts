#!/usr/bin/env python3
import subprocess
import time
import sys

def main():
    # Run your helper scripts in background
    subprocess.Popen(["bash", "/home/kali/Scripts/keep_artha_on_top.sh"])
    subprocess.Popen(["python3", "/home/kali/Scripts/vocab_watcher.py"])

    # Start Okular with any passed arguments (like file paths)
    args = ["okular"] + sys.argv[1:]
    subprocess.run(args)

if __name__ == "__main__":
    main()

