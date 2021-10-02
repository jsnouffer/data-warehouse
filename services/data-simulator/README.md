### Queries to verify simulation

Get percentage of MILK among all transactions **(70%)**
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of CEREAL among MILK transactions **(50%)**
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'CEREAL'
            INTERSECT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK');
```
Get percentage of CEREAL among non MILK transactions **(5%)**
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'CEREAL'
        EXCEPT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK') I) /
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions
        EXCEPT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK') J);
```

Get percentage of BABY FOOD among all transactions **(20%)**
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of DIAPERS among BABY FOOD transactions **(80%)**
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'DIAPERS'
            INTERSECT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD');
```

Get percentage of DIAPERS among non BABY FOOD transactions **(1%)**
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'DIAPERS'
        EXCEPT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD') I) /
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions
        EXCEPT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD') J);
```

Get percentage of BREAD among all transactions **(50%)**
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BREAD') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of PEANUT BUTTER among all transactions **(10%)**
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of JELLY/JAM among PEANUT BUTTER transactions **(90%)**
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'JELLY/JAM'
            INTERSECT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER');
```

Get percentage of JELLY/JAM among non PEANUT BUTTER transactions **(5%)**
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'JELLY/JAM'
        EXCEPT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER') I) /
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions
        EXCEPT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER') J);
```

Average customer visits per day **((1100 + 1150)/2 + 100/7 ~= 1139)**
```sql
SELECT
    (SELECT COUNT(DISTINCT transaction_id) FROM transactions) /
    (SELECT COUNT(DISTINCT transaction_date) from transactions);
```

Average items per customer **(90/2 + 1 ~= 46)**
```sql
SELECT
    (SELECT COUNT(*) FROM transactions) /
    (SELECT COUNT(DISTINCT transaction_id) from transactions);
```