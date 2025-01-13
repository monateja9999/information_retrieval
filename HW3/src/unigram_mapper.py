import sys
import re

# Reading input line by line
for line in sys.stdin:
    # Split the line into docID and content
    parts = line.strip().split("\t", 1)
    if len(parts) < 2:
        continue  # skip lines that don't follow the expected format

    doc_id = parts[0]
    content = parts[1]

    # Clean the text: replace non-alphabetic characters with space and lowercase all words
    cleaned_content = re.sub(r'[^a-zA-Z]+', ' ', content).lower()
    words = cleaned_content.split()

    # Emit each unigram with the doc_id
    for word in words:
        if word:  # skip empty words
            print(f"{word}\t{doc_id}")
