#!/usr/bin/env bash
#
# Usage: ./wu.sh [years]
#
# If years is not provided as an argument, a default value of 1 is used.
YEARS=${1:-1}

for airport in `cut -d , -f 1 airport-city-state.csv | tail -n +2`
do
    mkdir -pv wg-csv/$airport
    for dt in `python -c "from datetime import datetime, timedelta; \
        end = datetime(datetime.now().year, 1, 1); \
        print '\n'.join(((end - timedelta(days=day)).strftime('%Y-%m-%d')) \
        for day in range((end - datetime(end.year - $YEARS, end.month, \
            end.day)).days, 0, -1))"`
    do
        URL=`echo $airport $dt \
            | sed 's/\-/ /g' \
            | awk '{printf("https://www.wunderground.com/history/airport/%s/%d/%d/%d/DailyHistory.html?format=1\n", $1, $2, $3, $4)}'`
        echo -n "$airport on $dt... "
        if [[ ! -f wg-csv/$airport/$dt.csv ]] || [[ ! -s wg-csv/$airport/$dt.csv ]]
        then
            sleep 0.25
            curl -s $URL | sed '/./,$!d' | sed 's/<br \/>$//g' > wg-csv/$airport/$dt.csv
            if grep -q "No daily or hourly history data available" \
                wg-csv/$airport/$dt.csv
            then
                rm -f wg-csv/$airport/$dt.csv
                echo "Omitted (bad/no data)"
            else
                echo "Done"
            fi
        else
            echo "Skipped"
        fi
    done
done
