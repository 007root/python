from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from datetime import datetime
import MySQLdb


HOST = "192.168.4.5"
USER = "root"
PASS = "root"
KEY = "INSERT INTO `django_session` VALUES "
VALUE = "(\"%s\", \"%s\", \"%s\")"
v_list = []

mongo_client = MongoClient(host=HOST)
mongo_db = mongo_client.test
session = mongo_db.session
user_info = mongo_db.user_info

mysql_db = MySQLdb.connect(HOST, USER, PASS, "test")
cursor = mysql_db.cursor()


def get_user_id(uid=None):
    if uid == None:
        ret = user_info.find({}, {"user_id": 1}).sort("user_id", ASCENDING).limit(500)
    else:
        ret = user_info.find({"user_id": {"$gt": uid}}, {"user_id": 1}).sort("user_id", ASCENDING).limit(500)
    return ret


result = get_user_id()
while result.count():
    for user in result:
        if user.get("user_id"):
            ret = session.find({"$and": [{"user_id": user["user_id"]}, {"expire_date": {"$gt": datetime.today()}}]})
            if ret.count() != 0:
                for r in ret:
                    v_list.append(VALUE % (r["session_key"], r["session_data"], r["expire_date"]))
                values = ','.join(v_list)
                exec_sql = KEY + values + ";"
                cursor.execute(exec_sql)
                mysql_db.commit()
                v_list = []
    else:
        result = get_user_id(user["user_id"])


