#!/bin/zsh
# Small script to drop in ~/bin/, that will scrape and run the stats for you
source ~/.zshrc

print "This operation takes about 16seconds depending on your system.
Please be patient"

JSON_FILE=/tmp/memrise_items.json
SCRAPY_PROJECT=/home/dori/Projects/Personal/memrise_crawler

if  [[ -e $JSON_FILE ]]
then
    \rm $JSON_FILE
fi

# Go to env
cd $SCRAPY_PROJECT
workon scrapy

# Update json
scrapy crawl memrise -o $JSON_FILE --logfile=/var/log/memrise.log

# Show stats
./get_stats.py $JSON_FILE
