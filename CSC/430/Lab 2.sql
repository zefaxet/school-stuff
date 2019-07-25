-- Retrieve first name and last name of employees who have a birthday in January.
SELECT FName, LName
FROM EMPLOYEE
WHERE BDate LIKE '____-01-__';

--Show the resulting salaries if every employee working on the ‘ProductX’ project with a salary between 
--$20000 and $40000 is given a 15% raise.
SELECT FName, LName, 1.15 * Salary AS Increased_Salary
FROM (EMPLOYEE JOIN (WORKS_ON JOIN PROJECT ON PNo = PNumber) ON SSN = ESSN)
WHERE PName = 'ProductX' and Salary BETWEEN 20000 AND 40000;

--List first name, last name and SSN of employees whose salary is less than the salary of any of the
--employees in department 4.
SELECT FName, LName, SSN
FROM EMPLOYEE
WHERE Salary < ANY (SELECT Salary
					FROM EMPLOYEE
					WHERE DNo = 4);

--Retrieve SSNs of all female employees who work on project numbers 10, 20, or 30.
SELECT DISTINCT SSN
FROM EMPLOYEE
	JOIN WORKS_ON
	ON SSN = ESSN
WHERE Sex = 'F' AND PNo IN (10, 20, 30);

--For each project on which less than three employees work, retrieve the project number,
--the project name, and the average salary of employees who work on the project.
SELECT PName, PNumber, AVG(Salary) AS Average_Salary
FROM PROJECT
	JOIN (WORKS_ON
		JOIN EMPLOYEE
		ON ESSN = SSN)
	ON Pno = PNumber
GROUP BY PName, PNumber
HAVING COUNT(SSN) < 3;