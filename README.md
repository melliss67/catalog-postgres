# Linux Server Configuration

## Server Connection
ip address: 52.27.29.183
ssh port 2200

## Web application url
http://ec2-52-27-29-183.us-west-2.compute.amazonaws.com

## Software Added to the Server
* apache2
* postgresql
* libapache2-mod-wsgi
* git
* python-dev
* python-pip
* python-psycopg2
* libpq-dev
* Python Packages
 * httplib2
 * sqlalchemy
 * Flask
 * oauth2client
 * xmlify
 * dict2xml

## Configuration File Changes
* Changed sshd_config file as follows
 * changed Port from 22 to 2200
 * changed PermitRootLogin to no
* Created catalog.wsgi file to load the application.py file in Apache
* Had to move the line setting app.secret_key in the application.py file
	to outside the `if __name__ == '__main__':` block so it would be set.
* Changed the create_engine line in database_setup.py, additems.py, and
	application.py to use the postgresql databse instead of a sqllite file.
* Edited the /etc/ssh/sshd_config file to PermitRootLogin no to restrict
	the root user from logging in with ssh.
* Added the lines below to the /etc/apache2/sites-enabled/000-default.conf file
	to enable WSGI
```
    WSGIDaemonProcess application user=www-data group=www-data threads=5
    WSGIScriptAlias / /var/www/html/catalog-postgres/catalog.wsgi

    <Directory /var/www/html/catalog-postgres>
           WSGIProcessGroup application
           WSGIApplicationGroup %{GLOBAL}
           Order deny,allow
           Allow from all
    </Directory>
```


## Third Party Resouces Used
* Configring firewall
	https://help.ubuntu.com/community/UFW
* Configure Apache to Run Flask Applications
	http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
* Configuring ufw to allow certain ports and deny others
	https://help.ubuntu.com/community/UFW
* Disable root ssh login
	http://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server
* Conecting to a postgres database with Flask
	https://pythonhosted.org/Flask-SQLAlchemy/config.html
