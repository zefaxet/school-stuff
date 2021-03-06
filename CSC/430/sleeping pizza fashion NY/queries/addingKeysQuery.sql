# -- FOREIGN KEYS for TABLES

# product
ALTER TABLE Product
ADD CONSTRAINT Product_Fk
  FOREIGN KEY (D_Id) REFERENCES Designer(Designer_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;
    
# tops
ALTER TABLE Tops
ADD CONSTRAINT Tops_Fk
  FOREIGN KEY (P_Id) REFERENCES Product(Product_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;

# bottoms
ALTER TABLE Bottoms
ADD CONSTRAINT Bottoms_Fk
  FOREIGN KEY (P_Id) REFERENCES Product(Product_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;
    
# shoes
ALTER TABLE Shoes
ADD CONSTRAINT Shoes_Fk
  FOREIGN KEY (P_Id) REFERENCES Product(Product_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;
	
# orders
ALTER TABLE Orders
ADD CONSTRAINT Order_C_Id_Fk
  FOREIGN KEY (C_Id) REFERENCES Customer(Customer_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
ADD CONSTRAINT Order_P_Id_Fk
  FOREIGN KEY (P_Id) REFERENCES Product(Product_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;
    
# C_Order
ALTER TABLE C_Order
ADD CONSTRAINT C_Order_C_Id_Fk
  FOREIGN KEY (C_Id) REFERENCES Customer(Customer_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
ADD CONSTRAINT C_Order_P_Id_Fk
  FOREIGN KEY (P_Id) REFERENCES Product(Product_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
ADD CONSTRAINT C_Order_Order_No_Fk
  FOREIGN KEY (Order_No) REFERENCES Orders(Order_Number)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;
    
# review
ALTER TABLE Review
ADD CONSTRAINT Review_C_Id_Fk
  FOREIGN KEY (C_Id) REFERENCES Customer(Customer_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
ADD CONSTRAINT Review_P_Id_Fk
  FOREIGN KEY (P_Id) REFERENCES Product(Product_Id)
	ON DELETE RESTRICT
	ON UPDATE CASCADE;
    

