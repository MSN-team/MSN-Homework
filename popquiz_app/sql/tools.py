import pymysql

class DBUtil:
    config={
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'database': 'MSN',
        'charset' : 'utf8'
    }
    def __init__(self)->None:
        #建立连接
        self.connection=pymysql.connect(**DBUtil.config)
        #获取游标
        self.cursor= self.connection.cursor()

    def close(self)->None:
        #关闭游标
        self.cursor.close()
        #关闭连接
        self.connection.close()

    def execute(self,sql,*args):
        try:
            #执行sql语句
            self.cursor.execute(sql,args)
            #提交事务
            self.connection.commit()
        except Exception as e:
            #回滚事务
            print(e)
            if(self.connection):
                self.connection.rollback()
        finally:
           self.close()
   