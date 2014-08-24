# -*- coding: utf-8 -*-

# Scrapy settings for memrise project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'memrise'

SPIDER_MODULES = ['memrise.spiders']
NEWSPIDER_MODULE = 'memrise.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'memrise (+http://www.yourdomain.com)'


USER = ""
PASSWORD = ""

try:
    """
    Make a symbolic link name "local_settings.py" to where settings are stored
    """
    from local_settings import *  # NOQA
except ImportError:
    import warnings
    warnings.warn('You should create a local_settings.py file')
except Exception, e:
    raise Exception(e)
