## Summary Output
---

### Number of customers
```sql
SELECT COUNT(DISTINCT customer_id) AS "Number of Customers" FROM transactions;
```
**`number of customers: 9454`**

---
### Total sales
```sql
SELECT FORMAT(SUM(sale_price),2) FROM transactions;
```
**`total sales: $64,161,803.52`**

---
### Total items bought
```sql
SELECT FORMAT(COUNT(*),0) FROM transactions; 
```
**`total items bought: 19,409,988`**

---
### Top 10 selling items with counts
```sql
SELECT manufacturer, product_name AS "product", size, FORMAT(COUNT(*),0) AS "count"
    FROM transactions
    JOIN catalog
    ON transactions.sku = catalog.sku
    GROUP BY transactions.sku
    ORDER BY COUNT(*) DESC
    LIMIT 10;
```
<table style="width=100%" border="0">
  <tr>
    <th>#</th>
    <th>Manufacturer</th>
    <th>Product</th>
    <th>Size</th>
    <th>Count</th>
  </tr>
  <tr>
    <td>
      1
    </td>
    <td>
      Rowan Dairy
    </td>
    <td>
      Whole Milk Milk
    </td>
    <td>
      1/2 gal
    </td>
    <td>
      48,735
    </td>
  </tr>
  </tr>
    <td>
      2
    </td>
    <td>
      Rowan Dairy
    </td>
    <td>
      1.00% Milk
    </td>
    <td>
      1/2 gal
    </td>
    <td>
      48,704
    </td>
  </tr>
  </tr>
    <td>
      3
    </td>
    <td>
      Rowan Dairy
    </td>
    <td>
      2.00% Milk
    </td>
    <td>
      1/2 gal
    </td>
    <td>
      48,618
    </td>
  </tr>
  </tr>
    <td>
      4
    </td>
    <td>
      Rowan Dairy
    </td>
    <td>
      1.00% Milk
    </td>
    <td>
      1 gal
    </td>
    <td>
      48,533
    </td>
  </tr>
  </tr>
    <td>
      5
    </td>
    <td>
      Rowan Dairy
    </td>
    <td>
      Whole Milk Milk
    </td>
    <td>
      1 gal
    </td>
    <td>
      48,514
    </td>
  </tr>
  </tr>
    <td>
      6
    </td>
    <td>
      Rowan Dairy
    </td>
    <td>
      2.00% Milk
    </td>
    <td>
      1 gal
    </td>
    <td>
      48,467
    </td>
  </tr>
  </tr>
    <td>
      7
    </td>
    <td>
      Smuckers
    </td>
    <td>
      Jelly Grape
    </td>
    <td>
      18 oz
    </td>
    <td>
      14,101
    </td>
  </tr>
  </tr>
    <td>
      8
    </td>
    <td>
      Smuckers
    </td>
    <td>
      Squeeze Jelly Grape
    </td>
    <td>
      20 oz
    </td>
    <td>
      14,062
    </td>
  </tr>
  </tr>
    <td>
      9
    </td>
    <td>
      Smuckers
    </td>
    <td>
      Jam Grape
    </td>
    <td>
      18 oz
    </td>
    <td>
      14,004
    </td>
  </tr>
  </tr>
    <td>
      10
    </td>
    <td>
      Smuckers
    </td>
    <td>
      Jam Strawberry
    </td>
    <td>
      18 oz
    </td>
    <td>
      13,921
    </td>
  </tr>
</table>

---
### Average total sales per customer
```sql
SELECT FORMAT((
    (SELECT SUM(sale_price) FROM transactions) /
    (SELECT COUNT(DISTINCT customer_id) FROM transactions)),2);
```
**`average total sales per customer: $6,786.74`**