import pandas as pd
import json
import time
import argparse
import sys

def load_and_clean_data(file_path):
    """Loads transactions from CSV and performs necessary data cleaning."""
    print("Loading and cleaning data...")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please ensure you have downloaded the dataset locally.")
        sys.exit(1)
        
    # Clean missing or malformed timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    
    # Normalize merchant names and filter valid amounts (positive = debit per spec)
    df['merchant_name'] = df['merchant_name'].str.lower().str.strip()
    df = df[df['amount'] >= 0].copy()
    
    # Sort chronologically for accurate time-window calculations
    df = df.sort_values(by=['timestamp']).reset_index(drop=True)
    
    # Initialize output columns for flags
    df['rules_fired'] = [[] for _ in range(len(df))]
    df['reason'] = ""
    
    return df

def apply_rule_1_card_testing(df):
    """Flags high velocity of micro-transactions (<$5) by a single user."""
    print("Evaluating Rule 1: Card Testing Velocity...")
    small_txns = df[df['amount'] < 5.0].copy()
    small_txns['time_diff'] = small_txns.groupby('user_id')['timestamp'].diff(periods=3)
    rule1_idx = small_txns[small_txns['time_diff'] <= pd.Timedelta(minutes=15)].index
    
    df.loc[rule1_idx, 'rules_fired'] = df.loc[rule1_idx, 'rules_fired'].apply(lambda x: x + ['Rule 1: Card Testing'])
    df.loc[rule1_idx, 'reason'] = df.loc[rule1_idx, 'reason'] + "High velocity of micro-transactions (<$5) within 15 minutes. "
    return df

def apply_rule_2_high_risk_merchants(df):
    """Flags stealthy card testing behavior strictly at high-risk merchants."""
    print("Evaluating Rule 2: Stealthy Card Testing (High-Risk Merchants)...")
    high_risk = ['gametop credits', 'digitalgoods llc', 'donatenow org', 'globalpay net', 'online-mkt 8827', 'quicksub.io', 'appstore-micro']
    hr_txns = df[df['merchant_name'].isin(high_risk)].copy()
    hr_txns = hr_txns.sort_values(by=['user_id', 'timestamp'])
    
    hr_txns['time_diff'] = hr_txns.groupby('user_id')['timestamp'].diff(periods=1)
    rule2_idx = hr_txns[hr_txns['time_diff'] <= pd.Timedelta(hours=24)].index
    
    df.loc[rule2_idx, 'rules_fired'] = df.loc[rule2_idx, 'rules_fired'].apply(lambda x: x + ['Rule 2: Stealthy Card Testing'])
    df.loc[rule2_idx, 'reason'] = df.loc[rule2_idx, 'reason'] + "Multiple transactions at high-risk digital goods merchants within 24 hours. "
    return df

def apply_rule_3_account_takeover(df):
    """Flags massive transactions on new devices for established users."""
    print("Evaluating Rule 3: Account Takeover (New Device Cash-out)...")
    df['user_first_txn'] = df.groupby('user_id')['timestamp'].transform('min')
    df['days_since_user_first_txn'] = (df['timestamp'] - df['user_first_txn']).dt.days
    
    df['device_first_txn'] = df.groupby(['user_id', 'device_id'])['timestamp'].transform('min')
    df['is_first_device_use'] = df['timestamp'] == df['device_first_txn']
    
    rule3_mask = (df['days_since_user_first_txn'] > 14) & df['is_first_device_use'] & (df['amount'] > 500)
    rule3_idx = df[rule3_mask].index
    
    df.loc[rule3_idx, 'rules_fired'] = df.loc[rule3_idx, 'rules_fired'].apply(lambda x: x + ['Rule 3: ATO High Amount'])
    df.loc[rule3_idx, 'reason'] = df.loc[rule3_idx, 'reason'] + "Massive transaction (>$500) on a device previously unseen for this established user. "
    return df

def save_flagged_transactions(df, output_path):
    """Extracts flagged transactions and writes them to a JSONL file."""
    flagged_df = df[df['rules_fired'].apply(len) > 0].copy()
    flagged_df['reason'] = flagged_df['reason'].str.strip()
    output_data = flagged_df[['txn_id', 'rules_fired', 'reason']].to_dict(orient='records')
    
    print(f"Total Flagged Transactions: {len(output_data)}")
    print(f"Saving output to {output_path}...")
    
    with open(output_path, 'w') as f:
        for record in output_data:
            f.write(json.dumps(record) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Fraud Detection Pipeline')
    parser.add_argument('--input', type=str, default='transactions.csv', help='Path to input CSV file')
    parser.add_argument('--output', type=str, default='flagged_transactions.jsonl', help='Path to output JSONL file')
    args = parser.parse_args()

    print("Starting Fraud Detection Pipeline...")
    start_time = time.time()
    
    # Execute Pipeline
    df = load_and_clean_data(args.input)
    df = apply_rule_1_card_testing(df)
    df = apply_rule_2_high_risk_merchants(df)
    df = apply_rule_3_account_takeover(df)
    save_flagged_transactions(df, args.output)
            
    elapsed = time.time() - start_time
    print(f"Pipeline completed in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
