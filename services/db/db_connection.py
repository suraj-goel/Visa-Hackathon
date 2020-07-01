from flask_mysqldb import MySQL

def set_connection(app):
    """
    :param app: controller object
    :return: database connection
    """
    print('connecting to database....')
    app.config['MYSQL_HOST'] = 'SG-visahackathon-2575-master.servers.mongodirector.com'
    app.config['MYSQL_USER'] = 'sgroot'
    app.config['MYSQL_PASSWORD'] = 'k0fcxBO64qM.A2q1'
    app.config['MYSQL_DB'] = 'smallBusiness'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql = MySQL(app)
    print('Done!')
    return mysql
