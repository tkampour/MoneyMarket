# Scrapy settings for xrima project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'xrima'

SPIDER_MODULES = ['xrima.spiders']
NEWSPIDER_MODULE = 'xrima.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0'

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = ['xrima.pipelines.XrimaPipeline']