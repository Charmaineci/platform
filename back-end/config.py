# 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'yolo_detection',
    'port': 3306
}

# JWT配置
JWT_SECRET_KEY = 'your-secret-key'  # 请更改为一个安全的密钥
JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24小时 