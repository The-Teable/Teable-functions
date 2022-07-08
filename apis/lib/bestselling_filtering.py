# connect mysql
from .ConnectDB import MYSQLDB

def bestselling_filtering():
    myDB = MYSQLDB()
    Tea_df = myDB.teas
    bestselling_df = Tea_df.sort_values('sell_count', ascending=False)
    bestselling_df_result = bestselling_df.head(10)

    return (bestselling_df_result)
