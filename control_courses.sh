#!/bin/zsh
# Small script to drop in ~/bin/, that will scrape and run the stats for you
source /home/dori/.virtualenvs/scrapy/bin/activate

PROJECT_DIR=/home/dori/Projects/Personal/
# Go to env
cd ${PROJECT_DIR}memrise_crawler/

./control_courses.py

su - dori -c "cd ${PROJECT_DIR}memrise_crawler/ && git add . && git commit -m 'update backup' && git push"
