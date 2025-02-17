### SQL Query Explanation

```sql
SELECT p.BRAND, COUNT(t.RECEIPT_ID) AS Receipts_Scanned 
FROM TRANSACTIONS t 
JOIN PRODUCTS p ON t.BARCODE = p.BARCODE 
JOIN USERS u ON t.USER_ID = u.ID 
WHERE (JULIANDAY('now') - JULIANDAY(u.BIRTH_DATE)) / 365.25 >= 21  -- Filter users 21 and over 
AND p.BRAND IS NOT NULL AND p.BRAND != ''  -- Exclude null or empty brand names
GROUP BY p.BRAND 
ORDER BY Receipts_Scanned DESC 
LIMIT 5;
```

#### Query Breakdown:
1. **SELECT p.BRAND, COUNT(t.RECEIPT_ID) AS Receipts_Scanned**: 
   - This part selects the `BRAND` from the `PRODUCTS` table and counts the number of `RECEIPT_ID` from the `TRANSACTIONS` table for each brand.
   - The `Receipts_Scanned` column represents how many times a brand's products were scanned in the transactions.

2. **FROM TRANSACTIONS t**: 
   - This specifies the main table for the query, `TRANSACTIONS`, aliased as `t`.

3. **JOIN PRODUCTS p ON t.BARCODE = p.BARCODE**: 
   - This joins the `PRODUCTS` table (aliased as `p`) with the `TRANSACTIONS` table based on the matching `BARCODE` values. This allows us to link each transaction to the corresponding product's brand.

4. **JOIN USERS u ON t.USER_ID = u.ID**: 
   - This joins the `USERS` table (aliased as `u`) with the `TRANSACTIONS` table based on the matching `USER_ID` values. This ensures we have access to user information for filtering based on age.

5. **WHERE (JULIANDAY('now') - JULIANDAY(u.BIRTH_DATE)) / 365.25 >= 21**: 
   - This filters the users to include only those who are 21 years old or older. The `JULIANDAY()` function returns the Julian day number, representing a continuous count of days. The subtraction between the current date (`'now'`) and the user's birthdate (`u.BIRTH_DATE`) gives the number of days, which is then divided by 365.25 to approximate the user's age in years.

6. **AND p.BRAND IS NOT NULL AND p.BRAND != ''**: 
   - This excludes rows where the `BRAND` is null or an empty string, ensuring only valid brands are counted.

7. **GROUP BY p.BRAND**: 
   - This groups the result by brand, so that we can count the number of receipts for each brand.

8. **ORDER BY Receipts_Scanned DESC**: 
   - This orders the result by the `Receipts_Scanned` count in descending order, meaning the most scanned brands will appear first.

9. **LIMIT 5**: 
   - This limits the output to the top 5 brands with the most scanned receipts.

### Output Explanation:

```
COCA-COLA,628
"ANNIE'S HOMEGROWN GROCERY",576
DOVE,558
BAREFOOT,552
ORIBE,504
```

- The output shows the **top 5 brands** with the highest number of scanned receipts for users aged 21 and older.
- For example, **COCA-COLA** appears first with 628 scanned receipts, meaning products from Coca-Cola were scanned 628 times in the transactions of users aged 21 or older.
- **"ANNIE'S HOMEGROWN GROCERY"** is in second place with 576 scans, and so on for the other brands.
- This list helps identify the **most popular brands** among users in this age group based on transaction data.

This information could be used to gauge brand popularity or consumer behavior within specific demographics (like users over 21).