from tornado.options import define

#port
define("port", default=9014, help="run on the given port", type=int)

#mysql
define("mysql_host", default="47.110.232.145:3306", help="database host")
define("mysql_database", default="youbao", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="4608310zk", help="database password")

define("pool_size", default=20, help="pool size")
define("pool_recycle", default=3600, help="pool recycle")

#tornado execute threads num
define("max_workers", default=25, type=int, help="max threads")

#redis
define("redis_host", default="47.110.67.202", help="redis host")
define("redis_port", default="6379", help="redis port")
define("redis_password", default="123456", help="redis password")

#session
define("session_key", default="JinLiBao123321~#", help="session key")
