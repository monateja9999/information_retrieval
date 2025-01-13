#!/usr/bin/env python
import sys
from collections import defaultdict

# Set of target bigrams in the desired output order
target_bigrams_ordered = [
    "computer science",
    "information retrieval",
    "power politics",
    "los angeles",
    "bruce willis"
]

# Dictionary to hold the final counts for both unigrams and bigrams
final_counts = defaultdict(lambda: defaultdict(int))

# Read from standard input
for line in sys.stdin:
    line = line.strip()
    if line:
        term, doc_id = line.split('\t')
        # Increment the count for each term-doc_id pair
        final_counts[term][doc_id] += 1

# Output each target bigram in the specified order
for bigram in target_bigrams_ordered:
    if bigram in final_counts:
        doc_counts = final_counts[bigram]
        doc_counts_output = '\t'.join([f"{doc_id}:{count}" for doc_id, count in doc_counts.items()])
        print(f"{bigram}\t{doc_counts_output}")

# Output any unigrams in the remaining part of final_counts
for term, doc_counts in final_counts.items():
    # Only output terms not in the target bigram list to avoid duplicates
    if term not in target_bigrams_ordered:
        doc_counts_output = '\t'.join([f"{doc_id}:{count}" for doc_id, count in doc_counts.items()])
        print(f"{term}\t{doc_counts_output}")
