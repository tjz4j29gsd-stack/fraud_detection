# Fraud Detection Pipeline

This repository contains a highly performant, rule-based transaction monitoring subsystem written in Python. It processes 1 million transactions in roughly ~2.5 seconds on a standard laptop.

## Requirements
- Python 3.8+
- pandas

Install dependencies:
```bash
pip install pandas
```

## Running the Pipeline

**1. Data Setup:**
Because the dataset is highly confidential and extremely large (1M rows), `transactions.csv` is explicitly excluded from version control via `.gitignore`. 
Before running the pipeline, you **must** download `transactions.csv` and place it in the root directory of this repository.

**2. Execution:**
Run the main pipeline script:
```bash
python3 main.py
```
*(You can also specify custom input/output paths using `python3 main.py --input path/to/data.csv --output results.jsonl`)*

### Expected Output
- The script will print the evaluation steps and the total number of flagged transactions.
- A new file named `flagged_transactions.jsonl` will be created in the directory.
- Execution time should be roughly 3.5 seconds.

## Files
- `main.py`: The core E2E pipeline script.
- `Rules_and_Pipeline.md`: The required documentation explaining the 5 proposed rules, the 3 implemented rules, and the reasoning behind prioritizing them.
- `flagged_transactions.jsonl`: The output file containing the flagged transactions and their human-readable reasons.
- `experimentation.ipynb`: A Jupyter Notebook used during the EDA phase to rapidly test hypothesis and tune rule thresholds against the budget without paying the data-loading cost every time.
- `eda_results.md`: A summary of the initial exploratory data analysis findings.
