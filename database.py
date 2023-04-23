import json
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor


class DbAdvanced:

    def __init__(self):
        self.conn = sqlite3.connect('marking_hack.db')
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS vvod(
           dt CHAR(50),
           inn CHAR(50),
           gtin CHAR(50),
           prid CHAR(50),
           operation_type CHAR(50),
           cnt CHAR(10)
           );
        """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS sprav_prod(
           gtin CHAR(50),
           inn CHAR(50),
           product_name CHAR(50),
           product_short_name CHAR(50),
           tnved CHAR(50),
           tnved10 CHAR(50),
           brand CHAR(50),
           country CHAR(50),
           volume CHAR(50)  
           );
        """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS oborot_tovarov(
           inn CHAR(50),
           region_code CHAR(50) 
           );
        """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS torg_tochki(
           id_sp_ CHAR(50),
           inn CHAR(50),
           region_code CHAR(50),
           city_with_type CHAR(50),
           city_fias_id CHAR(50),
           postal_code CHAR(50)
           );
        """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS peremeshenie(
           dt CHAR(50),
           gtin CHAR(50),
           prid CHAR(50),
           sender_inn CHAR(50),
           receiver_inn CHAR(50),
           cnt_moved CHAR(50)
           );
        """)
        self.conn.commit()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS vivod(
           dt CHAR(50),
           gtin CHAR(50),
           prid CHAR(50),
           inn CHAR(50),
           id_sp_ CHAR(50),
           type_operation CHAR(50),
           price CHAR(50),
           cnt CHAR(50)
           );
        """)
        self.conn.commit()

    def insert_into_db(self):
        pd.read_csv(r"C:\Users\Chubu\OneDrive\Рабочий стол\MH\Данные о выводе товаров из оборота с 2021-11-22 по 2022-11-21.csv").to_sql('vivod', self.conn, if_exists='append', index=False)
        pd.read_csv(r'C:\Users\Chubu\OneDrive\Рабочий стол\MH\Данные о вводе товаров в оборот с 2021-11-22 по 2022-11-21.csv').to_sql('vvod', self.conn, if_exists='append', index=False)
        pd.read_csv(r"C:\Users\Chubu\OneDrive\Рабочий стол\MH\Справочник продукции.csv").to_sql('sprav_prod', self.conn, if_exists='append', index=False)
        pd.read_csv(r"C:\Users\Chubu\OneDrive\Рабочий стол\MH\Справочник участников оборота товаров.csv").to_sql('oborot_tovarov', self.conn, if_exists='append', index=False)
        pd.read_csv(r"C:\Users\Chubu\OneDrive\Рабочий стол\MH\Справочник торговых точек.csv").to_sql('torg_tochki', self.conn, if_exists='append', index=False)
        pd.read_csv(r"C:\Users\Chubu\OneDrive\Рабочий стол\MH\Данные о перемещениях товаров между участниками с 2021-11-22 по 2022-11-21.csv").to_sql('peremeshenie', self.conn, if_exists='append', index=False)

    def torg_points(self):
        ### Используя JSON файл получаю названия 1132 городов с их координатами
        with open("russian-cities.json", encoding="utf8") as f:
            d = json.load(f)

        self.city_list = []
        self.city_lon = []
        self.city_lat = []

        for element in d:
            self.city_list.append(element['name'])
            self.city_lon.append(element['coords']['lat'].lower())
            self.city_lat.append(element['coords']['lon'].lower())

        self.cur.execute('SELECT * FROM torg_tochki WHERE city_with_type NOT NULL')
        elements = self.cur.fetchall()

        self.draw_info = []

        for element in elements:
            city_name = element[3].split()[-1]
            if city_name in self.city_list:
                num = self.city_list.index(city_name)
                lat = float(self.city_lon[num])
                lon = float(self.city_lat[num])

                new_element = (city_name, lat, lon)
                if new_element not in self.draw_info:
                    self.draw_info.append(new_element)

    def create_plot_vvod(self, gtin):

        self.cur.execute('SELECT * from vvod WHERE gtin == ?', (gtin,))
        vvod_records = self.cur.fetchall()

        vvod_data = dict()

        for row in vvod_records:
            if row[0] not in vvod_data and type(row[-1] == int):
                vvod_data[row[0]] = int(row[-1])
            if row[0] in vvod_data and type(row[-1] == int):
                vvod_data[row[0]] += int(row[-1])

        return vvod_data

    def create_plot_vivod(self, gtin):
        self.cur.execute('SELECT * from vivod WHERE gtin == ?', (gtin,))
        vivod_records = self.cur.fetchall()

        vivod_data = dict()

        for row in vivod_records:
            if row[0] not in vivod_data and type(row[-1] == int):
                vivod_data[row[0]] = int(row[-1])
            if row[0] in vivod_data and type(row[-1] == int):
                vivod_data[row[0]] += int(row[-1])

        return vivod_data

    def create_vvod_gtin_map(self, gtin):

        ### Используя JSON файл получаю названия 1132 городов с их координатами
        with open("russian-cities.json", encoding="utf8") as f:
            d = json.load(f)

        self.city_list = []
        self.city_lon = []
        self.city_lat = []

        for element in d:
            self.city_list.append(element['name'])
            self.city_lon.append(element['coords']['lat'].lower())
            self.city_lat.append(element['coords']['lon'].lower())

        self.cur.execute('SELECT * from vvod WHERE gtin == ?', (gtin,))
        vvod_gtin = self.cur.fetchall()

        self.gtin_draw_info = []

        for row in vvod_gtin:
            self.cur.execute('SELECT * from torg_tochki WHERE inn == ?', (row[1],))

            if self.cur.fetchone():
                city = self.cur.fetchone()

                if not city:
                    continue

                city = str(city[3])
                city = city.split()[-1]

                if city in self.city_list:
                    num = self.city_list.index(city)
                    lat = float(self.city_lon[num])
                    lon = float(self.city_lat[num])

                    new_element = (city, lat, lon, row[0], row[4], row[5])
                    if new_element not in self.gtin_draw_info:
                        self.gtin_draw_info.append(new_element)

        self.gtin_draw_info_final = dict()

        for element in self.gtin_draw_info:
            if (element[0], element[1], element[2]) not in self.gtin_draw_info_final:
                self.gtin_draw_info_final[(element[0], element[1], element[2])] = [(element[3], element[4], element[5])]
            else:
                self.gtin_draw_info_final[(element[0], element[1], element[2])].append((element[3], element[4], element[5]))

    def create_vivod_gtin_map(self, gtin):

        ### Используя JSON файл получаю названия 1132 городов с их координатами
        with open("russian-cities.json", encoding="utf8") as f:
            d = json.load(f)

        self.city_list = []
        self.city_lon = []
        self.city_lat = []

        for element in d:
            self.city_list.append(element['name'])
            self.city_lon.append(element['coords']['lat'].lower())
            self.city_lat.append(element['coords']['lon'].lower())

        self.cur.execute('SELECT * from vivod WHERE gtin == ?', (gtin,))
        vivod_gtin = self.cur.fetchall()

        self.gtin_draw_info_vivod = []

        for row in vivod_gtin:
            self.cur.execute('SELECT * from torg_tochki WHERE inn == ?', (row[3],))

            if self.cur.fetchone():
                city = self.cur.fetchone()

                if not city:
                    continue

                city = str(city[3])
                city = city.split()[-1]
                #print(city)

                if city in self.city_list:
                    num = self.city_list.index(city)
                    lat = float(self.city_lon[num])
                    lon = float(self.city_lat[num])

                    new_element = (city, lat, lon, row[0], row[-3], row[-1])
                    if new_element not in self.gtin_draw_info_vivod:
                        self.gtin_draw_info_vivod.append(new_element)

        self.gtin_draw_info_vivod_final = dict()

        for element in self.gtin_draw_info_vivod:
            if (element[0], element[1], element[2]) not in self.gtin_draw_info_vivod_final:
                self.gtin_draw_info_vivod_final[(element[0], element[1], element[2])] = [(element[3], element[4], element[5])]
            else:
                self.gtin_draw_info_vivod_final[(element[0], element[1], element[2])].append((element[3], element[4], element[5]))

    def route(self, gtin):

        with open("russian-cities.json", encoding="utf8") as f:
            d = json.load(f)

        self.city_list = []
        self.city_lon = []
        self.city_lat = []

        for element in d:
            self.city_list.append(element['name'])
            self.city_lon.append(element['coords']['lat'].lower())
            self.city_lat.append(element['coords']['lon'].lower())

        self.paths = []
        self.cur.execute('SELECT * FROM peremeshenie WHERE gtin == ?', (gtin,))
        records = self.cur.fetchall()

        for row in records:
            local_path = []
            self.cur.execute('SELECT * from torg_tochki WHERE inn == ?', (row[3],))
            if self.cur.fetchone():
                city = self.cur.fetchone()

                if not city:
                    continue

                city = str(city[3])
                city = city.split()[-1]

                if city in self.city_list:
                    num = self.city_list.index(city)
                    lat = float(self.city_lon[num])
                    lon = float(self.city_lat[num])
                    dt = row[0]

                    local_path.extend([city, lat, lon, dt])

            self.cur.execute('SELECT * from torg_tochki WHERE inn == ?', (row[4],))
            if self.cur.fetchone():
                city1 = self.cur.fetchone()

                if not city1:
                    continue

                city1 = str(city1[3])
                city1 = city1.split()[-1]

                if city1 in self.city_list:
                    num = self.city_list.index(city1)
                    lat1 = float(self.city_lon[num])
                    lon1 = float(self.city_lat[num])

                    local_path.extend([city1, lat1, lon1])
            self.paths.append(local_path)

        self.paths = [el for el in self.paths if len(el) == 7]
        print(self.paths)

    def prediction(self, gtin):

        self.cur.execute('SELECT dt, gtin, price, cnt FROM vivod WHERE gtin = ? AND price != "0"', (gtin,))

        data = self.cur.fetchall()

        df = pd.DataFrame(data, columns=['date', 'product', 'price', 'quantity'])

        # Преобразование данных
        df['date'] = pd.to_datetime(df['date'])
        df['price'] = df['price'].astype(float)
        df['quantity'] = df['quantity'].astype(int)
        df['weekday'] = df['date'].dt.weekday
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year

        # Выбор заданного продукта
        df = df[df['product'] == gtin]

        # Разделение данных на тренировочный и тестовый наборы
        train_size = int(len(df) * 0.9)
        train_df = df[:train_size]

        # Обучение модели случайного леса
        features = ['weekday', 'month', 'year', 'quantity']
        target = 'price'
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=0)
        rf.fit(train_df[features], train_df[target])

        # Предсказание объема продаж на три месяца вперед
        future_dates = pd.date_range(start=df['date'].max(), periods=90, freq='D')[1:]
        future_df = pd.DataFrame({'date': future_dates})
        future_df['weekday'] = future_df['date'].dt.weekday
        future_df['month'] = future_df['date'].dt.month
        future_df['year'] = future_df['date'].dt.year
        future_df['quantity'] = 0  # Задаем нулевое количество продаж

        future_df['predicted_price'] = rf.predict(future_df[features])

        self.current1 = sorted(df['date'])
        self.current2 = df['price']

        self.predicted1 = future_df['date']
        self.predicted2 = future_df['predicted_price']

         


# if __name__ == '__main__':
#     test_one = DbAdvanced()
#     #test_one.insert_into_db()
#     #test_one.create_plot("8D4932D20D0ECA4F36669252566F05A9")
#     test_one.torg_points()