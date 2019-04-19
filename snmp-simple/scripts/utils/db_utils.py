import pymysql


from snmp.cfgs.db_cfg import DEBUG
if DEBUG:
    MPP_CONFIG = {
        'host': '192.168.2.73',
        'port': 3306,
        'user': 'actanble',
        'password': '09121233.',
        'db': 'cso',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
else:
    MPP_CONFIG = {
        'host': '192.168.2.101',
        'port': 3306,
        'user': 'admin007',
        'password': 'myadmin@816',
        'db': 'cso',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }

def from_sql_get_data(sql, MPP_CONFIG=MPP_CONFIG):
    # Connect to the database
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    try:
        res = corsor.fetchall()
        try:
            data = {"data": res, "heads": [x[0] for x in corsor.description]}
        except:
            data = None
    finally:
        ## connection.commit()
        corsor.close()
        connection.close()
    return data


## 单纯执行的
def sql_action(sql):
    connection = pymysql.connect(**MPP_CONFIG)
    corsor = connection.cursor()
    corsor.execute(sql)
    # print(sql)
    connection.commit()
    corsor.close()
    connection.close()
    return
