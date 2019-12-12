-- SELECT
-- 	s.adsh, s.cik, 
--     s.`name`, s.fp, s.fy, s.form,
--     s.sic
-- FROM 
-- 	financial_statements.submissions s
-- WHERE 
-- 	s.sic BETWEEN 6000 and 9000
-- GROUP BY 
-- 	s.sic;
--     
SELECT 
    p.tag,
    count(*) tag
FROM
	financial_statements.presentations p
WHERE
	stmt = 'IS' AND
    inpth = 0
GROUP BY 
	tag
ORDER BY 
	tag DESC
LIMIT 
	20;

