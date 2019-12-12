SELECT 
	s.cik,
    s.sic,
	n.tag,
	n.`value`,
	s.adsh
FROM 
	financial_statements.numbers n
    inner join financial_statements.submissions s
	on s.adsh=n.adsh
WHERE
	(tag='Revenues' or tag='GrossProfit' or tag='OperatingIncomeLoss') and
    fp='FY' and 
	fy='2018' and
    sic between 2000 and 4000;