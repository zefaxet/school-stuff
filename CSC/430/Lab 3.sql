-- Write a trigger to create a default department location in Houston every time new department is inserted into database.
DELIMITER $$
CREATE TRIGGER DEFAULT_DEPT_LOCATION_TRIG
AFTER INSERT ON DEPARTMENT
FOR EACH ROW
BEGIN
	INSERT INTO DEPT_LOCATIONS
		VALUES(NEW.DNumber, 'Houston');
END$$
DELIMITER ;

-- Write a trigger to enforce following constraint: employee salary must not be higher than the salary of 
-- his/her direct supervisor. If it is, then display message –
-- “Supervisee salary is higher than supervisor salary."
DELIMITER $$
CREATE TRIGGER SALARY_CONTSR_TRIG
BEFORE INSERT ON EMPLOYEE
FOR EACH ROW
BEGIN
	DECLARE MSG TEXT;
	IF NEW.Salary > (SELECT Salary
						FROM EMPLOYEE
						WHERE SSN = NEW.Super_SSN)
	THEN
	SET MSG = 'Supervisee salary is higher than supervisor salary.';
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = MSG;
	END IF;
END$$
DELIMITER ;

-- Write a trigger to update supervisor SSN of an employee with the SSN of the department manager
-- where he/she works BEFORE INSERT(ing) the record into employee table IF the supervisor SSN
-- attribute is empty or NULL.
DELIMITER $$
CREATE TRIGGER SNN_CONSTR_TRIG
BEFORE INSERT ON EMPLOYEE
FOR EACH ROW
BEGIN
	IF (NEW.Super_SSN = '' OR NEW.Super_SSN IS NULL)
	THEN
	SET NEW.Super_SSN = (SELECT Mgr_SSN
							FROM DEPARTMENT
							WHERE DNumber = NEW.DNo);
	END IF;
END$$
DELIMITER ;

-- Create a view that displays first name, last name, SSN, salary, department name and department
-- number for each department manager.
CREATE VIEW DEPT_MANAGER
AS SELECT FName, LName, SSN, Salary, DNo -- maybe also DNumber, there is no uniqueness contraint for DNo of department managers
	FROM DEPARTMENT JOIN EMPLOYEE ON ESSN = SSN;
	
-- Create a view that displays project number, project name, controlling department number,
-- controlling department name, total number of employees, total salary paid, and total hours
-- worked for each project.
CREATE VIEW PROJECT_INFO(PNo, PName, DNo, DName, Num_Emps, Total_Sal, Total_Hrs)
AS SELECT PNumber, PName, DNum, DName, COUNT(SSN), SUM(Salary), SUM(Hours)
	FROM ((PROJECT JOIN (WORKS_ON JOIN EMPLOYEE ON ESSN = SSN) ON PNumber = PNo) JOIN DEPARTMENT ON DNum = DNumber),
	GROUP BY PNumber, PName;