# Views - 3 examples
USE spfny;

# View 1
CREATE VIEW All_Orders_of_Customer
AS SELECT Customer_Name, Order_Number, Product_Name
	FROM orders, customer, product
	WHERE C_Id = Customer_Id AND P_Id = Product_Id
    GROUP BY C_Id;
    
# View 2
CREATE VIEW All_Types_of_Clothes
AS SELECT Product_Id, Product_Name, T_Type, B_Type, S_Type
	FROM product p, top_type t, bottom_type b, shoe_type s
    WHERE Product_Id = t.P_Id OR Product_Id = b.P_Id OR Product_Id = s.P_Id;

# View 3
CREATE VIEW All_Products_Made_by_Designer
AS SELECT Product_Name, Designer_Name
	FROM product p, designer d
	WHERE D_Id = Designer_Id;

