create view filtered as select locale_airport_icao, date(datetime_local) as day, count(*) as num from observations where time(datetime_local) between time('12:00:00') and time('18:00:00') and (temperature_f is not null and temperature_f >= 42) and (heat_index_f is not null and heat_index_f <= 91) and conditions in ("Clear", "Scattered Clouds", "Partly Cloudy", "Unknown") and (precipitation_in <= 0.1 or precipitation_in is null) and events is null group by locale_airport_icao, day order by locale_airport_icao, day desc;

create view total as select locale_airport_icao, date(datetime_local) as day, count(*) as num from observations where time(datetime_local) between time('12:00:00') and time('18:00:00') and temperature_f is not null and heat_index_f is not null group by locale_airport_icao, day order by locale_airport_icao, day desc;

create view final as select filtered.locale_airport_icao, filtered.day, cast(filtered.num as float) / cast(total.num as float) as percent from filtered, total where filtered.locale_airport_icao = total.locale_airport_icao and filtered.day = total.day and percent >= 0.75;

select locale_airport_icao, count(*) as days from final group by locale_airport_icao order by days desc;