#!/usr/bin/env bash
#
# Usage: ./wu.sh [years]
#
# If years is not provided as an argument, a default value of 1 is used.
YEARS=${1:-1}

for airport in `cat airports.txt`
do
    mkdir -pv csv/$airport
    for dt in `python -c "from datetime import datetime, timedelta; \
        now = datetime.now(); \
        print '\n'.join(((now - timedelta(days=day)).strftime('%Y-%m-%d')) \
        for day in range((now - datetime(now.year - $YEARS, now.month, \
            now.day)).days, 0, -1))"`
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
