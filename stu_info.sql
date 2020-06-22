CREATE TABLE `stu_info` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '姓名',
  `sid` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学号',
  `sex` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别',
  `college` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学院',
  `class` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级',
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号码',
  `minor` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '辅修',
  `type` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '未知',
  `qq` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'QQ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;