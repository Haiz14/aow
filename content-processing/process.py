#!/usr/bin/python3

"""
Processes an original txt document to json.

This script reads a text file named 'orig.txt', parses its content based on
pre-defined chapter and content patterns, and writes the structured data
into a JSON file named 'output.json'.

Input File Pattern ('./orig.txt'):
- Chapters are denoted by a Roman numeral (I to XIII) followed by a name.
  Example: I. Chapter One
- Each chapter contains numbered line with a pragraph or two of text followed by next number
  Example:   1. This is a line of text.
  Lime 2 of line 1
  2. New line
- The content ends with "THE END", followed by a separator line of hyphens,
  and then copyright information.
"""

import json
import re


def process_document(input_path: str, output_path: str):
    """
    Reads, parses, and converts the text document to JSON.

    Args:
        input_path (str): The path to the source text file.
        output_path (str): The path for the destination JSON file.
    """
    # (File reading logic remains the same)
    import re

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
            # Search for the <pre> tag content
            pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', html_content, re.DOTALL)
            
            if not pre_match:
                raise ValueError(f"No <pre> tag found in the file: '{input_path}'")
            
            full_text = pre_match.group(1).strip()
            
            if not full_text:
                raise ValueError(f"Empty <pre> tag in the file: '{input_path}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
        quit()
    except ValueError as e:
        print(f"Error: {e}")
        quit()

    # --- Parsing Logic ---

    # 1. Split the document into the main content and the footer at "THE END"
    main_content, _, footer = map(str.strip, full_text.partition('THE END'))

    # 2. Extract copyright info from the footer
    copyright_info = footer.split('---', 1)[-1].strip()

    # 3. Define Regex to find chapters and their content
    chapter_regex = re.compile(
        # Capture group 1: Roman Numeral (I-XIII)
        r'^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII)\.\s+'
        # Capture group 2: Chapter Name
        r'(.*?)\n'
        # Capture group 3: All content until the next chapter or end of string
        r'((?:.|\n)*?)(?='
        # Positive lookahead to find the start of the next chapter or end of string
        r'^(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII)\.|\Z)',
        re.MULTILINE
    )

    # 4. Find all chapters
    chapters = []
    for match in chapter_regex.finditer(main_content):
        roman_numeral, title, content_block = match.groups()

        # Extract numbered lines from the chapter's content block
        lines = re.findall(
            # This updated regex allows capture group 3 to grab everything
            # until the next numbered line, the next chapter, or the end.
            r'^\s*\d+\.\s+(.*?)(?=\n\s*\d+\.|\n\s*I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII\.\s|\Z)',
            content_block, re.MULTILINE | re.DOTALL
        )

        chapters.append({
            "chapter_number": roman_numeral,
            "chapter_title": title.strip(),
            "content": [line.strip() for line in lines]
        })

    # 5. Assemble the final data structure
    processed_data = {
        "meta": {
          "name": "Art of War",
          "by": "Sun Tzu",
          "translated-by": "Lionel Giles"
        },
        "chapters": chapters,
        "copyright": copyright_info
    }

    # 6. Write the data to a JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Success! Document processed and saved to '{output_path}'")
    except Exception as e:
        print(f"An error occurred while writing the JSON file: {e}")


def create_dummy_file(path: str):
    """Creates a sample 'orig.txt' file for demonstration."""
    dummy_content = """
I. The Journey Begins
  1. The old map was discovered in a dusty attic.
  2. A secret was hidden within its faded lines.

II. Into the Woods
  1. The path was overgrown and treacherous.

XIII. The Treasure
  1. After a long search, the chest was unearthed.
  2. It was filled not with gold, but with ancient books.

THE END
-----------------------
Copyright 2025, The Adventure Company. All Rights Reserved.
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dummy_content.strip())


if __name__ == "__main__":
    # Define the input and output file paths
    input_file = "orig.html"
    output_file = "aow.json"
    process_document(input_file, output_file)
