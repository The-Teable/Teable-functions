# connect mysql
from .ConnectDB import MYSQLDB

def theme_filtering(theme):
    myDB = MYSQLDB()
    Tea_df = myDB.teas
    theme_df = Tea_df[Tea_df['theme'] == theme]
    theme_df_result = theme_df.sample(frac=1).reset_index(drop=True).head(10)

    return (theme_df_result)
