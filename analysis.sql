SELECT final.locale_airport_icao, (count(*) / 5) AS days, locales.city,
locales.state
FROM locales,
  (SELECT filtered.locale_airport_icao, filtered.day, (cast(filtered.num AS
        float) / cast(total.num AS float)) AS percent
  FROM
    (SELECT locale_airport_icao, date(datetime_local) AS day, count(*) AS num
    FROM observations
    WHERE (strftime('%m', datetime_local) IN ('04', '05', '06', '07', '08',
        '09') AND time(datetime_local) BETWEEN time('12:00:00') AND
      time('18:00:00') AND (temperature_f IS NOT NULL AND temperature_f >=
        70.0) AND (heat_index_f IS NOT NULL AND heat_index_f <= 80.0)) OR
    (strftime('%m', datetime_local) IN ('01', '02', '03', '10', '11', '12') AND
      time(datetime_local) BETWEEN time('12:00:00') AND time('18:00:00') AND
      (temperature_f IS NOT NULL AND temperature_f BETWEEN 60.0 AND 70.0))
    GROUP BY locale_airport_icao, day) filtered,
    (SELECT locale_airport_icao, date(datetime_local) AS day, count(*) AS num
    FROM observations
    WHERE (strftime('%m', datetime_local) IN ('04', '05', '06', '07', '08',
        '09') AND time(datetime_local) BETWEEN time('12:00:00') AND
      time('18:00:00') AND temperature_f IS NOT NULL AND heat_index_f IS NOT
      NULL) OR (strftime('%m', datetime_local) IN ('01', '02', '03', '10',
        '11', '12') AND time(datetime_local) BETWEEN time('12:00:00') AND
      time('18:00:00') AND temperature_f IS NOT NULL)
    GROUP BY locale_airport_icao, day) total
  WHERE filtered.locale_airport_icao = total.locale_airport_icao AND
  filtered.day = total.day AND percent >= cast((100.0 / 100.0) AS float)
  GROUP BY filtered.locale_airport_icao, filtered.day) final
WHERE final.locale_airport_icao = locales.airport_icao
GROUP BY final.locale_airport_icao
ORDER BY days DESC;
