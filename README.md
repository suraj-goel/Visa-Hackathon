__Small Business Merchants__

project structure:
1. common : html, css and js needed for all packages
2. modules: are made according to the user stories. Includes one html file for now
3. venu: virtual environment for project, contains all packages
4. services: for database connection and Visa API calls. It contains
    (a) certificate and key for VDP
    (b)db : to manage all database functions 
      (i) will have db functions for different modules
      (ii) connection file
5. app.py is the default controller for flask

note: do not delete __init__.py and 

__render templates__
follow "module/htmlfile.html" to render templates

__to link CSS__
1. in common/css and your css file
2. put this in html file and replace stylefile with your new file name
<link rel="stylesheet" href= "{{ url_for('static',filename='css/stylefile.css') }}"> 

install dependencies:
pip install -r requirements.txt

__deployment__
heroku
https://stackabuse.com/deploying-a-flask-application-to-heroku/
