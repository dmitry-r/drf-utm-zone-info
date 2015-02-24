#!/bin/bash

echo ""
echo "[setup] configure host ..."
sudo sh -c "echo 'osmaxx-environment' > /etc/hostname"
sudo sh -c "echo '' >> /etc/hosts"
sudo sh -c "echo '127.0.0.1 osmaxx.dev' >> /etc/hosts"
sudo sh -c "echo '127.0.0.1 osmaxx-environment' >> /etc/hosts"

echo ""
echo "------------ /etc/hosts ----------"
cat /etc/hosts
echo "----------------------------------"

# prevent error message: "dpkg-reconfigure: unable to re-open stdin: No file or directory"
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales


echo ""
echo "[setup] install software and clean up ..."
sudo apt-get update
sudo apt-get -y install rsync git git-flow
sudo apt-get -y autoremove


echo ""
echo "[setup] install python, tools and django ..."
sudo apt-get -y install python3 python3-doc python3-setuptools python3-pip python-dev libpq-dev
sudo pip3 install virtualenv


echo ""
echo "[setup] install postgresql and python driver ..."
sudo apt-get -y install postgresql postgresql-client
sudo apt-get -y install postgis osmctools apache2
sudo apt-get -y install python3-psycopg2


echo""
echo "[setup] install webserver ..."
sudo apt-get -y install apache2 apache2-utils libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo sh -c "echo 'ServerName localhost' >> /etc/apache2/apache2.conf"
sudo service apache2 restart


echo ""
echo "[setup] configure database ..."
sudo -u postgres psql -c "CREATE USER osmaxx WITH PASSWORD 'osmaxx';"
sudo -u postgres psql -c "CREATE DATABASE osmaxx;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE osmaxx TO osmaxx;"
echo "------------ available databases ------------"
sudo -u postgres psql -c "SELECT datname FROM pg_database WHERE datistemplate = false;"
echo "---------------------------------------------"


echo ""
echo "[setup] setup application ..."
cd /var/www
if [ ! -d "eda" ]; then
	mkdir "eda"
fi
cd "eda"
if [ ! -d "projects" ]; then
	mkdir "projects"
fi

virtualenv-3.4 environment
sudo chown -R vagrant:www-data environment
source environment/bin/activate
pip3 install psycopg2
pip3 install django
#django-admin.py startproject osmaxx projects

sudo cp /vagrant/osmaxx.vhost /etc/apache2/sites-available/osmaxx.conf
sudo ln -s /etc/apache2/sites-available/osmaxx.conf /etc/apache2/sites-enabled/osmaxx.conf
sudo a2ensite osmaxx
service apache2 restart

echo ""
echo ".----------------------------------------------------------------------."
echo "|                                                                      |"
echo "|   The vagrant box should be created successfully.                    |"
echo "|   Please add 'osmaxx.dev localhost' to your local /etc/hosts file    |"
echo "|   Open 'osmaxx.dev:{applicationPort}' with a browser                 |"
echo "|                                                                      |"
echo "'----------------------------------------------------------------------'"