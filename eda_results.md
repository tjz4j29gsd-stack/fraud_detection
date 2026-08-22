# Exploratory Data Analysis (EDA) Summary

This document summarizes the initial findings from our exploration of the `transactions.csv` and `confirmed_fraud.csv` datasets. These insights directly informed the design of our proposed fraud rules.

## Dataset Overview

- **Total Transactions:** 1,001,000
- **Confirmed Fraud Transactions:** 190

> [!WARNING]
> The number of confirmed frauds is extremely small relative to the total dataset (~0.019%). As discussed, this is a biased sample of *reported* fraud. There is likely significant unreported fraud in the remaining 1M rows.

## 1. Merchant Analysis

We analyzed the top merchants across the entire dataset versus the top merchants in the confirmed fraud dataset. The contrast is stark and highly informative.

### Top Merchants Overall

The top merchants overall reflect typical consumer spending (retail, travel, food, tech).

| Merchant | Count |
| :--- | :--- |
| best buy | 12,477 |
| hilton | 12,475 |
| shell | 12,461 |
| delta air lines | 12,456 |
| chevron | 12,410 |
| ebay | 12,394 |
| google play | 12,388 |
| panda express | 12,387 |
| target | 12,366 |
| starbucks | 12,364 |

### Top Merchants for Confirmed Fraud

The merchants with the most confirmed fraud are almost exclusively digital goods, generic payment processors, or potential fake charities. These are classic targets for card testing or easy liquidation.

| Merchant | Count |
| :--- | :--- |
| gametop credits | 19 |
| digitalgoods llc | 18 |
| donatenow org | 15 |
| globalpay net | 15 |
| online-mkt 8827 | 14 |
| quicksub.io | 14 |
| appstore-micro | 14 |
| cloudhost basic | 13 |
| webservices pro | 11 |
| vpn-secure ltd | 9 |

> [!TIP]
> **Takeaway:** A rule specifically targeting high-risk digital goods merchants (like the ones listed above) could be highly effective.

## 2. Transaction Amount Analysis

We compared the distribution of transaction amounts (`amount` column) between the overall dataset and the confirmed fraud dataset.

### Overall Amount Distribution

- **Count:** 1,000,985 (Note: 15 rows dropped due to malformed data/nulls in our initial load)
- **Mean:** $40.20
- **Standard Deviation:** $58.35
- **Minimum:** -$186.03 *(Note: The spec says amounts should be positive debits. These negative values are likely refunds or data quality errors we need to clean during preprocessing).*
- **25th Percentile:** $13.03
- **Median (50%):** $24.73
- **75th Percentile:** $46.91
- **Maximum:** $4,463.72

### Confirmed Fraud Amount Distribution

- **Count:** 190
- **Mean:** $168.53
- **Standard Deviation:** $401.99
- **Minimum:** $0.51
- **25th Percentile:** $1.77
- **Median (50%):** $3.11
- **75th Percentile:** $4.60
- **Maximum:** $1,753.17

> [!IMPORTANT]
> **Takeaways:**
> 1. **Card Testing:** The median fraud amount is incredibly low ($3.11), with 75% of confirmed frauds being under $5. This strongly suggests fraudsters are performing "card testing" (running tiny authorizations to see if the stolen card is active) before moving on.
> 2. **High Variability:** While the median is tiny, the mean is very high ($168.53), and the max is massive ($1,753.17). This indicates a bifurcated fraud pattern: lots of tiny card-testing transactions, followed by a few massive, anomalous cash-out transactions.

## Next Steps

Based on this data, rules targeting **high velocity of small amounts** (card testing), **anomalous massive amounts** (cash-outs), and **high-risk digital merchants** are strongly supported by the evidence. 

Please let me know if you would like me to write additional python scripts to analyze other dimensions (e.g., time-of-day anomalies, or the number of unique devices per user)!
