## Centos下部署 SNMP

- `yum -y install net-snmp*`

```
yum install -y net-snmp
yum install -y net-snmp-devel
yum install -y net-snmp-libs
yum install -y net-snmp-perl
yum install -y net-snmp-utils
```
- 注意通常习惯和 `mrtg` 结合进行监控 `yum install -y mrtg`


## 配置
- 1, 定义 all .1 都能看到
- 2, 修改白名单 access systemview 为 all


## 使用略
