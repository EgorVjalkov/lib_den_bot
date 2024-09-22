import datetime
from typing import Optional
from sqlalchemy import create_engine
import pandas as pd

from connection_config import user, password, host, db_name


engine = create_engine(
    f'postgresql+psycopg2://{user}:{password}@{host}:5432/{db_name}')


class DataBase:
    def __init__(self, table_name):
        self.table_name = table_name

    def get_table(self,
                  with_dates: bool,
                  index_col: Optional[str] = None,
                  columns: Optional[list] = None) -> pd.DataFrame:
        table = pd.read_sql_table(self.table_name,
                                  con=engine,
                                  schema='public',
                                  index_col=index_col,
                                  columns=columns)
        if with_dates:
            table['DATE'] = table['DATE'].map(lambda i: i.date())
        return table

    def update_table(self, table: pd.DataFrame, index_label: str = 'DATE'):
        table.to_sql(self.table_name,
                     con=engine,
                     if_exists='replace',
                     index_label=index_label)

    def get_game_list(self) -> list:
        table = self.get_table(with_dates=False).set_index('bgame')
        return table.index.to_list()

    def get_leased_games(self, user_id: int) -> pd.Series:
        place_ser = self.get_table(with_dates=False, index_col='bgame').get('place')
        user_games_ser = place_ser[place_ser == str(user_id)]
        return user_games_ser

    def set_day_row_and_upload(self, day_row: pd.Series) -> pd.DataFrame:
        table = self.get_table(with_dates=True).set_index('DATE')
        table.loc[day_row.name] = day_row
        self.update_table(table)
        return table


if __name__ == '__main__':
    pd.set_option('display.max_columns', 100)
    xls_name = 'game_base'

    # for vedomost upload:
    #ved_frame = pd.read_excel(f'{xls_name}.xlsx', index_col=0, dtype=str)
    #print(ved_frame)
    df = DataBase(xls_name)
    frame = df.get_table(with_dates=False).set_index('bgame')
    frame = frame.sort_index()
    df.update_table(frame, 'bgame')

    # for price upload:
    #price_frame = pd.read_excel(f'{price}.xlsx', index_col=0, dtype=str)
    #print(price_frame)
    #df = DataBase(xls_name)
    #df = df.get_table(with_dates=False).set_index('DATE')
    #df.to_excel('aug24_vedomost.xlsx')
