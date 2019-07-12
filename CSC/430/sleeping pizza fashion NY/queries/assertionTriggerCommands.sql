# Assertion & Triggers - 1 assertion and 1 trigger
USE spfny;

# Assertion -- MySQL does not support Assertions, but we can use Triggers instead
DELIMITER $$
CREATE Trigger Card_Expr_Check
BEFORE INSERT ON customer
FOR EACH ROW
BEGIN
	DECLARE MSG VARCHAR(255);
	IF NEW.customer.Card_Exp_Date < DATE_FORMAT(DATE(NOW()), '%d%y') # if the card has expired <-- done by checking current month and year
	THEN
    SET MSG = 'Card has expired. Please provide a valid card.';
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = MSG;
    END IF;
END$$
DELIMITER ;


# Trigger -- after a customer has ordered something, decrease the stock
DELIMITER $$
CREATE Trigger Reduce_Stock_After_Purchase
AFTER INSERT ON NEW.c_order 
FOR EACH ROW
BEGIN
	SET No_in_stock = (SELECT No_in_stock - 1
						FROM product, c_order
						WHERE Product_Id = NEW.P_Id);
END$$
DELIMITER ;
