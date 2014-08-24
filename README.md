Program to crawl the memrise web application and get useful statistics, like how
many reviews will come in the day, etc.


# Requirements

```Shell
$ mkvirtualenv -p python2.7 scrapy
(scrapy)$ pip install -r requirements.txt
```


# Run the script


```Shell
(scrapy)$ cd memrise/
(scrapy)$ echo -e "USER=YOUR_USERNAME\nPASSWORD=YOUR_PASSWORD" > local_settings.py
(scrapy)$ scrapy crawl memrise -e memrise_items.json
```

# Use the data

Do whatever you want with the data in the json file.
For example, the `get_stats.py` script will list the number of reviews to come:

![get_stats.py](http://i.imgur.com/SaHd6Ix.png)
