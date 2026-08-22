# Fraud Detection Pipeline

This repository contains a highly performant, rule-based transaction monitoring subsystem written in Python. It easily processes the dataset within the required time constraints.

## Requirements
- Python 3.8+
- pandas

Install dependencies:
```bash
pip install pandas
```

## Running the Pipeline

**1. Data Setup:**
Because the dataset is highly confidential and extremely large, both data files were explicitly excluded from version control via `.gitignore`. 
Before running the pipeline, you **must** download the `transactions.csv` file provided in the challenge prompt and place it in the root directory of this repository. 
*(Note: `main.py` does not require the `confirmed_fraud.csv` file to run the rule evaluation, but it is necessary if you wish to manually verify the ~80% recall metrics cited in `Rules_and_Pipeline.md`)*.

**2. Execution:**
Run the main pipeline script:
```bash
python3 main.py
```
*(You can also specify custom input/output paths using `python3 main.py --input path/to/data.csv --output results.jsonl`)*

### Expected Output
- The script will print the evaluation steps and the total number of flagged transactions.
- A new file named `flagged_transactions.jsonl` will be created in the directory.
- Execution time should be well under 10 minutes, as required.

## Challenge Deliverables

The prompt requested 4 specific deliverables. They are mapped to the following files in this repository:

1. **Code + README with run instructions:** 
   - `main.py` (The highly-modular core pipeline script)
   - `README.md` (This file, containing setup and run instructions)
2. **Rules Doc:** 
   - `Rules_and_Pipeline.md` (Contains our EDA findings, the 3 implemented rules with rationales, and the 2 deferred rules with our prioritization reasoning).
3. **Flagged-Output File:** 
   - `flagged_transactions.jsonl` (Contains all 992 flagged transactions formatted exactly as requested).
4. **Note on `confirmed_fraud.csv`:** 
   - `Confirmed_Fraud_Analysis.md` (A dedicated document explaining how we used the labeled dataset for EDA, our 78.9% recall performance against it, and why the dataset's inherent dispute bias prevents it from measuring false-positive rates).
