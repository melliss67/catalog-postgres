Item Catalog
by Matt Ellis
2015-08-05

Summary:
This project is a web application using the Flask framework. The application
displays items by category and sub category. There is a JSON end point that 
allows downloading the catalog in a JSON format. Users can register with their
Google Plus account to have the ability to add, edits, and delete items.

Configuration:
This application was developed using Flask version 0.10.1. In addition to the
standard Flask libraries and sqlalchemy the application also uses json and
dict2xml libraries.

Installation:
The database_setup.py file can be used to create a blank database and the 
additems.py can be used to add sample items to the database.

Usage:
Run the application.py file to start the webserver. It is set to run on port 
8000. You can browse the items by selecting the categories and subcategories. 
If you register with your Google Plus account you can add, edit and delete 
items.

The full catalog can be accessed in a JSON or XML format using the following
urls. http://localhost:8000/catalog.json and http://localhost:8000/catalog.xml


