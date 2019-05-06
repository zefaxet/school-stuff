-- Retrieve first name and last name of all male employees with salary more than 30000.
SELECT FName, LName
FROM EMPLOYEE
WHERE Sex = 'M' and Salary > 30000;

-- Retrieve locations of Research department projects.
SELECT PLocation
FROM PROJECT;

-- Retrieve first name, last name, and SSN of all employees who work more than 9 hours on project #2.
SELECT FName, SELECT FName, LName, SSN
FROM EMPLOYEE E JOIN WORKS_ON WO ON E.SSN = WO.ESSN
WHERE PNo = 2 and Hours > 9;

-- Retrieve name, date of birth and relationship of all female dependents of employees who work for department #5.
SELECT Dependent_name, D.BDate, Relationship
FROM DEPENDENT D JOIN EMPLOYEE E ON D.ESSN = E.SSN
WHERE D.Sex = 'F' AND E.DNo = 5;

-- Retrieve first name, last name and salary of employees who manage departments with projects located in Houston.
SELECT FName, LName, Salary
FROM PROJECT P JOIN (DEPARTMENT D
	JOIN EMPLOYEE E ON SSN = Mgr_SSN) ON DNum = DNumber
WHERE PLocation = 'Houston';