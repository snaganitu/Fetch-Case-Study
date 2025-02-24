## SQL Query Explanation: Top 5 Brands by Total Quantity Purchased (Users 21+)

```sql
SELECT UPPER(TRIM(p.BRAND)) AS Standard_Brand, 
       SUM(CAST(t.FINAL_QUANTITY AS INTEGER)) AS Total_Quantity 
FROM USERS u 
JOIN TRANSACTIONS t ON u.ID = t.USER_ID 
JOIN PRODUCTS p ON t.BARCODE = p.BARCODE 
WHERE (JULIANDAY('now') - JULIANDAY(SUBSTR(u.BIRTH_DATE,1,10))) / 365.25 >= 21 
  AND t.FINAL_QUANTITY IS NOT NULL 
  AND LOWER(t.FINAL_QUANTITY) NOT IN ('0','zero') 
  AND p.BRAND IS NOT NULL 
  AND TRIM(p.BRAND) != '' 
GROUP BY Standard_Brand 
ORDER BY Total_Quantity DESC 
LIMIT 5;
```

```markdown
## SQL Query: Top 5 Brands by Total Quantity Purchased (Users 21 and Over)

### Query:
```sql
SELECT UPPER(TRIM(p.BRAND)) AS Standard_Brand, SUM(CAST(t.FINAL_QUANTITY AS INTEGER)) AS Total_Quantity 
FROM USERS u 
JOIN TRANSACTIONS t ON u.ID = t.USER_ID 
JOIN PRODUCTS p ON t.BARCODE = p.BARCODE 
WHERE (JULIANDAY('now') - JULIANDAY(SUBSTR(u.BIRTH_DATE,1,10)))/365.25 >= 21 
  AND t.FINAL_QUANTITY IS NOT NULL 
  AND LOWER(t.FINAL_QUANTITY) NOT IN ('0','zero') 
  AND p.BRAND IS NOT NULL 
  AND TRIM(p.BRAND) != '' 
GROUP BY Standard_Brand 
ORDER BY Total_Quantity DESC 
LIMIT 5;
```

This query calculates the total purchased quantity for each brand (after cleaning and standardizing brand names) and returns the top 5 brands, but only for users aged 21 or older.
# Query Breakdown:

**SELECT UPPER(TRIM(p.BRAND)) AS Standard_Brand, SUM(CAST(t.FINAL_QUANTITY AS INTEGER)) AS Total_Quantity:**
- **UPPER(TRIM(p.BRAND)) AS Standard_Brand:**  
  - This part normalizes the brand names by removing any extra spaces with `TRIM()` and converting them to uppercase with `UPPER()`, ensuring that the same brand is consistently represented.
- **SUM(CAST(t.FINAL_QUANTITY AS INTEGER)) AS Total_Quantity:**  
  - This converts the `FINAL_QUANTITY` (stored as text) into an integer and then sums these quantities to calculate the total quantity purchased for each brand.

**FROM USERS u JOIN TRANSACTIONS t ON u.ID = t.USER_ID JOIN PRODUCTS p ON t.BARCODE = p.BARCODE:**
- The query starts with the `USERS` table (aliased as `u`) and joins:
  - **TRANSACTIONS (t):** using `u.ID = t.USER_ID`, to connect each user with their transactions.
  - **PRODUCTS (p):** using `t.BARCODE = p.BARCODE`, to link each transaction to the corresponding product details (including the brand).

**WHERE (JULIANDAY('now') - JULIANDAY(SUBSTR(u.BIRTH_DATE,1,10)))/365.25 >= 21:**
- This calculates each user's age by:
  - Extracting the date portion (`YYYY-MM-DD`) from `BIRTH_DATE` using `SUBSTR(u.BIRTH_DATE,1,10)`.
  - Using `JULIANDAY()` to compute the difference between today's date and the user's birthdate.
  - Dividing by 365.25 to convert the difference from days to years.
- Only users who are **21 years or older** are included.

**AND t.FINAL_QUANTITY IS NOT NULL AND LOWER(t.FINAL_QUANTITY) NOT IN ('0','zero'):**
- Ensures that the `FINAL_QUANTITY` field has a valid, non-null value.
- Excludes transactions where the quantity is either "0" or the text "zero" (case-insensitive).

**AND p.BRAND IS NOT NULL AND TRIM(p.BRAND) != '':**
- Filters out any rows where the brand is either null or an empty string, so only valid brand names are processed.

**GROUP BY Standard_Brand:**
- Groups the data by the normalized brand name, so that the total quantity is calculated for each unique brand.

**ORDER BY Total_Quantity DESC:**
- Sorts the grouped results in descending order based on the total quantity purchased, placing the brands with the highest total quantity at the top.

**LIMIT 5:**
- Restricts the output to the top 5 brands.

## Key Assumptions in the Query

- **Date Format Consistency:**  
  It is assumed that all `BIRTH_DATE` values in the USERS table follow the format "YYYY-MM-DD ..." so that using `SUBSTR(u.BIRTH_DATE,1,10)` correctly extracts the date portion for age calculation.

- **Valid Age Calculation:**  
  The age is calculated using the difference in Julian days between the current date (`JULIANDAY('now')`) and the extracted birth date, divided by 365.25. We assume this method provides an accurate approximation of a user's age.

- **User Eligibility:**  
  Only users who are 21 years or older are included. This is based solely on the computed age, assuming no other factors need to be considered for eligibility.

- **Quantity Field Format:**  
  The `FINAL_QUANTITY` field in the TRANSACTIONS table is stored as text and may contain numeric values as well as the string "zero" (in various cases). We assume that:
  - Valid quantities are represented as numbers in text.
  - The string "zero" (or "0") indicates that no quantity was purchased.
  - Casting these values to an integer is safe and appropriate for aggregation.

- **Data Integrity in Joins:**  
  The query assumes that:
  - The `USER_ID` in TRANSACTIONS reliably matches the `ID` in USERS.
  - The `BARCODE` in TRANSACTIONS correctly corresponds to the `BARCODE` in PRODUCTS.
  These joins are assumed to accurately combine user, transaction, and product data.

- **Brand Normalization:**  
  By applying `UPPER(TRIM(p.BRAND))`, we assume that differences in letter case or extra whitespace are the only inconsistencies in the brand names, and that normalizing them will group similar brands correctly.

- **Exclusion of Invalid Data:**  
  It is assumed that rows with `NULL` or empty strings for `p.BRAND` or with `FINAL_QUANTITY` equal to "0" or "zero" are not useful for analysis and should be excluded.

- **Metric for "Receipts Scanned":**  
  The query uses the sum of the valid `FINAL_QUANTITY` values (after conversion) per brand as a proxy for "receipts scanned." This assumes that the total quantity accurately reflects the level of engagement or volume of purchases for each brand among users 21 and over.
