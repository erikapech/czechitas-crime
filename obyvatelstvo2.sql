SELECT *
FROM
	obyvatelstvo

;WITH pocet_deti_kraj AS
	(
	SELECT
		k.id_kraj, o.datum, SUM(pocet_obyvatel) AS pocet_deti
	FROM
		obyvatelstvo o
		JOIN kraj k ON o.kraj = k.id_kraj
	WHERE 
		o.vek < 18
	GROUP BY
		k.id_kraj, o.datum

	)
SELECT
	k.kraj,
	k.datum,
	pocet_deti
	--SUM(k.objasneno_spachano_detmi) AS spachano_detmi, 
	--SUM(pdk.pocet_deti)/12 AS pocet_deti
	--SUM(k.objasneno_spachano_detmi) / SUM(pdk.pocet_deti) * 100000 AS koeficient_100000
FROM
	kriminalita k
	JOIN pocet_deti_kraj pdk ON k.kraj = pdk.id_kraj AND k.datum = pdk.datum
	JOIN ciselnik_4_uroven c4 ON k.id_cin =c4.kod_trestny_cin 
--GROUP BY
	--k.kraj, k.datum
ORDER BY
	k.datum,
	k.kraj

CREATE OR ALTER VIEW w_pocet_deti AS
	SELECT
		o.kraj, o.datum, SUM(pocet_obyvatel) AS pocet_deti
	FROM
		obyvatelstvo o
		
	WHERE 
		o.vek < 18
	GROUP BY
		o.kraj, o.datum
;

CREATE OR ALTER VIEW w_kriminalita_deti AS
	SELECT
		kraj, datum, SUM(objasneno_spachano_detmi) AS spachano_deti
	FROM
		kriminalita
	GROUP BY
		kraj, datum

CREATE OR ALTER VIEW w_spachano_detmi_koeficient AS
	SELECT
		kd.kraj, kd.datum, kd.spachano_deti, pd.pocet_deti, kd.spachano_deti / pd.pocet_deti * 100000 AS spachano_koeficient_100000
	FROM
		w_kriminalita_deti kd
		JOIN w_pocet_deti  pd ON kd.kraj = pd.kraj AND kd.datum = pd.datum
	
-- prumer koeficientu
SELECT
	DATEPART(YEAR, datum) AS year, kraj, AVG(spachano_koeficient_100000)
FROM
	w_spachano_detmi_koeficient
GROUP BY
	DATEPART(YEAR, datum), kraj
ORDER BY
	year

SELECT 
	datum, kraj, pocet_deti
FROM 
	w_pocet_deti
ORDER BY
datum, kraj

-- výpoèet poètu obyvatel
CREATE OR ALTER VIEW w_pocet_obyvatel AS
	SELECT
		o.kraj, o.datum, SUM(pocet_obyvatel) AS pocet_obyvatel
	FROM
		obyvatelstvo o
	GROUP BY
		o.kraj, o.datum

SELECT 
	DATEPART(YEAR, datum) as rok, SUM(pocet_obyvatel) / 12
FROM 
	w_pocet_obyvatel
GROUP BY
	DATEPART(YEAR, datum)
ORDER BY
 rok