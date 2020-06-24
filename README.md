# Small Business Merchants #

## project structure ##
1. common : html, css and js needed for all packages
2. modules: are made according to the user stories. Includes one html file for now.
    __always seperate out your html,css and js code and place them under the same module__
3. venu: virtual environment for project, contains all packages
4. services: for database connection and Visa API calls. It contains
    - certificate and key for VDP
    - db : to manage all database functions 
      - will have db functions for different modules
      - connection file
5. app.py is the default controller for flask

note: do not delete __init__.py

__render templates__
follow "module/htmlfile.html" to render templates

__to link CSS__
1. in common/css and your css file
2. put this in html file and replace stylefile with your new file name
```
<link rel="stylesheet" href= "{{ url_for('static',filename='css/stylefile.css') }}"> 
```

__dependencies__
1. install
```
pip install -r requirements.txt
```
2.update
```
pip freeze> requirements.txt
```

__deployment__
heroku
https://stackabuse.com/deploying-a-flask-application-to-heroku/
