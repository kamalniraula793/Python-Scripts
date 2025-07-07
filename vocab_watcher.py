import subprocess
import time
import pyperclip
import os
import requests
import string

REPO_PATH = "/home/kali/Scripts"
FILENAME = "vocab.txt"
FULL_PATH = os.path.join(REPO_PATH, FILENAME)
last_clipboard = ""

def clean_word(word):
    return word.strip(string.whitespace + string.punctuation)

def is_okular_running():
    try:
        subprocess.check_output(["pgrep", "-f", "okular"])
        return True
    except subprocess.CalledProcessError:
        return False

def get_main_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            for meaning in data["meanings"]:
                part_of_speech = meaning.get("partOfSpeech", "unknown")
                definitions = meaning.get("definitions", [])
                if definitions:
                    definition = definitions[0].get("definition", "No definition available")
                    examples = [d.get("example") for d in definitions if d.get("example")]
                    synonyms = set()
                    for d in definitions:
                        for syn in d.get("synonyms", []):
                            synonyms.add(syn)
                    return {
                        "partOfSpeech": part_of_speech,
                        "definition": definition,
                        "examples": examples,
                        "synonyms": sorted(synonyms)
                    }
        return None
    except:
        return None

def format_entry(word, data):
    lines = []
    lines.append(f"📖 Word: {word}")
    lines.append(f"🔤 Part of Speech: {data['partOfSpeech']}")
    lines.append(f"📝 Definition: {data['definition']}\n")

    for i, ex in enumerate(data['examples'], start=1):
        lines.append(f"📌 Example {i}: {ex}")

    if data["synonyms"]:
        lines.append(f"\n🔁 Synonyms: {', '.join(data['synonyms'])}")

    lines.append("─" * 44)
    return "\n".join(lines) + "\n\n"

def append_to_file(formatted_text):
    with open(FULL_PATH, "a", encoding="utf-8") as f:
        f.write(formatted_text)

def git_commit_and_push():
    subprocess.run(["git", "pull", "--rebase"], cwd=REPO_PATH)
    subprocess.run(["git", "add", FILENAME], cwd=REPO_PATH)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_PATH)
    if result.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Added new word meaning"], cwd=REPO_PATH)
        subprocess.run(["git", "push"], cwd=REPO_PATH)

print("📚 Vocabulary watcher started... (Watching Okular + clipboard)")

while True:
    if is_okular_running():
        raw_word = pyperclip.paste()
        word = clean_word(raw_word)
        if word and word != last_clipboard and word.isalpha():
            last_clipboard = word
            print(f"🔍 Looking up: {word}")
            result = get_main_meaning(word)
            if result:
                formatted = format_entry(word, result)
                print(f"✅ Found:\n{formatted}")
                append_to_file(formatted)
                git_commit_and_push()
            else:
                print(f"❌ No meaning found for: {word}")
    time.sleep(3)

