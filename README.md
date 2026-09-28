# Assignment 3: Algorithm Efficiency and Scalability

## Overview

This repository contains implementations and analysis of:

* Randomized Quicksort
* Deterministic Quicksort using the first element as pivot
* Hash Table with Separate Chaining

The assignment examines algorithm complexity, runtime behavior across different input distributions, and the effect of the load factor on hash table performance.

## Repository Structure

```text
assignment3/
├── assignment3.py
├── benchmark.py
├── benchmark_results.csv
├── report.md
└── README.md
```

## Requirements

* Python 3.10 or newer
* No third-party packages required

## How to Run

### 1. Run the implementation tests

```bash
python assignment3.py
```

Expected output:

```text
All tests passed.
```

### 2. Run the benchmarks

```bash
python benchmark.py
```

The script compares both Quicksort implementations on random, sorted, reverse-sorted, and repeated-value arrays.

The results are saved to `benchmark_results.csv`.

### 3. Use the hash table

```python
from assignment3 import ChainedHashTable

table = ChainedHashTable()

table.insert("apple", 10)
table.insert("banana", 20)

print(table.search("apple"))  # 10

table.delete("apple")
print(table.search("apple"))  # None
```

## Main Findings

* Randomized Quicksort has expected O(n log n) time complexity.
* First-element-pivot Quicksort can take O(n²) time on sorted and reverse-sorted arrays.
* Both two-way Quicksort implementations can degrade to O(n²) on arrays containing identical values.
* Hash table operations have expected O(1 + α) time under simple uniform hashing.
* Dynamic resizing helps maintain a bounded load factor and efficient average performance.

## Files

* `assignment3.py`: Algorithm implementations and tests.
* `benchmark.py`: Runtime comparison script.
* `benchmark_results.csv`: Generated benchmark measurements.
* `report.md`: Theoretical analysis and discussion.
