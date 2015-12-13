#Project5: Linux Server Configuration
#####Deanna M. Wagner, December 13, 2015

A Flask web application* has been deployed on a Udacity provided virtual 
server in Amazon Web Services’s Elastic Compute Cloud (EC2), which has been
configured to serve a PostgreSQL database and an Apache mod-wsgi server.

*The Item Catalog Application is implemented as an informational app which 
catalogs exercises based on their type to encourage people to engage in physical 
activity more often.  Since the categories represent the basic list of what an
exercise program should contain, no creating, editing or deleting of categories
is included.  Each category has a name, description and an image associated with
it.  Authorized, logged in users may create an exercise item.  These users may
edit and/or delete exercises that they themselves created.  The site contains
introductory information and a disclaimer concerning the terms of use of this
web app.  Visitors might compile an exercise program by choosing from each
category in order one or more exercise choices.

##Connection Information
The server IP address is 52.25.243.158 and the SSH port is 2200
The complete URL to your hosted web application http://ec2-52-25-243-158.us-west-2.compute.amazonaws.com/.  

##Required Libraries, Files and Dependencies

*  Python
*  PostreSQL, psychopg2 and psql
*  SQLAlchemy
*  Flask
*  bleach
*  flask-seasurf
*  oauth2client
*  json
*  dict2xml
*  httplib2
*  `application.py`
*  `db_setup.py`
*  `db_populate.py`
*  `templates/super.html`
*  `templates/main.html`
*  `templates/cat_items.html`
*  `templates/create_items.html`
*  `templates/edit_items.html`
*  `templates/delete_items.html`
*  `templates/404.html`
*  `static/FC.css`
*  `static/images` which contains many image files


##Software Installation & Configuration Summary

#####Launch Virtual Machine (VM) and set up user accounts
*   Access Udacity account and login by following:
    https://www.udacity.com/account#!/development_environment  	
*   As root `adduser deanna`, set user password, grant sudo permissions by
    `nano /etc/sudoers.d/deanna` and
    `deanna ALL=(ALL) NOPASSWD:ALL`,
    `mkdir /home/deanna/.ssh`, `chown deanna:deanna /home/deanna/.ssh`,
    `chmod 700 /home/deanna/.ssh`
    `cp /root/.ssh/authorized_keys /home/deanna/.ssh`. 
*   `adduser grader`, set grader password, grant sudo permissions by
    `nano /etc/sudoers.d/grader` and
    `grader ALL=(ALL) NOPASSWD:ALL`,
    `mkdir /home/grader/.ssh`, `chown grader:grader /home/grader/.ssh`,
    `chmod 700 /home/grader/.ssh`
    `exit`, `ssh-keygen` and follow steps with passphrase the same for grader
    as user pw, copy contents of public key, ssh into server,
    `nano /home/grader/.ssh/authorized_keys`, paste contents of public key,
    exit and save file.  `chmod 644 /home/grader/.ssh/authorized_keys`
    exit server and login as user deanna for all subsequent tasks
    
#####Update & Upgrade
*   Update and upgrade all currently installed packages with `sudo apt-get update` and
    `sudo apt-get upgrade`.
*   Configure the local timezone to UTC with `sudo timedatectl set-timezone UTC`.

#####Configure Uncomplicated Firewall (ufw)& SSH
*   `default deny incoming`, `default allow outgoing`, `allow ssh`,
    `allow 2200/tcp`, `allow www`, `allow ntp`, `ufw enable`,
    `nano /etc/ssh/sshd_config` to edit port and disallow password authorization,
*  Disable root login on ssh by editing /etc/ssh/sshd_config to `PermitRootLogin no`
    `sudo service ssh restart`.
    
#####Install & Configure Apache
*  Install Apache `sudo apt-get install apache2` to handle mod-wsgi with
  `apt-get install libapache2-mod-wsgi` and editing
  /etc/apache2/sites-enabled/000-default.conf:
 * <VirtualHost *:80>
 *   
 *   WSGIDaemonProcess catalog user=deanna group=deanna threads=5
 *   WSGIScriptAlias / /var/www/catalog/catalog.wsgi
 *   <Directory /var/www/catalog>
 *       WSGIProcessGroup catalog
 *       WSGIApplicationGroup %{GLOBAL}
 *       Order deny,allow
 *       Allow from all
 *   \<\/Directory>
 *  \<\/VirtualHost> 

Restart Apache with the sudo apache2ctl restart command.
Create a /var/www/catalog/catalog.wsgi file and add the following:

*	import sys
*	import logging
*	logging.basicConfig(stream=sys.stderr)
*	sys.path.insert(0, '/var/www/catalog/')
*	from catalog import app as application
*	application.secret_key = '<secret key>'
*	application.debug = True
*	csrf = SeaSurf(application)

#####Install & Configure PostgreSQL
*  Install PostgreSQL with `sudo apt-get install postgresql`
  `sudo su postgres`, then `createuser catalog, psql \password cVGy7`
  `psql` `createdb fitcollection;` `\q`
  `sudo apt-get install postgresql-contrib`, `sudo su postgres`, `psql`,
  grant all on database fitcollection to catalog and exit shell of postgres user

#####Install Catalog Item Application & Dependencies
*  Changed connection strings in py files to point to new server, install git with
  `sudo apt-get install git`, 
  `git clone https://github.com/DeannaWagner/fullstack-nanodegree-vm.git fullstack`,
  `chmod 500 .git`, `sudo cp -r fullstack/vagrant/p5catalog /var/www`,
  `sudo mv /var/www/p5catalog/ catalog`, `sudo mv /var/www/catalog/application/py catalog/py`
  `sudo apt-get install python-pip`, `sudo apt-get install python-psycopg2`
  `sudo pip install httplib2`, `sudo pip install flask`, `sudo pip install --upgrade oauth2client`,
  `sudo pip install sqlalchemy`, `sudo pip install flask-seasurf`, 
  `sudo pip install dict2xml`, `sudo pip install bleach`


##Extra Credit Description

#####Firewall has been configured to monitor for brute force attacks
*  The firewall has been configured to monitor for repeat unsuccessful login
    attempts and appropriately bans attackers; 
     sudo apt-get install fail2ban, looked at config file
     sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
 sudo nano /etc/fail2ban/jail.local
 sudo fail2ban-client status
Status
|- Number of jail:      1
`- Jail list:           ssh

#####Cron scripts have been included to automatically manage package updates.
*  `sudo bash`, `crontab -e`, select option 2 from prompt, enter:
  `0 5 * * * /root/upgrade.py` to configure cron, `nano /root/upgrade.py`
Added commands found from link below and adjusted to update and then upgrade
http://stackoverflow.com/questions/89228/calling-an-external-command-in-python
`chmod 775 /root/upgrade.py`


#####VM includes monitoring applications that provide automated feedback
*  Application availability status and/or system security alerts monitoring.
  `sudo  apt-get install glances`, `sudo apt-get install python-dev`,
  `sudo pip install --upgrade psutil`, `sudo glances`

##Miscellaneous

Some credit is rightfully due and offered to the supporting courses instructors
and Udacians in the discussion forums for help remembering and learning new
linux commands.  These pages were instrumental in configuration of PostgreSQL &
Fail2Ban
https://help.ubuntu.com/community/PostgreSQL
https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2
https://www.digitalocean.com/community/tutorials/how-to-protect-an-apache-server-with-fail2ban-on-ubuntu-14-04

##License

[MIT](https://opensource.org/licenses/MIT)
