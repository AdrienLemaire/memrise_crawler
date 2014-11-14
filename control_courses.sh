#!/bin/zsh
# Small script to drop in ~/bin/, that will scrape and run the stats for you
source ~/.zshrc


PROJECT_DIR=/home/dori/Projects/Personal/
# Go to env
cd ${PROJECT_DIR}memrise_crawler/
workon scrapy

./control_courses.py