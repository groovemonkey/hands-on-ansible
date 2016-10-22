#!/usr/bin/env bash

# from http://docs.mattermost.com/install/prod-ubuntu.html


###########################
##### 1: Database Setup
###########################
sudo apt-get install postgresql postgresql-contrib

sudo -i -u postgres
psql
CREATE DATABASE mattermost;
CREATE USER mmuser WITH PASSWORD 'mmuser_password';
GRANT ALL PRIVILEGES ON DATABASE mattermost to mmuser;
\q
exit



# If you are using a separate app server, use the AWS VPC address or DNS to allow connections from it.
# sudo vi /etc/postgresql/$PG_VERSION/main/postgresql.conf

# sudo vi /etc/postgresql/9.5/main/pg_hba.conf
# IPv4 local connections --> 10.10.10.2/32 md5

sudo /etc/init.d/postgresql reload
(or)
sudo systemctl reload postgresql

# if you're using a separate app server...try connecting from it
psql --host=10.10.10.1 --dbname=mattermost --username=mmuser



###########################
##### 2: Mattermost Setup
###########################

adduser mattermost
su - mattermost

# Download the application
LATEST_MM_VERSION="3.3.0"
wget https://releases.mattermost.com/${LATEST_MM_VERSION}/mattermost-team-${LATEST_MM_VERSION}-linux-amd64.tar.gz
tar -xzf mattermost-team-${LATEST_MM_VERSION}-linux-amd64.tar.gz

# rename and create 'data' directory
mv mattermost mattermost_app
mkdir -p mattermost_app/data


vim mattermost_app/config/config.json
    replace DriverName": "mysql" with DriverName": "postgres"
    # do we need to change this to a unix socket? Maybe not a bad idea.
    replace "DataSource": "postgres://mmuser:mmuser_password@localhost:5432/mattermost?sslmode=disable&connect_timeout=10"

# test running the application (ctrl-c to kill)
cd ~/mattermost_app/bin
./platform


# create systemd file
vim /etc/systemd/system/mattermost.service

# add the following content
[Unit]
Description=Mattermost
After=syslog.target network.target

[Service]
Type=simple
WorkingDirectory=/home/mattermost/mattermost_app/bin
User=mattermost
ExecStart=/home/mattermost/mattermost_app/bin/platform
PIDFile=/var/spool/mattermost/pid/master.pid
Requires=

[Install]
WantedBy=multi-user.target



# reload systemctl daemons to discover this service
systemctl daemon-reload

# verify
systemctl start mattermost.service
systemctl status mattermost.service

# enable at boot time
systemctl enable mattermost.service





###########################
##### 3: Nginx Setup
###########################

# install nginx from the official PPA
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update
sudo apt-get install nginx


# configure nginx -- make sure vhosts are loaded from /etc/nginx/conf.d/
vim /etc/nginx/nginx.conf


# add the mattermost vhost (have nginx proxy for mattermost on port 80)
vim /etc/nginx/sites-available/mattermost
YOURDOMAIN=tutorialinux.com

server {
    server_name mattermost.${YOURDOMAIN}.com;
    location / {
        client_max_body_size 50M;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Frame-Options SAMEORIGIN;
        proxy_pass http://127.0.0.1:8065;
    }
}



# remove default vhost
sudo rm /etc/nginx/sites-enabled/default

# enable site
ln -s /etc/nginx/sites-available/mattermost /etc/nginx/sites-enabled/mattermost


# verify, start, enable nginx at boot
systemctl reload nginx
systemctl status nginx
systemctl enable nginx
