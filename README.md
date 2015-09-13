# Linux Server Configuration

## Server Connection
ip address: 52.88.157.250
ssh port 2200

## Web application url
http://52.88.157.250

## Software Added to the Server
* apache2
* postgresql
* git
* python-dev
* python-pip
* python-psycopg2
* libpq-dev

## Configuration File Changes
* Created catlog.wsgi file to load the application.py file in Apache
* Had to move the line setting app.secret_key in the application.py file
	to outside the if __name__ == '__main__': block so it would be set.
* Changed the create_engine line in database_setup.py, additems.py, and
	application.py to use the postgresql databse instead of a sqllite file.
* Edited the /etc/ssh/sshd_config file to PermitRootLogin no to restrict
	the root user from logging in with ssh.


## Third Party Resouces Used
* Configure Apache to Run Flask Applications
	http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
* Configuring ufw to allow certain ports and deny others
	https://help.ubuntu.com/community/UFW
* Disable root ssh login
	http://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server
