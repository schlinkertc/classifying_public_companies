
DELETE FROM 
	financial_statements.presentations
WHERE 
	adsh in 
	(SELECT 
		adsh
	FROM 
		financial_statements.submissions
	WHERE 
		form !='10-K'
	)