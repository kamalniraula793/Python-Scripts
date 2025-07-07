import subprocess
import time
import pyperclip
import os
import requests

REPO_PATH = "/home/kali/Scripts"
FILENAME = "vocab.txt"
FULL_PATH = os.path.join(REPO_PATH, FILENAME)
last_clipboard = ""

def is_okular_running():
    try:
        subprocess.check_output(["pgrep", "-f", "okular"])
        return True
    except subprocess.CalledProcessError:
        return False

def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data[0]['meanings'][0]['definitions'][0]['definition']
        else:
            return None
    except:
        return None

def append_to_file(word, meaning):
    with open(FULL_PATH, "a", encoding="utf-8") as f:
        f.write(f"{word} : {meaning}\n")

def git_commit_and_push():
    subprocess.run(["git", "add", FILENAME], cwd=REPO_PATH)
    subprocess.run(["git", "commit", "-m", "Added new word meaning"], cwd=REPO_PATH)
    subprocess.run(["git", "push"], cwd=REPO_PATH)

print("📚 Vocabulary watcher started... (Watching Okular + clipboard)")

while True:
    if is_okular_running():
        word = pyperclip.paste().strip()
        if word and word != last_clipboard and word.isalpha():
            last_clipboard = word
            print(f"🔍 Looking up: {word}")
            meaning = get_meaning(word)
            if meaning:
                print(f"✅ Found: {word} : {meaning}")
                append_to_file(word, meaning)
                git_commit_and_push()
            else:
                print(f"❌ No meaning found for: {word}")
    time.sleep(3)

