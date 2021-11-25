
;WITH w_nezamestnanost AS
(
	SELECT 
		kodNuts3, 
		SUM(dosazitelniUchazeci15_64) AS celkem_uchazeci, 
		SUM(celkemObyvatelstvo15_64) AS celkem_obyvatelstvo
	
	FROM
		nezamestnanost
	--GROUP BY 
		--datum, kodNuts3
	WHERE
		datum = '2019-12-31'
	GROUP BY
		kodNuts3
)

SELECT kodNuts3, CAST(celkem_uchazeci AS float) / celkem_obyvatelstvo * 100 AS mira_nezamestnanosti
FROM
	w_nezamestnanost


SELECT
	*
FROM
	nezamestnanost
ORDER BY
	datum