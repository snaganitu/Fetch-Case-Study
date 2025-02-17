import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV files
users_df = pd.read_csv("USER_TAKEHOME.csv")
transactions_df = pd.read_csv("TRANSACTION_TAKEHOME.csv")
products_df = pd.read_csv("PRODUCTS_TAKEHOME.csv")

# Function to check for missing values, duplicates, and data types
def check_data_quality(df, file_name, primary_keys):
    print(f"\n🔍 Checking Data Quality for: {file_name}")
    print("=" * 60)

    # 🔹 Check for missing values
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]  # Filter only columns with missing values
    print("\n🛑 Missing Values Per Column:")
    print(missing_values)

    if not missing_values.empty:
        # 📊 Visualizing missing values
        plt.figure(figsize=(10, 5))
        missing_values.plot(kind="bar", color="red")
        plt.title(f"Missing Values in {file_name}")
        plt.ylabel("Number of Missing Values")
        plt.xlabel("Columns")
        plt.xticks(rotation=45)
        plt.show()

        # 🔎 Show sample rows with missing values
        print("\n📌 Sample Rows with Missing Data:")
        print(df[df.isnull().any(axis=1)].head(3))

    # 🔹 Handling Missing Values (Replacing NaN in non-primary columns)
    non_primary_cols = [col for col in df.columns if col not in primary_keys]
    df[non_primary_cols] = df[non_primary_cols].fillna("Unknown")

    # 🔹 Check for duplicate rows based on the specific primary keys
    if all(col in df.columns for col in primary_keys):
        duplicate_rows = df[df.duplicated(subset=primary_keys)]
        print(f"\n⚠️ Total Duplicate Rows (Based on {primary_keys}): {len(duplicate_rows)}")
    else:
        print(f"\n⚠️ Skipping duplicate check! Columns {primary_keys} not found in {file_name}.")
        duplicate_rows = pd.DataFrame()  # Empty DataFrame to avoid errors

    if not duplicate_rows.empty:
        print("\n🔄 Sample Duplicate Records (after checking based on primary keys only):")
        print(duplicate_rows.head(2))  # Show first 2 duplicate rows

    # 🔹 Check for incorrect data types
    print("\n📊 Column Data Types:")
    print(df.dtypes)

    # 🔹 Check for empty strings
    empty_strings = (df == "").sum()
    empty_strings = empty_strings[empty_strings > 0]  # Filter only columns with empty strings
    print("\n⚠️ Empty String Values:")
    print(empty_strings)

# Run the function on each dataset with the correct primary keys
check_data_quality(users_df, "USER_TAKEHOME.csv", primary_keys=["ID"])
check_data_quality(transactions_df, "TRANSACTION_TAKEHOME.csv", primary_keys=["RECEIPT_ID", "BARCODE"])
check_data_quality(products_df, "PRODUCTS_TAKEHOME.csv", primary_keys=["BARCODE"])
