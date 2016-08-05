SELECT final.locale_airport_icao, count(*) AS days, locales.city, locales.state
FROM locales,
  (SELECT filtered.locale_airport_icao, filtered.day, (cast(filtered.num AS
        float) / cast(total.num AS float)) AS percent
  FROM
    (SELECT locale_airport_icao, date(datetime_local) AS day, count(*) AS num
    FROM observations
    WHERE time(datetime_local) BETWEEN time('12:00:00') AND time('18:00:00')
    AND (temperature_f IS NOT NULL AND temperature_f >= 55.0) AND (heat_index_f
      IS NOT NULL AND heat_index_f < 85.0)
    GROUP BY locale_airport_icao, day) filtered,
    (SELECT locale_airport_icao, date(datetime_local) AS day, count(*) AS num
    FROM observations
    WHERE time(datetime_local) BETWEEN time('12:00:00') AND time('18:00:00')
    AND temperature_f IS NOT NULL and heat_index_f IS NOT NULL
    GROUP BY locale_airport_icao, day) total
  WHERE filtered.locale_airport_icao = total.locale_airport_icao AND
  filtered.day = total.day AND percent >= cast((6.0 / 6.0) AS float)
  GROUP BY filtered.locale_airport_icao, filtered.day) final
WHERE final.locale_airport_icao = locales.airport_icao
GROUP BY final.locale_airport_icao
ORDER BY days DESC;
