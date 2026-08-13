"""
╔══════════════════════════════════════════════════════════════════════╗
║         PROFESSIONAL DATA QUALITY INSPECTION TOOL                   ║
║         Built for BI Analysts and Data Analysts                     ║
║         Run this on ANY dataset before cleaning begins              ║
║                                                                      ║
║  Usage:                                                              ║
║     from data_quality_inspector import inspect                       ║
║     df = pd.read_csv("your_file.csv")                               ║
║     inspect(df)                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np


def inspect(df, id_column=None, numeric_floor=None, max_categories=20):
    """
    Professional Data Quality Inspection Tool.

    Parameters:
    -----------
    df              : your pandas DataFrame
    id_column       : column that should be unique (e.g. 'Order ID')
    numeric_floor   : dict of minimum allowed values
                      e.g. {'Sales': 0, 'Quantity': 1}
    max_categories  : max unique values to show per categorical column
    """

    DIVIDER = "=" * 70
    rows, cols = df.shape

    def header(title):
        print(f"\n{DIVIDER}")
        print(f"  {title}")
        print(DIVIDER)

    # ══════════════════════════════════════════════════════
    # SECTION 1 — DATASET OVERVIEW
    # ══════════════════════════════════════════════════════
    header("SECTION 1 — DATASET OVERVIEW")
    print(f"\n  Total Rows:    {rows:,}")
    print(f"  Total Columns: {cols}")
    print(f"  Memory Usage:  {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    print(f"\n  Column Names ({cols} total):")
    for i, col in enumerate(df.columns, 1):
        print(f"    {i:2}. {col}")

    # ══════════════════════════════════════════════════════
    # SECTION 2 — DATA TYPES
    # Business problem: Wrong data type = broken calculations
    # If Sales is stored as text you cannot SUM it
    # ══════════════════════════════════════════════════════
    header("SECTION 2 — DATA TYPES")
    print(f"\n  {'Column':<25} {'Type':<15} {'Flag'}")
    print(f"  {'-'*25} {'-'*15} {'-'*25}")

    numeric_keywords = ['sales', 'profit', 'price', 'cost',
                        'revenue', 'amount', 'total', 'margin',
                        'discount', 'quantity', 'qty']
    date_keywords = ['date', 'time', 'day', 'month', 'year']

    for col in df.columns:
        dtype = str(df[col].dtype)
        flag = ""
        if dtype in ['object', 'str']:
            if any(kw in col.lower() for kw in numeric_keywords):
                flag = "⚠️  SHOULD THIS BE NUMERIC?"
            elif any(kw in col.lower() for kw in date_keywords):
                flag = "⚠️  SHOULD THIS BE DATETIME?"
        print(f"  {col:<25} {dtype:<15} {flag}")

    # ══════════════════════════════════════════════════════
    # SECTION 3 — MISSING VALUES (NaN / NULL)
    # Business problem: Missing values break calculations
    # and exclude rows silently from analysis
    # ══════════════════════════════════════════════════════
    header("SECTION 3 — MISSING VALUES (NaN / NULL)")
    missing = df.isnull().sum()
    missing_pct = (missing / rows * 100).round(2)
    has_missing = missing[missing > 0]

    if len(has_missing) == 0:
        print("\n  ✅ No missing values found.")
    else:
        print(f"\n  ⚠️  {len(has_missing)} columns have missing values:\n")
        print(f"  {'Column':<25} {'Count':<12} {'Percent':<12} {'Severity'}")
        print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*15}")
        for col in has_missing.index:
            count = has_missing[col]
            pct = missing_pct[col]
            severity = "Low" if pct < 1 else "Medium ⚠️" if pct < 5 else "HIGH 🔴"
            print(f"  {col:<25} {count:<12,} {pct:<12.1f}% {severity}")

    # ══════════════════════════════════════════════════════
    # SECTION 4 — EMPTY STRINGS
    # Business problem: fillna() does NOT catch empty strings
    # '' looks blank but is NOT null — easy to miss
    # ══════════════════════════════════════════════════════
    header("SECTION 4 — EMPTY STRINGS")
    text_cols = [c for c in df.columns
                 if str(df[c].dtype) in ['object', 'str']]
    found_empty = False

    print(f"\n  {'Column':<25} {'Empty Strings':<15} {'% of Total'}")
    print(f"  {'-'*25} {'-'*15} {'-'*12}")

    for col in text_cols:
        empty_count = (df[col].astype(str).str.strip() == '').sum()
        if empty_count > 0:
            found_empty = True
            pct = empty_count / rows * 100
            print(f"  {col:<25} {empty_count:<15,} {pct:.1f}%  ⚠️")

    if not found_empty:
        print("\n  ✅ No empty strings found.")

    # ══════════════════════════════════════════════════════
    # SECTION 5 — DUPLICATE ROWS
    # Business problem: Duplicate rows inflate every metric
    # Revenue looks higher than it really is
    # ══════════════════════════════════════════════════════
    header("SECTION 5 — DUPLICATE ROWS")
    dupe_count = df.duplicated().sum()
    dupe_pct = dupe_count / rows * 100

    if dupe_count == 0:
        print("\n  ✅ No duplicate rows found.")
    else:
        print(f"\n  ⚠️  Duplicate rows: {dupe_count:,} ({dupe_pct:.1f}% of data)")
        print(f"\n  Sample duplicated rows:")
        dupes = df[df.duplicated(keep=False)].head(4)
        print(dupes.to_string(max_cols=5, max_colwidth=20))

    if id_column and id_column in df.columns:
        id_dupes = df[id_column].duplicated().sum()
        print(f"\n  ID Column '{id_column}' duplicates: {id_dupes:,}")
        if id_dupes > 0:
            print(f"  ℹ️  Expected if one order has multiple products.")

    # ══════════════════════════════════════════════════════
    # SECTION 6 — LEADING / TRAILING SPACES
    # Business problem: 'Furniture' and 'Furniture '
    # look identical but create separate Pivot Table rows
    # ══════════════════════════════════════════════════════
    header("SECTION 6 — LEADING / TRAILING SPACES")
    found_spaces = False

    print(f"\n  {'Column':<25} {'Rows Affected':<15} {'Example'}")
    print(f"  {'-'*25} {'-'*15} {'-'*35}")

    for col in text_cols:
        has_spaces = df[col].dropna().astype(str).apply(
            lambda x: x != x.strip()
        ).sum()
        if has_spaces > 0:
            found_spaces = True
            example_series = df[col].dropna().astype(str)
            bad = example_series[example_series != example_series.str.strip()]
            bad_example = bad.iloc[0] if len(bad) > 0 else ""
            print(f"  {col:<25} {has_spaces:<15,} '{bad_example}' → '{bad_example.strip()}'")

    if not found_spaces:
        print("\n  ✅ No leading or trailing spaces found.")

    # ══════════════════════════════════════════════════════
    # SECTION 7 — INCONSISTENT CAPITALIZATION
    # Business problem: 'West', 'WEST', 'west' are 3 different
    # values — your Pivot Table shows 3 rows instead of 1
    # ══════════════════════════════════════════════════════
    header("SECTION 7 — INCONSISTENT CAPITALIZATION")
    print()

    for col in text_cols:
        if df[col].nunique() > 50:
            continue
        unique_vals = df[col].dropna().astype(str).unique()
        seen = {}
        conflicts = {}
        for original in unique_vals:
            lower = original.strip().lower()
            if lower in seen:
                if lower not in conflicts:
                    conflicts[lower] = [seen[lower]]
                conflicts[lower].append(original)
            else:
                seen[lower] = original

        if conflicts:
            print(f"  ⚠️  {col} — Case inconsistencies:")
            for base, variants in list(conflicts.items())[:5]:
                print(f"       {variants}")
        else:
            if len(unique_vals) <= 20:
                print(f"  ✅  {col} — Consistent ({len(unique_vals)} unique values)")

    # ══════════════════════════════════════════════════════
    # SECTION 8 — UNIQUE VALUES AND VALUE COUNTS
    # Business problem: Abbreviations and typos hide in data
    # 'W', 'Cntrl', 'Furnitre' corrupt your analysis
    # ══════════════════════════════════════════════════════
    header("SECTION 8 — UNIQUE VALUES & VALUE COUNTS")
    print()

    for col in text_cols:
        n_unique = df[col].nunique()
        if n_unique > max_categories:
            print(f"  {col}: {n_unique:,} unique values (high cardinality — skipped)")
            continue

        print(f"\n  {col} ({n_unique} unique values):")
        vc = df[col].value_counts(dropna=False).head(max_categories)

        for val, count in vc.items():
            pct = count / rows * 100
            flag = ""
            val_str = str(val)
            if val_str != val_str.strip():
                flag = "← has spaces ⚠️"
            elif val_str.isupper() and len(val_str) > 1:
                flag = "← ALL CAPS ⚠️"
            elif val_str.islower() and len(val_str) > 2:
                flag = "← all lowercase ⚠️"
            elif len(val_str) <= 2 and val_str.isalpha():
                flag = "← possible abbreviation ⚠️"
            elif str(val) == 'nan':
                flag = "← NULL / MISSING 🔴"

            print(f"    {val_str:<30} {count:>6,}  ({pct:>5.1f}%)  {flag}")

    # ══════════════════════════════════════════════════════
    # SECTION 9 — NUMERIC COLUMN STATISTICS
    # Business problem: Numeric summaries reveal impossible
    # values — negative Sales, zero Quantity, extreme outliers
    # ══════════════════════════════════════════════════════
    header("SECTION 9 — NUMERIC COLUMN STATISTICS")
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not num_cols:
        print("\n  ⚠️  No numeric columns detected.")
        print("  Check Section 2 — numeric columns may be stored as text.")
    else:
        print(f"\n  {'Column':<20} {'Count':>8} {'Min':>12} "
              f"{'Max':>12} {'Mean':>12} {'Nulls':>8}")
        print(f"  {'-'*20} {'-'*8} {'-'*12} {'-'*12} {'-'*12} {'-'*8}")
        for col in num_cols:
            s = df[col].dropna()
            if len(s) == 0:
                continue
            print(f"  {col:<20} {len(s):>8,} {s.min():>12.2f} "
                  f"{s.max():>12.2f} {s.mean():>12.2f} "
                  f"{df[col].isnull().sum():>8,}")

    # ══════════════════════════════════════════════════════
    # SECTION 10 — NEGATIVE VALUES
    # Business problem: Sales = -$500 is impossible
    # Corrupts your revenue totals silently
    # ══════════════════════════════════════════════════════
    header("SECTION 10 — NEGATIVE VALUES")
    found_negatives = False
    print()

    for col in num_cols:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            found_negatives = True
            neg_pct = neg_count / rows * 100
            neg_vals = df[df[col] < 0][col]
            verdict = ("✅ Expected (losses are valid)"
                       if col.lower() in ['profit', 'margin']
                       else "🔴 INVESTIGATE — possible data error")
            print(f"  {col}:")
            print(f"    Count:   {neg_count:,} ({neg_pct:.1f}%)")
            print(f"    Min:     {neg_vals.min():,.2f}")
            print(f"    Verdict: {verdict}\n")

    if numeric_floor:
        print("  Business Rule Violations:")
        for col, floor in numeric_floor.items():
            if col in df.columns:
                try:
                    violations = (df[col] < floor).sum()
                    if violations > 0:
                        print(f"  ⚠️  {col}: {violations:,} values below {floor}")
                    else:
                        print(f"  ✅  {col}: all values >= {floor}")
                except Exception:
                    print(f"  ⚠️  {col}: could not check (non-numeric dtype)")

    if not found_negatives:
        print("  ✅ No negative values in numeric columns.")

    # ══════════════════════════════════════════════════════
    # SECTION 11 — OUTLIERS (IQR METHOD)
    # Business problem: One $50,000 order makes your average
    # order value look 3x higher than typical
    # ══════════════════════════════════════════════════════
    header("SECTION 11 — OUTLIERS (IQR METHOD)")
    print()

    for col in num_cols:
        s = df[col].dropna()
        if len(s) < 4:
            continue
        try:
            Q1 = s.quantile(0.25)
            Q3 = s.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()
            pct = outlier_count / rows * 100
            if outlier_count > 0:
                print(f"  {col}:")
                print(f"    Outlier count: {outlier_count:,} ({pct:.1f}%)")
                print(f"    Normal range:  {lower:,.2f} to {upper:,.2f}")
                print(f"    Actual range:  {s.min():,.2f} to {s.max():,.2f}\n")
        except Exception:
            print(f"  {col}: Could not compute outliers")

    # ══════════════════════════════════════════════════════
    # SECTION 12 — DATE COLUMNS
    # Business problem: Dates stored as text cannot be used
    # for monthly trends, year-over-year, seasonal analysis
    # ══════════════════════════════════════════════════════
    header("SECTION 12 — DATE COLUMN ANALYSIS")
    date_cols = [c for c in df.columns
                 if any(kw in c.lower() for kw in date_keywords)]

    if not date_cols:
        print("\n  No date columns detected.")
    else:
        for col in date_cols:
            dtype = str(df[col].dtype)
            print(f"\n  {col}:")
            print(f"    Current dtype: {dtype}")
            if 'datetime' in dtype:
                s = df[col].dropna()
                print(f"    ✅ Correct datetime format")
                print(f"    Range: {s.min()} → {s.max()}")
            else:
                sample = df[col].dropna().head(3).tolist()
                print(f"    ⚠️  Stored as text. Sample: {sample}")
                print(f"    Fix: df['{col}'] = pd.to_datetime(df['{col}'], errors='coerce')")
                try:
                    converted = pd.to_datetime(df[col], errors='coerce')
                    failed = converted.isnull().sum() - df[col].isnull().sum()
                    if failed > 0:
                        print(f"    ⚠️  {failed} values fail date conversion")
                    else:
                        print(f"    ✅ All values convert successfully")
                except Exception:
                    pass

    # ══════════════════════════════════════════════════════
    # SECTION 13 — MIXED DATA TYPES (numbers stored as text)
    # Business problem: '239.50 USD' cannot be summed
    # Looks like a number, behaves like text
    # ══════════════════════════════════════════════════════
    header("SECTION 13 — MIXED DATA TYPES")
    print()
    found_mixed = False

    for col in text_cols:
        s = df[col].dropna().astype(str)
        if len(s) == 0:
            continue
        try:
            numeric_attempt = pd.to_numeric(s, errors='coerce')
            convertible_pct = (numeric_attempt.notna().sum() / len(s)) * 100

            if 20 < convertible_pct < 100:
                found_mixed = True
                non_numeric = s[numeric_attempt.isna()]
                sample_bad = non_numeric.head(3).tolist()
                print(f"  ⚠️  {col}: {convertible_pct:.0f}% numeric but stored as text")
                print(f"    Contamination sample: {sample_bad}")
                print(f"    Fix: clean text then pd.to_numeric(df['{col}'], errors='coerce')\n")
            elif convertible_pct == 100:
                skip_cols = ['order id', 'customer id', 'product id', 'postal code', 'row id']
                if any(kw in col.lower() for kw in numeric_keywords):
                    if col.lower() not in skip_cols:
                        found_mixed = True
                        print(f"  ⚠️  {col}: 100% numeric but stored as text")
                        print(f"    Fix: df['{col}'] = pd.to_numeric(df['{col}'], errors='coerce')\n")
        except Exception:
            pass

    if not found_mixed:
        print("  ✅ No mixed data type issues found.")

    # ══════════════════════════════════════════════════════
    # SECTION 14 — SINGLE VALUE COLUMNS (useless columns)
    # Business problem: A column where every row has the same
    # value provides zero analytical value
    # ══════════════════════════════════════════════════════
    header("SECTION 14 — USELESS COLUMNS (SINGLE UNIQUE VALUE)")
    single_value = []

    for col in df.columns:
        if df[col].nunique() <= 1:
            single_value.append(col)
            val = df[col].unique()[0] if df[col].nunique() == 1 else "ALL NULL"
            print(f"\n  ⚠️  {col}: only value is '{val}'")

    if not single_value:
        print("\n  ✅ No single-value columns found.")

    # ══════════════════════════════════════════════════════
    # SECTION 15 — DATA QUALITY SCORECARD
    # Your final verdict: is this data safe to analyze?
    # ══════════════════════════════════════════════════════
    header("SECTION 15 — DATA QUALITY SCORECARD")

    issues = []
    score = 100

    total_missing = df.isnull().sum().sum()
    if total_missing > 0:
        pct = total_missing / (rows * cols) * 100
        issues.append(f"Missing values: {total_missing:,} cells ({pct:.2f}%)")
        score -= min(20, int(pct * 2))

    dupe_count = df.duplicated().sum()
    if dupe_count > 0:
        issues.append(f"Duplicate rows: {dupe_count:,} ({dupe_count/rows*100:.1f}%)")
        score -= min(15, int(dupe_count / rows * 100))

    inconsistent_cols = 0
    for col in text_cols:
        if df[col].nunique() > 50:
            continue
        unique_vals = df[col].dropna().astype(str).unique()
        seen = {}
        conflict_found = False
        for v in unique_vals:
            lower = v.strip().lower()
            if lower in seen:
                conflict_found = True
                break
            seen[lower] = v
        if conflict_found:
            inconsistent_cols += 1
    if inconsistent_cols > 0:
        issues.append(f"Inconsistent capitalization: {inconsistent_cols} column(s)")
        score -= inconsistent_cols * 3

    space_cols = sum(
        1 for col in text_cols
        if df[col].dropna().astype(str).apply(lambda x: x != x.strip()).sum() > 0
    )
    if space_cols > 0:
        issues.append(f"Leading/trailing spaces: {space_cols} column(s)")
        score -= space_cols * 2

    mixed_cols = 0
    for col in text_cols:
        if any(kw in col.lower() for kw in numeric_keywords):
            try:
                s = df[col].dropna().astype(str)
                converted = pd.to_numeric(s, errors='coerce')
                if converted.notna().sum() > 0:
                    mixed_cols += 1
            except Exception:
                pass
    if mixed_cols > 0:
        issues.append(f"Numeric columns stored as text: {mixed_cols}")
        score -= mixed_cols * 5

    score = max(0, score)

    if score >= 90:
        rating = "EXCELLENT ✅ — Safe to analyze"
    elif score >= 70:
        rating = "GOOD ⚠️ — Minor cleaning needed"
    elif score >= 50:
        rating = "POOR 🔴 — Significant cleaning required"
    else:
        rating = "CRITICAL 🚨 — Do not analyze until cleaned"

    print(f"\n  SCORE:  {score}/100")
    print(f"  RATING: {rating}")

    if issues:
        print(f"\n  Issues to fix (in order of priority):")
        for i, issue in enumerate(issues, 1):
            print(f"    {i}. {issue}")

    print(f"\n  RECOMMENDED CLEANING ORDER:")
    steps = [
        "Fix data types (numeric columns stored as text)",
        "Remove duplicate rows → drop_duplicates()",
        "Handle missing values → fillna() or replace()",
        "Remove leading/trailing spaces → str.strip()",
        "Standardize capitalization → str.title()",
        "Fix abbreviations and typos → replace({})",
        "Remove impossible values (negative Sales)",
        "Fix date formats → pd.to_datetime()",
        "Drop useless single-value columns"
    ]
    for i, step in enumerate(steps, 1):
        print(f"    {i}. {step}")

    print(f"\n{DIVIDER}")
    print(f"  INSPECTION COMPLETE — {rows:,} rows × {cols} columns")
    print(DIVIDER)