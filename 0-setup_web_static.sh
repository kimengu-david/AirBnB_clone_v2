#!/usr/bin/env bash
#sets up a web servers for the deployment of web_static

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Holberton School is cool" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root   /var/www/html;
    server_name _;
    add_header X-Served-By $HOSTNAME;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    error_page 404 /custom_404.html;
    location =  /custom_404.html  {
                root /usr/share/nginx/html;
                internal;
    }

    rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4/$1 permanent;

}" > /etc/nginx/sites-enabled/default

service nginx restart
