import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# функция для создания таблиц в БД marking_hack_database
def create_tables():
    '''
    # создание таблиц БД
    # создание таблицы "Справочник продукции" volume в граммах, до 999 999 гр., т.е до 999 кг. 999 гр.
    cur.execute("""
        CREATE TABLE Spravochnik_produkcii (
            gtin CHAR(32),
            inn CHAR(32),
            product_name CHAR(32),
            product_short_name CHAR(32),
            tnved CHAR(32),
            tnved10 CHAR(32),
            brand CHAR(32),
            country CHAR(100),
            volume CHAR(255) 
        );
    """)

    # создание таблицы "Справочник торговых точек"
    cur.execute("""
        CREATE TABLE Spravochnik_torgovyh_tochek (
            id_sp_ CHAR(32),
            inn CHAR(32),
            region_code CHAR(50),
            city_with_type CHAR(255),
            city_fias_id CHAR(36),
            postal_code CHAR(50)
        );
    """)

    # создание таблицы "Справочник участников оборота товаров"
    cur.execute("""
        CREATE TABLE Spravochnik_uchastnikov_oborota_tovarov (
            inn CHAR(32),
            region_code CHAR(50)
        );
    """)

    # создание таблицы "Данные о вводе в оборот"
    cur.execute("""
        CREATE TABLE Dannye_o_vvode_v_oborot (
            dt DATE,
            inn CHAR(32),
            gtin CHAR(32),
            prid CHAR(32),
            operation_type CHAR(50),
            cnt CHAR(50)
        );
    """)
    '''
    # создание таблицы "Данные о выводе из оборота"
    cur.execute("""
        CREATE TABLE Dannye_o_vyvode_iz_oborota (
            dt DATE,
            gtin CHAR(32),
            prid CHAR(32),
            inn CHAR(32),
            id_sp_ CHAR(32),
            type_operation CHAR(50),
            price CHAR(50),
            cnt CHAR(50)
        );
    """)

    # создание таблицы "Данные о перемещениях между участниками"
    cur.execute("""
        CREATE TABLE Dannye_o_peremeshcheniyah_mezhdu_uchastnikami (
            dt DATE,
            gtin CHAR(32),
            prid CHAR(32),
            sender_inn CHAR(32),
            receiver_inn CHAR(32),
            cnt_moved CHAR(50)
        );
    """)
    conn.commit()


# функция загрузки в фрейм pandas DataFrame данных из csv и записи их в БД
def read_load_DataFrame_in_database():
    # загружаем файл с данными в pandas DataFrame
    Spravochnik_produkcii = pd.read_csv('Справочник продукции.csv')
    Spravochnik_torgovyh_tochek = pd.read_csv('Справочник торговых точек.csv')
    Spravochnik_uchastnikov_oborota_tovarov = pd.read_csv('Справочник участников оборота товаров.csv')
    Dannye_o_vvode_v_oborot = pd.read_csv("Данные о вводе товаров в оборот с 2021-11-22 по 2022-11-21.csv")
    Dannye_o_vyvode_iz_oborota = pd.read_csv("Данные о выводе товаров из оборота с 2021-11-22 по 2022-11-21.csv")
    Dannye_o_peremeshcheniyah_mezhdu_uchastnikami = pd.read_csv("Данные о перемещениях товаров между участниками с 2021-11-22 по 2022-11-21.csv")

    # Запишем данные в таблицы
    insert_data(Spravochnik_produkcii, 'spravochnik_produkcii')
    insert_data(Spravochnik_torgovyh_tochek, 'spravochnik_torgovyh_tochek')
    insert_data(Spravochnik_uchastnikov_oborota_tovarov, 'spravochnik_uchastnikov_oborota_tovarov')
    insert_data(Dannye_o_vvode_v_oborot, 'dannye_o_vvode_v_oborot')
    insert_data(Dannye_o_vyvode_iz_oborota, 'dannye_o_vyvode_iz_oborota')
    insert_data(Dannye_o_peremeshcheniyah_mezhdu_uchastnikami, 'dannye_o_peremeshcheniyah_mezhdu_uchastnikami')
    
    print(Dannye_o_vyvode_iz_oborota.head(10))

# Определим функцию для выполнения записи данных в таблицу
def insert_data(dataframe, table_name):
    # Составим запрос на вставку данных в таблицу
    query = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, dataframe.columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(dataframe.columns))
    )
    # Выполним запрос на вставку данных в таблицу
    for index, row in dataframe.iterrows():
        cur.execute(query, list(row))
    
    # Закроем транзакцию
    conn.commit()


def drop_all_tables():
    cur.execute("DROP SCHEMA public CASCADE;")
    cur.execute("CREATE SCHEMA public;")
    conn.commit()


def dfs(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = dfs(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


# подключение к базе данных marking_hack_database
conn = psycopg2.connect(
    host="localhost",
    database="marking_hack_database",
    user="postgres",
    password="12345678",
    port="5432"
)

# создание курсора
cur = conn.cursor()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
product_name = 'E1C0503EA9201D56D7173CB4CA4A6AFA'

cur.execute('''
    SELECT dt, gtin, price, cnt
    FROM dannye_o_vyvode_iz_oborota
    WHERE gtin = %s
''', [product_name])
data = cur.fetchall()

df = pd.DataFrame(data, columns=['date', 'product', 'price', 'quantity'])

# Преобразование данных
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
df['quantity'] = df['quantity'].astype(int)
df['weekday'] = df['date'].dt.weekday
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Выбор заданного продукта
product = product_name
df = df[df['product'] == product]

# Разделение данных на тренировочный и тестовый наборы
train_size = int(len(df) * 0.9)
train_df = df[:train_size]
test_df = df[train_size:]

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
future_df['quantity'] = 0 # Задаем нулевое количество продаж

future_df['predicted_price'] = rf.predict(future_df[features])

plt.figure(figsize=(10, 5))
plt.plot(sorted(df['date']), df['price'], label='Текущие продажи', color='blue')
plt.plot(future_df['date'], future_df['predicted_price'], label='Предсказанные продажи', color='red')
plt.xlabel('Дата')
plt.ylabel('Цена продажи')
plt.title('Продажи продукта "{}"'.format(product))
plt.legend()
plt.show()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# закрытие соединения с базой данных
cur.close()
conn.close()


# cur.execute('''
#     SELECT sender_inn, receiver_inn
#     FROM dannye_o_peremeshcheniyah_mezhdu_uchastnikami
# ''')
# graph_peremeshcheniya = cur.fetchall()
# print(graph_peremeshcheniya)

# # пример входных данных
# edges = graph_peremeshcheniya
# # создание графа
# graph = {}
# for edge in edges:
#     if edge[0] not in graph:
#         graph[edge[0]] = []
#     graph[edge[0]].append(edge[1])

# # поиск маршрутов движения
# start = '19485F700068E6A9A8593AFDE9803638'
# end = None
# paths = []
# for node in graph:
#     if node == start:
#         continue
#     new_paths = dfs(graph, node, start)
#     for new_path in new_paths:
#         paths.append([start] + new_path)

# # вывод результатов
# for el in paths:
#     print(el[1:])




#---------------------------------------------------------------------------------------------------------------------------------------------
#drop_all_tables()
#create_tables()
#read_load_DataFrame_in_database()


#---------------------------------------------------------------------------------------------------------------------------------------------
# print(" DATA,     GTIN,     INN,     ID TOCHKI,     COLVO TOVARA")
# cur.execute('''
#     SELECT dt, gtin, inn, id_sp_, cnt
#     FROM dannye_o_vyvode_iz_oborota
#     WHERE id_sp_ = '19485F700068E6A9A8593AFDE9803638' 
#     AND dt >= '2021-06-01'
#     AND dt <= '2021-12-01'
# ''')
# print("GOVNO = 19485F700068E6A9A8593AFDE9803638")
# inf_tovara = cur.fetchall()
# # dt, gtin, inn, id_sp_, cnt
# vse_tovari = []
# for el in inf_tovara:
#     print(*el) 
#     vse_tovari.append(el[1])
# print("Все товары: ", set(vse_tovari))
# print("========================")



# print(" GTIN,     SENDER,     RECEIVER,     COLVO TOVARA")
# for el in inf_tovara:
#     gtin = el[1]
#     receiver_inn = el[2]
#     cur.execute('''
#         SELECT COALESCE(gtin, 'NONE'), COALESCE(sender_inn, 'NONE'), COALESCE(receiver_inn, 'NONE'), COALESCE(cnt_moved, 'NONE')
#         FROM dannye_o_peremeshcheniyah_mezhdu_uchastnikami
#         WHERE gtin = %s
#         AND receiver_inn = %s
#     ''',[gtin, receiver_inn])
#     inf_peredachi = cur.fetchall()
#     # gtin, sender_inn, receiver_inn, cnt_moved
#     vse_skladi = []
#     for el_1 in inf_peredachi:
#         print(*el_1)
#         vse_skladi.append(el_1[1])
#     print("Все склады: ", set(vse_skladi))
#     print("---------------------------------------")
#---------------------------------------------------------------------------------------------------------------------------------------------
