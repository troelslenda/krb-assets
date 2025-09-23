import os
import urllib.parse

README_PATH = "README.md"
SPOT_ILLUSTRATIONS_DIR = "spot-illustrations"
START_TAG = "<!--- SPOT ILLUSTRATIONS START -->"
END_TAG = "<!--- SPOT ILLUSTRATIONS END -->"


def get_svg_files(directory):
    files = []
    for f in os.listdir(directory):
        if f.lower().endswith(".svg") and not f.lower().endswith(".backup"):
            files.append(f)
    return sorted(files)


def generate_markdown_table(files):
    header = "| Name | Preview |\n| --- | --- |"
    rows = []
    for file in files:
        url_file = urllib.parse.quote(file)
        link = f"[{file}]({SPOT_ILLUSTRATIONS_DIR}/{url_file})"
        img = f'![{url_file}]({SPOT_ILLUSTRATIONS_DIR}/{url_file})'
        rows.append(f"| {link} | {img} |")
    return f"{header}\n" + "\n".join(rows)


def update_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(START_TAG)
    end_idx = content.find(END_TAG)
    if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
        raise ValueError("Spot illustration tags not found or malformed in README.md")

    svg_files = get_svg_files(SPOT_ILLUSTRATIONS_DIR)
    md_table = generate_markdown_table(svg_files)

    before = content[:start_idx + len(START_TAG)]
    after = content[end_idx:]
    new_content = f"{before}\n\n{md_table}\n\n{after}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()
