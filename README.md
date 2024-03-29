Tools to interact with Memrise


# Requirements

```Shell
$ mkvirtualenv -p python2.7 scrapy
(scrapy)$ pip install -r requirements.txt
```


# Statistics monitor

Program to crawl the memrise web application and get useful statistics for your
**pinned courses**, like how many reviews will come in the day, etc.


## Run the script


```Shell
(scrapy)$ cd memrise/
(scrapy)$ echo -e "USER=YOUR_USERNAME\nPASSWORD=YOUR_PASSWORD" > local_settings.py
(scrapy)$ scrapy crawl memrise -e memrise_items.json
```


## Use the data

Do whatever you want with the data in the json file.
For example, the `get_stats.py` script will list the number of reviews to come:

![get_stats.py](http://i.imgur.com/rgMy2fF.png)


I wrote a shell command to update the json file and return the stats.
Make sure `~/bin/` is in your PATH, then:
```Shell
$ ln -s /path/to/memrise_stats.sh ~/bin/memrise_stats
$ memrise_stats
```

This will also create a file `/tmp/memrise_global_stats.json`



## Cron job

I also added a daily service to update the json files.
```Shell
$ for f in {memrise.service,memrise.timer};
> do sudo ln -s $file /etc/systemd/user/; done
$ systemctl --user list-timers
NEXT                         LEFT     LAST PASSED UNIT          ACTIVATES
Tue 2014-08-26 00:00:00 JST  12h left n/a  n/a    memrise.timer memrise.service
```

# Download a course

Find the ID of the course you want to download. For example,
`http://www.memrise.com/course/556/jlpt-n2-vocab-9/` has ID 556 as indicated in
the url.
Then run the script:

```Shell
$ ./download_course.py -c 556
```
