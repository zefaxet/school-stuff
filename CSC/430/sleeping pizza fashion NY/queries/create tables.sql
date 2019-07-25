#CREATE DATABASE SPFNY;
USE SPFNY;

DROP TABLE Customer, Product, Tops, Bottoms, Shoes, Orders, Designer, Review, C_Order, Top_Type, Bottom_Type, Shoe_Type;

CREATE TABLE Customer (
	Customer_Id			INT(32)			NOT NULL		AUTO_INCREMENT,	# went ahead and made this auto incrementing to save time
    Username			VARCHAR(32)		NOT NULL,
    Password			VARCHAR(256)	NOT NULL,
    Card_Number			BIGINT(16)		UNSIGNED, # Changed to BIGINT to support 16 digits
    Card_Exp_Date		DATE,
    CCV					SMALLINT(3)		UNSIGNED, # Changed to SMALLINT which the smallest data type that supports 3 digits
    Street				VARCHAR(32),
    City				VARCHAR(32),
    State				VARCHAR(16),
    Zip_Code			INT(16),
    PRIMARY KEY (Customer_Id)
);

CREATE TABLE Product (
	Product_Id			INT	UNSIGNED	NOT NULL		AUTO_INCREMENT, # changed to int so it can auto increment
    Product_Name		VARCHAR(64)		NOT NULL, # Increased field size because my names were too long
    Product_Price		DECIMAL(6, 2)	UNSIGNED, # changed so that it only stores two floating point places
    Product_Desc		VARCHAR(512),
    No_in_stock			INT				UNSIGNED,
    On_Sale				BOOL,
	D_Id				INT(8),
    PRIMARY KEY (Product_Id)
);

CREATE TABLE Tops (
	P_Id				INT UNSIGNED 	NOT NULL, # changed to reflect product
    Top_Type			VARCHAR(16),
    Top_Size			INT,
    PRIMARY KEY (P_Id)
);

CREATE TABLE Bottoms (
	P_Id				INT UNSIGNED	NOT NULL, # changed to reflect product
    Bottom_Type			VARCHAR(16),
    Bottom_Size			INT,
    PRIMARY KEY (P_Id)
);

CREATE TABLE Shoes (
	P_Id				INT UNSIGNED	NOT NULL, # changed to reflect product
    Shoe_Type			VARCHAR(16),
    Shoe_Size			INT,
    PRIMARY KEY (P_Id)
);

CREATE TABLE Orders (
	C_Id				INT(32)			NOT NULL, # changed to reflect customer
    P_Id				INT UNSIGNED	NOT NULL, # changed to reflect product
    Order_Number		INT	UNSIGNED	NOT NULL UNIQUE	AUTO_INCREMENT, # no reason to keep sign, and can auto increment
    Order_Date			DATE,
    PRIMARY KEY (C_Id, P_Id, Order_Number)
);

CREATE TABLE Designer (
	Designer_Id			INT(8)			NOT NULL	AUTO_INCREMENT,
    Designer_Name		VARCHAR(32)		NOT NULL,
    PRIMARY KEY (Designer_Id)
);

CREATE TABLE Review (
	C_Id				INT(32)			NOT NULL, # changed to reflect customer
    P_Id				INT UNSIGNED	NOT NULL, # changed to reflect product
    Review_Subject		VARCHAR(64), # was not long enough for reasonable subject
    Review_Rating		TINYINT(1) UNSIGNED, #Only needs one digit for 5 star review
    Review_Date			DATE,
    PRIMARY KEY (C_Id, P_Id)
);

CREATE TABLE C_Order (
	C_Id				INT(32)			NOT NULL, # changed to reflect customer
    P_Id				INT UNSIGNED	NOT NULL, # changed to reflect product
    Order_No			INT	UNSIGNED	NOT NULL, # changed to reflect orders
    PRIMARY KEY (C_Id, P_Id, Order_No)
);


CREATE TABLE Top_Type (
	P_Id				VARCHAR(8)		NOT NULL,
    T_Type				VARCHAR(16)		NOT NULL,
    PRIMARY KEY (P_Id, T_Type)
);

CREATE TABLE Bottom_Type (
	P_Id				VARCHAR(8)		NOT NULL,
    B_Type				VARCHAR(16)		NOT NULL,
    PRIMARY KEY (P_Id, B_Type)
);

CREATE TABLE Shoe_Type (
	P_Id				VARCHAR(8)		NOT NULL,
    S_Type				VARCHAR(16)		NOT NULL,
    PRIMARY KEY (P_Id, S_Type)
);