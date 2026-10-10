
# ============================================
# HORIZON FONT GENERATOR v1.0.0
# Python 3 | Pydroid 3
# ASCII Terminal Interface
# ============================================

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

APP_NAME = "HORIZON FONT GENERATOR"
VERSION = "1.0.0"

HOME = Path.home()
DATA_DIR = HOME / ".horizon_font_generator"
OUTPUT_DIR = HOME / "HorizonFontGenerator"
HISTORY_FILE = DATA_DIR / "history.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Unicode mathematical alphabets
RANGES = {
    "Bold": (0x1D400, 0x1D41A, 0x1D7CE),
    "Italic": (0x1D434, 0x1D44E, None),
    "Bold Italic": (0x1D468, 0x1D482, None),
    "Script / Fancy": (0x1D49C, 0x1D4B6, None),
    "Gothic": (0x1D504, 0x1D51E, None),
    "Double-struck": (0x1D538, 0x1D552, 0x1D7D8),
    "Monospace": (0x1D670, 0x1D68A, 0x1D7F6),
}

SPECIAL = {
    "Italic": {"h": "ℎ"},
    "Script / Fancy": {
        "B": "ℬ", "E": "ℰ", "F": "ℱ",
        "H": "ℋ", "I": "ℐ", "L": "ℒ",
        "M": "ℳ", "R": "ℛ", "e": "ℯ",
        "g": "ℊ", "o": "ℴ"
    },
    "Gothic": {
        "C": "ℭ", "H": "ℌ", "I": "ℑ",
        "R": "ℜ", "Z": "ℨ"
    },
    "Double-struck": {
        "C": "ℂ", "H": "ℍ", "N": "ℕ",
        "P": "ℙ", "Q": "ℚ", "R": "ℝ",
        "Z": "ℤ"
    },
}

SMALL_CAPS = str.maketrans({
    "a":"ᴀ", "b":"ʙ", "c":"ᴄ", "d":"ᴅ",
    "e":"ᴇ", "f":"ꜰ", "g":"ɢ", "h":"ʜ",
    "i":"ɪ", "j":"ᴊ", "k":"ᴋ", "l":"ʟ",
    "m":"ᴍ", "n":"ɴ", "o":"ᴏ", "p":"ᴘ",
    "q":"ǫ", "r":"ʀ", "s":"s", "t":"ᴛ",
    "u":"ᴜ", "v":"ᴠ", "w":"ᴡ", "x":"x",
    "y":"ʏ", "z":"ᴢ"
})

BUBBLE = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"
    "⓪①②③④⑤⑥⑦⑧⑨"
)

SQUARE = dict(zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
))

UPSIDE_DOWN = str.maketrans({
    "a":"ɐ", "b":"q", "c":"ɔ", "d":"p",
    "e":"ǝ", "f":"ɟ", "g":"ƃ", "h":"ɥ",
    "i":"ᴉ", "j":"ɾ", "k":"ʞ", "l":"l",
    "m":"ɯ", "n":"u", "o":"o", "p":"d",
    "q":"b", "r":"ɹ", "s":"s", "t":"ʇ",
    "u":"n", "v":"ʌ", "w":"ʍ", "x":"x",
    "y":"ʎ", "z":"z",
    "A":"∀", "B":"𐐒", "C":"Ɔ", "D":"◖",
    "E":"Ǝ", "F":"Ⅎ", "G":"פ", "H":"H",
    "I":"I", "J":"ſ", "K":"⋊", "L":"˥",
    "M":"W", "N":"N", "O":"O", "P":"Ԁ",
    "Q":"Ό", "R":"ᴚ", "S":"S", "T":"┴",
    "U":"Ո", "V":"Λ", "W":"M", "X":"X",
    "Y":"⅄", "Z":"Z",
    "0":"0", "1":"Ɩ", "2":"ᄅ", "3":"Ɛ",
    "4":"ㄣ", "5":"ϛ", "6":"9", "7":"ㄥ",
    "8":"8", "9":"6",
    ".":"˙", ",":"'", "?":"¿", "!":"¡",
    "(" : ")", ")" : "(", "[" : "]",
    "]" : "[", "{" : "}", "}" : "{"
})

STYLES = [
    "Bold",
    "Italic",
    "Cursive",
    "Small caps",
    "Bold Italic",
    "Script / Fancy",
    "Gothic",
    "Double-struck",
    "Monospace",
    "Bubble text",
    "Square text",
    "Upside-down text"
]


def banner():
    print(r"""
 _   _  ___  ____  ___ ______  ___  _   _
| | | |/ _ \|  _ \|_ _|__  /  / _ \| \ | |
| |_| | | | | |_) || |  / /  | | | |  \| |
|  _  | |_| |  _ < | | / /_  | |_| | |\  |
|_| |_|\___/|_| \_\___/____|  \___/|_| \_|

          HORIZON FONT GENERATOR
""")
    print(" Version:", VERSION)
    print(" Unicode Text Styling Toolkit")
    print("=" * 45)


def convert_math(text, style):
    upper, lower, digits = RANGES[style]
    special = SPECIAL.get(style, {})
    output = []

    for char in text:
        if char in special:
            output.append(special[char])

        elif "A" <= char <= "Z":
            output.append(
                chr(upper + ord(char) - ord("A"))
            )

        elif "a" <= char <= "z":
            output.append(
                chr(lower + ord(char) - ord("a"))
            )

        elif char.isdigit() and digits is not None:
            output.append(
                chr(digits + int(char))
            )

        else:
            output.append(char)

    return "".join(output)


def convert(text, style):
    if style in RANGES:
        return convert_math(text, style)

    if style == "Cursive":
        return convert_math(text, "Script / Fancy")

    if style == "Small caps":
        return text.translate(SMALL_CAPS)

    if style == "Bubble text":
        return text.translate(BUBBLE)

    if style == "Square text":
        return "".join(
            SQUARE.get(char.upper(), char)
            if char.isalpha() else char
            for char in text
        )

    if style == "Upside-down text":
        return text.translate(UPSIDE_DOWN)[::-1]

    return text


def get_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return []


def add_history(original, style, result):
    history = get_history()

    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "style": style,
        "original": original,
        "result": result
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history[-100:],
            file,
            ensure_ascii=False,
            indent=2
        )


def copy_text(text):
    # Optional clipboard support.
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        pass

    # Optional Termux clipboard support.
    try:
        result = subprocess.run(
            ["termux-clipboard-set"],
            input=text,
            text=True,
            capture_output=True,
            timeout=3
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass

    return False


def save_result(text, name):
    safe_name = "".join(
        char if char.isalnum() or char in "_-"
        else "_"
        for char in name
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"{safe_name}_{timestamp}.txt"

    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

    return path


def actions(result, style):
    while True:
        print("\n[C] Copy text")
        print("[S] Save to text file")
        print("[B] Back")

        choice = input("> ").strip().lower()

        if choice == "c":
            if copy_text(result):
                print("Copied!")
            else:
                print("\nClipboard unavailable.")
                print("Long-press and copy the output below:\n")
                print(result)

        elif choice == "s":
            try:
                path = save_result(result, style)
                print("Saved to:", path)
            except OSError as error:
                print("Save failed:", error)

        elif choice == "b":
            break

        else:
            print("Invalid choice.")


def convert_one():
    original = input("\nEnter your text: ")

    if not original:
        print("You entered no text.")
        return

    if len(original) > 5000:
        print("Maximum length is 5000 characters.")
        return

    print("\nChoose your font:\n")

    for number, style in enumerate(STYLES, 1):
        print(f"{number:2}. {style}")

    choice = input("\nFont number: ").strip()

    if not choice.isdigit():
        print("Enter a valid number.")
        return

    number = int(choice)

    if not 1 <= number <= len(STYLES):
        print("Invalid font number.")
        return

    style = STYLES[number - 1]
    result = convert(original, style)

    print("\n" + "=" * 45)
    print("FONT:", style)
    print("-" * 45)
    print("ORIGINAL:")
    print(original)
    print("\nPREVIEW:")
    print(result)
    print("=" * 45)

    add_history(original, style, result)
    actions(result, style)


def generate_all():
    original = input("\nEnter your text: ")

    if not original:
        print("You entered no text.")
        return

    if len(original) > 5000:
        print("Maximum length is 5000 characters.")
        return

    results = []

    print("\n========== ALL FONT STYLES ==========")

    for number, style in enumerate(STYLES, 1):
        result = convert(original, style)
        results.append((style, result))

        print(f"\n[{number}] {style}")
        print(result)

        add_history(original, style, result)

    print("\n[A] Save all styles")
    print("[C] Copy one style")
    print("[B] Back")

    choice = input("> ").strip().lower()

    if choice == "a":
        combined = "\n\n".join(
            f"=== {style} ===\n{result}"
            for style, result in results
        )

        try:
            print("Saved:", save_result(combined, "All_Styles"))
        except OSError as error:
            print("Save failed:", error)

    elif choice == "c":
        number = input("Enter style number: ").strip()

        if number.isdigit() and 1 <= int(number) <= len(results):
            style, result = results[int(number) - 1]
            actions(result, style)
        else:
            print("Invalid style number.")


def show_history():
    history = get_history()

    if not history:
        print("\nNo history available.")
        return

    print("\n====== RECENT CONVERSIONS ======")

    for entry in history[-15:][::-1]:
        print("\nTime:", entry.get("time", "?"))
        print("Style:", entry.get("style", "?"))
        print("Input:", entry.get("original", "")[:100])
        print("Output:", entry.get("result", "")[:100])

    print("\n[D] Delete history")
    print("[B] Back")

    choice = input("> ").strip().lower()

    if choice == "d":
        confirm = input("Type YES to delete history: ")

        if confirm == "YES":
            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump([], file)
            print("History cleared.")
        else:
            print("Cancelled.")


def help_screen():
    print("""
HORIZON FONT GENERATOR HELP

1. Enter ordinary text.
2. Select a font style.
3. Preview the converted text.
4. Copy it or save it.

FEATURES
- 12 Unicode text styles
- Generate all styles at once
- Preview before copying
- Optional clipboard integration
- Save results as .txt
- Last 100 conversions stored in history
- Offline operation
- No third-party package required

IMPORTANT
These are Unicode text styles, NOT actual TTF/OTF font files.
Appearance and compatibility depend on the app and device.

OUTPUT DIRECTORY:
~/HorizonFontGenerator

HISTORY FILE:
~/.horizon_font_generator/history.json
""")


def main():
    while True:
        banner()

        print("\n[1] Convert one style")
        print("[2] Generate all styles")
        print("[3] Conversion history")
        print("[4] Help")
        print("[5] Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == "1":
                convert_one()

            elif choice == "2":
                generate_all()

            elif choice == "3":
                show_history()

            elif choice == "4":
                help_screen()

            elif choice == "5":
                print("\nThanks for using Horizon Font Generator!")
                break

            else:
                print("Invalid option.")

        except (OSError, ValueError) as error:
            print("Error:", error)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExited safely.")
