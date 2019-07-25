# DML Commands - 1 insert, 1 delete, 1 update, and 5 retrievals (2 MUST be complex)
USE spfny;

# INSERT --Will cause the Trigger to react
INSERT INTO customer VALUES (
						'abcd12345',
                        'Bob Sanders',
                        'password12345',
                        '1111111111111113',
                        '0118',
                        '123',
                        '1356 Jenkins Street',
                        'Oklahoma City',
                        'Oklahoma',
                        '73008');

INSERT INTO customer VALUES (
						'abcd12345',
                        'Bob Sanders',
                        'password12345',
                        '1111111111111113',
                        '0122',
                        '123',
                        '1356 Jenkins Street',
                        'Oklahoma City',
                        'Oklahoma',
                        '73008');


# DELETE
DELETE FROM designer
WHERE  Designer_Name = 'Michael Koors Light';

# UPDATE
UPDATE product
SET No_in_stock = '0'
WHERE Product_Name = 'ZZ Top';

# Retrieval 1
SELECT street, city, state, zip_code
FROM customer
WHERE username = 'Teemo';

# Retrieval 2 - show all the employees of spfny
SELECT Designer_Name
FROM designer;

# Retrieval 3
SELECT Bottom_Size
FROM bottoms
WHERE Bottom_Type = 'Skirt';

# Retrieval 4 - Complex
SELECT p.product_name, COUNT(*) AS Total_Reviews # give the product name and the amount of reviews it has
FROM review r, product p
WHERE P_Id = Product_Id;

# Retrieval 5 - Complex - Look for orders made in the month of May
SELECT Order_Date
FROM orders o
WHERE CAST(o.Order_Date AS CHAR) LIKE '_____05___';
