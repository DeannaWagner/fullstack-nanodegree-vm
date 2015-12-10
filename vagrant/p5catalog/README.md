#Project5: Linux Server Configuration
#####Deanna M. Wagner, December 7, 2015

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

##TODO
The complete URL to your hosted web application.  LOOK AT RUBRIC FOR MORE ON ALL THIS

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
*



##Software Installation & Configuration Summary

1.  *Launch Virtual Machine (VM)* with Udacity account and login by following:
    https://www.udacity.com/account#!/development_environment  	
2.  `adduser deanna`, set user password, grant this user sudo permissions,
    grant ownership of a created directory /deanna which contains
    .ssh/authorized_keys. 
3.  `adduser grader`, set grader password, grant this user sudo permissions,
    grant ownership of a created directory /grader which contains
    .ssh/authorized_keys.
4.  Update and upgrade all currently installed packages with `apt-get update` and
    `apt-get upgrade`.
5.  Configure the local timezone to UTC with `sudo timedatectl set-timezone UTC`.
6.  Configure Uncomplicated Firewall (ufw) to `default deny incoming`, 
    `default allow outgoing`, `allow ssh`, `allow 2200/tcp`, `allow www`, `allow ntp`, 
    `ufw enable`, nano /etc/ssh/sshd_config to edit port and disallow password authorization, service ssh restart.
7.  Install Apache by sudo apt-get install apache2 
8.  Install Configure Apache to handle mod-wsgi with apt-get install libapache2-mod-wsgi and editing the /etc/apache2/sites-enabled/000-default.conf file by add the following line at the end of the <VirtualHost *:80> block, right before the closing </VirtualHost> line: WSGIScriptAlias / /var/www/html/myapp.wsgi, restart Apache with the sudo apache2ctl restart command.
9. Install PostgreSQL with `sudo apt-get install postgresql`
10. Disable root login on ssh by editing /etc/ssh/sshd_config to `PermitRootLogin no`
12. `sudo su postgres`, then `createuser catalog, psql \password cVGy7`
13. psql `createdb fitcollection` \q
14. `sudo apt-get install postgresql-contrib`
15. sudo su postgres, psql, grant all on database fitcollection to catalog **TODO change permeissions to CREUD**


###TODO

10. Install git, clone and setup your Catalog App project so that it functions
correctly when visiting your server’s IP address in a browser. Remember to set
this up appropriately so that your .git directory is not publicly accessible via
a browser!  (.git on server means you cand do a chmod to be read only by you)

11.    Your Amazon EC2 Instance's public URL will look something like this: http://ec2-XX-XX-XXX-XXX.us-west-2.compute.amazonaws.com/ where the X's are
replaced with your instance's IP address. You can use this url when configuring
third party authentication.

12. install any dependencies like these or other imports:

source venv/bin/activate
pip install httplib2
pip install requests
sudo pip install --upgrade oauth2client
sudo pip install sqlalchemy
pip install Flask-SQLAlchemy
sudo apt-get install python-psycopg2

##Extra Credit Description

This project includes some features that exceed specifications:

###TODO

1.  The firewall has been configured to monitor for repeat unsuccessful login
    attempts and appropriately bans attackers; cron scripts have been included 
    to automatically manage package updates.

2.  The VM includes monitoring applications that provide automated feedback on
    application availability status and/or system security alerts.


##Miscellaneous

Some credit is rightfully due and offered to the supporting courses instructors
for help remembering and learning new linux commands.  These pages were 
instrumental in configuring PostgreSQL on Linux:
https://help.ubuntu.com/community/PostgreSQL
https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps--2

##License

