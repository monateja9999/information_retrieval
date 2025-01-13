#!/usr/bin/env python
import sys
import re
from collections import defaultdict

# Set of target bigrams to filter
target_bigrams = {
    "computer science",
    "information retrieval",
    "power politics",
    "los angeles",
    "bruce willis"
}

# Initialize a default dictionary to hold bigram counts
bigram_count = defaultdict(lambda: defaultdict(int))

# Read from standard input
for line in sys.stdin:
    line = line.strip()
    if line:
        # Split the line into docID and content
        parts = line.split('\t', 1)
        if len(parts) < 2:
            continue  # Skip lines that don't match the expected format
        
        doc_id, content = parts
        # Normalize the content: remove punctuation and convert to lowercase
        content = re.sub(r'[^a-zA-Z\s]', ' ', content)  # Only allow letters and spaces
        content = content.lower()
        words = content.split()
        
        # Create bigrams and filter for target bigrams
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i + 1]}"
            if bigram in target_bigrams:  # Only emit target bigrams
                print(f"{bigram}\t{doc_id}")
