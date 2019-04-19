import xmltodict, os

from snmp.cfgs.db_cfg import BASE_DIR


def get_xml(path):
    with open(path, "r+", encoding="utf-8") as f:
        try:
            return f.read()
        finally:
            f.close()


def get_data_info():
    path = os.path.join(BASE_DIR, "datas", "n2.xml")
    xml = get_xml(path)
    datas = xmltodict.parse(xml)["nmaprun"]

    push_time = datas["@startstr"]
    nmap_args = datas["@args"]
    hosts_datas = datas["host"]
    services = []
    for host_datas in hosts_datas:
        host_info = host_datas["address"]
        print(host_datas)
        if type(host_info) != type([]):
            continue

        host_ip = [x["@addr"] for x in host_info if x["@addrtype"] == 'ipv4'][0]
        host_mac = [x["@addr"] for x in host_info if x["@addrtype"] == 'mac'][0]
        if "ports" in host_datas.keys():
            try:
                port_info = host_datas["ports"]
                for k, value in port_info.items():
                    if "port" == k:
                        for x in value:
                            _temp = {}
                            # 开始格式化我们自己的端口服务信息
                            _temp["port"] = x["@portid"] if "@portid" in x.keys() else "0"
                            _temp["protocol"]= x["@protocol"] if "@protocol" in x.keys() else "ptl"
                            _temp["state"]= x["@state"] if "@state" in x.keys() else "open"
                            # _temp["service"]= x["service"] if "service" in x.keys() else {}
                            _serv = x["service"]

                            if "@product" in _serv.keys():
                                app_version = _serv["@product"] + " " + _serv["@version"] if "@version" in _serv.keys() else _serv[
                                    "@product"]
                            else:
                                app_version = "unknown version"

                            _temp["service"] = dict(
                                app_name=_serv["@name"],
                                app_version=app_version,
                                app_version_comment = _serv["@extrainfo"] if "@extrainfo" in _serv.keys() else "",
                                port=_temp["port"],
                                protocol=_temp["protocol"],
                                ip=host_ip
                            )
                            ## 结束端口服务信息
                            _temp.setdefault("mac", host_mac)
                            _temp.setdefault("ip", host_ip)
                            services.append(_temp)
            except:
                # print(host_datas[KEY].keys())
                pass
    results = dict(
        nmap_args=nmap_args,
        services=services,
        push_time=push_time
    )
    return results

from uuid import uuid4

def write_data_to_dbs():
    _datas = [x["service"] for x in get_data_info()["services"]]
    _sql_str_list = []
    for item in _datas:
        _sql_str = "(\'" + "\',\'".join([str(uuid4()),
                                         item["ip"],
                                         item["protocol"],
                                         item["port"],
                                         item["app_name"],
                                         item["app_version"],
                                         item["app_version_comment"],
                                         ]) + "\')"
        _sql_str_list.append(_sql_str)
    _query_sql = """insert into dev_service(`uniq_id`, `ip`, `protocol`, `port`, `app_name`, `app_version`, `app_version_comment`) values {values_str};""".format(
        values_str=", ".join(_sql_str_list)
    )

    from snmp.scripts.utils.db_utils import sql_action
    sql_action(_query_sql)

from datetime import datetime
# _date = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
_date = datetime.now()

from snmp.scripts.utils.db_utils import from_sql_get_data, sql_action

def write_sql_2_sql():
    _datas = get_data_info()["services"]
    PrimaryKey = "ip"
    existed_ips = [x[PrimaryKey] for x in from_sql_get_data("""select ip,mac from dev_info group by ip;""")["data"]]

    _sql_str_list = []
    ip_list = []
    for item in _datas:
        print(item)
        if item["ip"] in existed_ips or item["ip"] in ip_list:
            continue
        _sql_str = "(\'" + "\',\'".join([str(item["ip"]),
                                         "",
                                         str(1),
                                         str(item["mac"]),
                                         str(1),
                                         str(_date),
                                         "内网主机",
                                         ]) + "\')"
        _sql_str_list.append(_sql_str)
        ip_list.append(item["ip"])
    _query_sql = """insert into dev_info(`ip`, `name`, `is_up`, `mac`, `id_type`, `add_time`, `comment`) values {values_str};""".format(
        values_str=", ".join(_sql_str_list)
    )

    sql_action(_query_sql)


def inital_sqls():
    sql_action("delete from dev_info;")
    sql_action("delete from dev_service;")


def task():
    # inital_sqls()
    write_sql_2_sql()
    write_data_to_dbs()

if __name__ == '__main__':
    task()

    # print(get_data_info())
