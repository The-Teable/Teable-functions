# connect mysql
import re
from datetime import datetime
from datetime import timedelta
import pymysql
import pandas as pd

# db연결
class MYSQLDB:
    def __init__(self):
        """생성자: MySQL 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='SkaksdmlTea', db='teable_dev', charset='utf8')
        self.users = self.get_user()
        self.teas = self.get_content()
        self.recommend_test_result = self.get_recommend_test_result()
        self.user_buy_df = self.get_user_buy()
        self.test_boolean = self.get_recommend_test()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def get_user(self):
        """user 테이블에서 읽어와서 codes에 저장
        userinfo에서는 id값으로 name, age, gender을 가져옴"""
        sql = "SELECT * FROM users"
        user_info = pd.read_sql(sql, self.conn)
        user_df = pd.DataFrame(user_info)
        return user_df 

    def get_content(self):
        """teas 테이블에서 읽어와서 teas에 저장"""
        sql = "SELECT * FROM teas"
        tea_info = pd.read_sql(sql, self.conn)
        tea_df = pd.DataFrame(tea_info)
        return tea_df

    def get_recommend_test(self):
        """recommend test 여부를 test_boolean에 저장"""
        sql = "SELECT * FROM filtering_results"
        test_info = pd.read_sql(sql, self.conn)
        test_df = pd.DataFrame(test_info)
        return test_df


    def get_recommend_test_result(self):
        """recommend test의 결과를 recommend_test_result에 저장"""
        sql = "SELECT * FROM filtering_result_product_map"
        test_result_info = pd.read_sql(sql, self.conn)
        test_result_df = pd.DataFrame(test_result_info)
        test_result_df['interaction_type'] = 'Recommend_test'
        return test_result_df

    def get_user_buy(self):
        """user_buy_product를 가져와서 user_buy_df에 저장"""
        sql = "SELECT * FROM user_buy_product"
        user_buy_info = pd.read_sql(sql, self.conn)
        user_buy_df = pd.DataFrame(user_buy_info)
        user_buy_df['interaction_type'] = 'Buy'
        return user_buy_df