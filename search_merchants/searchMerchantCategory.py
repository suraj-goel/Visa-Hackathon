def getMerchantCategoryCode(mysql,category):
    """
    :param mysql: database connection object
    :param category: category registered as per Visa
    :return: merchant category code
    """
    category = category.upper()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM MerchantCategoryCode WHERE Category LIKE '{}'".format("%" + category + "%"))
    data = list(cur.fetchall())
    return data