### Queries to verify simulation

Get percentage of MILK among all transactions
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of CEREAL among MILK transactions
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'CEREAL'
            INTERSECT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'MILK');
```

Get percentage of BABY FOOD among all transactions
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of DIAPERS among BABY FOOD transactions
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'DIAPERS'
            INTERSECT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BABY FOOD');
```

Get percentage of BREAD among all transactions
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'BREAD') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of PEANUT BUTTER among all transactions
```sql
SELECT
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER') /
    (SELECT COUNT(DISTINCT(transaction_id)) FROM transactions);
```

Get percentage of JELLY/JAM among PEANUT BUTTER transactions
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'JELLY/JAM'
            INTERSECT SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'PEANUT BUTTER');
```

Get percentage of JELLY/JAM among non PEANUT BUTTER transactions
```sql
SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'JELLY/JAM') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type != 'PEANUT BUTTER');
```

SELECT
    (SELECT COUNT(*) FROM
        (SELECT DISTINCT(transaction_id) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type = 'CEREAL') I) /
    (SELECT COUNT(*) FROM transactions JOIN catalog ON transactions.sku = catalog.sku WHERE item_type != 'MILK');