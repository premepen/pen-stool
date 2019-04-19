import os, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
oids_file = os.path.join(BASE_DIR, "datas", "oids.txt")

def get_oids_info():
    with open(oids_file, "r+", encoding="utf-8") as f:
        lines = f.read().split("\n")
        f.close()
    oids_datas = []
    _category = "-"
    for line in lines:
        matched_category = re.match("(.*?)（(.*?)）", line)
        matched_oid = re.match("(^\..*\d)\s*(.*?)\s*(\w+)\s*(GET|WALK)$", line)
        if matched_category:
            _category = matched_category.group(1)
            # print(_category)
        if matched_oid:
            temp = {}
            temp.setdefault("oid", matched_oid.group(1))
            temp.setdefault("desc", matched_oid.group(2))
            temp.setdefault("req_method", matched_oid.group(4))
            temp.setdefault("name", matched_oid.group(3))
            temp.setdefault("oid_cate", _category)
            oids_datas.append(temp)
    return oids_datas


from snmp.scripts.utils.db_utils import from_sql_get_data, sql_action


def write_oids2sql():
    PrimaryKey = "name"
    existed_oids = [x[PrimaryKey] for x in from_sql_get_data("""select oid,name from snmp_oid group by oid;""")["data"]]
    _datas = get_oids_info()
    _sql_str_list = []
    for item in _datas:
        if item[PrimaryKey] in existed_oids:
            continue
        _sql_str = "(\'" + "\',\'".join([item["oid"],
                                         item["desc"],
                                         item["req_method"],
                                         item["oid_cate"],
                                         item["name"],
                                         ]) + "\')"
        _sql_str_list.append(_sql_str)
    _query_sql = """insert into snmp_oid(`oid`, `desc`, `req_method`, `oid_cate`, `name`) values {values_str};""".format(
        values_str=", ".join(_sql_str_list)
    )

    try:
        # print(_query_sql)
        sql_action(_query_sql)
        # print(_query_sql)
    except:
        import logging
        logging.info("数据格式化失败！")
    return len(_datas)


if __name__ == '__main__':
    write_oids2sql()