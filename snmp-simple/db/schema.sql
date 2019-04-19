/*
 Navicat Premium Data Transfer

 Source Server         : 73
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : 192.168.2.73:3306
 Source Schema         : cso

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 11/03/2019 17:41:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dev_info
-- ----------------------------
DROP TABLE IF EXISTS `dev_info`;
CREATE TABLE `dev_info`  (
  `ip` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'N/A' COMMENT '设备名称',
  `is_up` tinyint(255) UNSIGNED NULL DEFAULT 1 COMMENT '默认为开启:1,\r\n0: 未开启',
  `mac` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'mac  地址',
  `id_type` smallint(5) UNSIGNED NULL DEFAULT 0 COMMENT '设备类型ID',
  `add_time` datetime(0) NULL DEFAULT NULL COMMENT '数据添加时间',
  `comment` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT 'N/A',
  PRIMARY KEY (`ip`) USING BTREE,
  INDEX `id_type`(`id_type`) USING BTREE,
  CONSTRAINT `id_type` FOREIGN KEY (`id_type`) REFERENCES `dev_type` (`uniq_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '设备信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for dev_service
-- ----------------------------
DROP TABLE IF EXISTS `dev_service`;
CREATE TABLE `dev_service`  (
  `uniq_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '主键',
  `ip` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `protocol` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '协议类型',
  `port` smallint(5) UNSIGNED NOT NULL DEFAULT 0,
  `app_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '服务名称',
  `app_version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `app_version_comment` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '版本备注',
  PRIMARY KEY (`uniq_id`) USING BTREE,
  INDEX `ip`(`ip`) USING BTREE,
  CONSTRAINT `ip` FOREIGN KEY (`ip`) REFERENCES `dev_info` (`ip`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '网络设备中 存在的服务列表信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for dev_type
-- ----------------------------
DROP TABLE IF EXISTS `dev_type`;
CREATE TABLE `dev_type`  (
  `uniq_id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '设备名称',
  PRIMARY KEY (`uniq_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '设备类型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for snmp_oid
-- ----------------------------
DROP TABLE IF EXISTS `snmp_oid`;
CREATE TABLE `snmp_oid`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '名称',
  `oid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'oid字符串',
  `req_method` char(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '请求方式,get或者walk',
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  `oid_cate` varchar(55) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '-',
  PRIMARY KEY (`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for tmp_task_info
-- ----------------------------
DROP TABLE IF EXISTS `tmp_task_info`;
CREATE TABLE `tmp_task_info`  (
  `task_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '0' COMMENT '0: 未开始\r\n1：进行中\r\n2：已完成',
  `progress` tinyint(3) UNSIGNED NULL DEFAULT 0,
  `ecode` tinyint(255) UNSIGNED NULL DEFAULT 0 COMMENT '错误码',
  `update_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`task_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = 'web  任务表，这是一个临时表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
