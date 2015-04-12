sudo pip install simplejson
sudo pip install elasticutils

sudo ln -s /srv/www/xrimatagora.gr/conf/nginx.conf /etc/nginx/nginx.conf
sudo supervisord -c /srv/www/xrimatagora.gr/conf/supervisord2.conf
