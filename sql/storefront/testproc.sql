DELIMITER //

CREATE PROCEDURE GetSomeProducts()
BEGIN
	SELECT id, title FROM store_product where id = 1 or id = 3;
END //

DELIMITER ;