#Project3: Item Catalog Application
#####Deanna M. Wagner, November 13, 2015

The Item Catalog Application has been implemented as an informational app which
catalogs exercises based on their type to encourage people to engage in physical 
activity more often.  Since the categories represent the basic list of what an 
exercise program should contain, no creating, editing or deleting of categories
is included.  Each category has a name, description and an image associated with
it.  Authorized, logged in users may create an exercise item.  These users may
edit and/or delete exercises that they themselves created.  The site contains
introductory information and a disclaimer concerning the terms of use of this 
web app.  Visitors might compile an exercise program by choosing from each
category in order one or more exercise choices.

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


A virtual machine is available that contains many of these applications and is
explained below.


##Installation

To run the application using the virtual machine (VM):

1.  Follow the installation instructions found here:
	https://www.udacity.com/wiki/ud197/install-vagrant  
    But, instead of forking Udacity's repository at the section:
    "Use Git/GitHub to fetch the VM configuration," fork, download zip or clone:
    Deanna's Repository https://github.com/DeannaWagner/fullstack-nanodegree-vm  	
2.  Type the following commands at the command line prompt:
    a. cd fullstack/vagrant
    b. vagrant up
    c. vagrant ssh
    d. cd catalog
    e. sudo su
    f. sudo -u postgres createuser fcuser
    g. enter password for user that matches connection strings in .py files
    h. pip install flask-seasurf
    i. pip install dict2xml
    j. install any other dependencies that may be required
    k. python db_setup.py
    l. python db_populate.py
    m. python application.py
    n. browse to localhost:5000
    o. sign in with google account
    p. explore the site and interact with its functionality

For the cloud server, simply browse to http://deannawagner.com and interact with
its functionality.  


##Extra Credit Description

This project includes some features that exceed specifications:

1.  Additional API endpoints are implemented in XML

2.  CRUD Read.  An item image field is contained within and read from database 
    and displayed along with the item name and description

3.  CRUD create.  New item form updated to process inclusion of images.

4.  CRUD Update.  Edit item form updated to process inclusion of images.

5.  CRUD Delete.  Implement function to delete an item record using POST requests
    and nonces to prevent cross-site request forgeries (CSRF).


##Miscellaneous

Some credit is rightfully due and offered to the Udacity discussion forum, the 
supporting courses instructor, and the Udacity webcasts for general instruction
on how to implement the various aspects of this project.

