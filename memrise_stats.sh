#!/bin/zsh
# Small script to drop in ~/bin/, that will scrape and run the stats for you
source /home/dori/.virtualenvs/scrapy/bin/activate


print "This operation takes about 16seconds depending on your system.
Please be patient"

JSON_FILE=/tmp/memrise_items.json
PROJECT_DIR=/home/dori/Projects/Personal/

if  [[ -e $JSON_FILE ]]
then
    \rm $JSON_FILE
fi

cd ${PROJECT_DIR}memrise_crawler/

# Update json
scrapy crawl memrise -o $JSON_FILE --logfile=/var/log/memrise.log

# Show stats
./get_stats.py $JSON_FILE


if [[ "$1" == "--save-kanji-learnt" ]]
then
    # Update kanji_learnt
    # https://github.com/Fandekasp/kanji_learnt.github.io
    #cp /tmp/memrise_global_stats.json ${PROJECT_DIR}kanji_learnt.github.io/data/
    cd ${PROJECT_DIR}kanji_learnt.github.io/ && gia . && gcm "update memrise global stats" && gp
else
    cd ${PROJECT_DIR}kanji_learnt.github.io/ && gCo data/memrise_global_stats.json
fi


