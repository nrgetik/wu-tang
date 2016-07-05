#!/usr/bin/env bash

YEARS=1

for airport in `cat airports.txt`
do
    mkdir -pv csv/$airport
    for dt in `python -c "from datetime import datetime, timedelta; print \
        '\n'.join(((datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')) \
        for day in range($YEARS * 365, 0, -1))"`
    do
        URL=`echo $airport $dt \
            | sed 's/\-/ /g' \
            | awk '{printf("https://www.wunderground.com/history/airport/%s/%d/%d/%d/DailyHistory.html?format=1\n", $1, $2, $3, $4)}'`
        if [[ ! -f csv/$airport/$dt.csv ]]
        then
            sleep 1
            curl -s $URL | sed 's/<br \/>$//g' > csv/$airport/$dt.csv
        fi
    done
done
