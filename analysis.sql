CREATE VIEW filtered AS
SELECT locale_airport_icao, date(datetime_local) AS day, count(*) AS num
FROM observations
WHERE time(datetime_local) BETWEEN time('12:00:00') AND time('18:00:00') AND
(temperature_f IS NOT NULL AND temperature_f >= 50.0) AND (heat_index_f IS NOT
    NULL AND heat_index_f < 91.0) AND conditions IN ('Clear') AND
(precipitation_in <= 0.1 OR precipitation_in IS NULL) AND events IS NULL
GROUP BY locale_airport_icao, day
ORDER BY locale_airport_icao, day DESC;

CREATE VIEW total AS
SELECT locale_airport_icao, date(datetime_local) AS day, count(*) AS num
FROM observations
WHERE time(datetime_local) BETWEEN time('12:00:00') AND time('18:00:00') AND
temperature_f IS NOT NULL and heat_index_f IS NOT NULL AND conditions NOT IN
('Unknown')
GROUP BY locale_airport_icao, day
ORDER BY locale_airport_icao, day DESC;

CREATE VIEW final AS
SELECT filtered.locale_airport_icao, filtered.day, (cast(filtered.num AS float)
    / cast(total.num AS float)) AS percent
FROM filtered, total
WHERE filtered.locale_airport_icao = total.locale_airport_icao AND filtered.day
= total.day AND percent >= cast((2.0 / 3.0) AS float);
GROUP BY filtered.locale_airport_icao, filtered.day
ORDER BY filtered.locale_airport_icao, filtered.day DESC;

SELECT locale_airport_icao, count(*) AS days
FROM final
GROUP BY locale_airport_icao
ORDER BY days DESC;
