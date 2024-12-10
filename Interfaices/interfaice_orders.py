import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import psycopg2

class OrdersWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Информация о заказах")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(8)
        self.orders_table.setHorizontalHeaderLabels(["Заказ", "Время", "Пользователь", "Email", "Номер", "Адрес", "Цена", "Действие"])
        layout.addWidget(self.orders_table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_orders_data()

    def load_orders_data(self):
        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        try:
            # Установление соединения с базой данных
            conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
            cur = conn.cursor()

            # SQL-запрос для получения информации о заказах, сортированных по времени
            sql_query = "SELECT o.id, o.name, o.timestamp, u.name, u.email, u.number, u.address, o.price " \
                        "FROM orders AS o " \
                        "JOIN users AS u ON o.id = u.id " \
                        "ORDER BY o.timestamp"

            # Выполнение SQL-запроса
            cur.execute(sql_query)

            # Извлечение результатов запроса
            orders = cur.fetchall()

            # Установка количества строк в таблице
            self.orders_table.setRowCount(len(orders))

            # Заполнение таблицы информацией о заказах
            for row, order in enumerate(orders):
                order_id, order_name, order_timestamp, user_name, user_email, user_number, user_address, order_price = order

                order_item = QTableWidgetItem(order_name)
                self.orders_table.setItem(row, 0, order_item)

                timestamp_item = QTableWidgetItem(str(order_timestamp))
                self.orders_table.setItem(row, 1, timestamp_item)

                user_item = QTableWidgetItem(user_name)
                self.orders_table.setItem(row, 2, user_item)

                email_item = QTableWidgetItem(user_email)
                self.orders_table.setItem(row, 3, email_item)

                number_item = QTableWidgetItem(user_number)
                self.orders_table.setItem(row, 4, number_item)

                address_item = QTableWidgetItem(user_address)
                self.orders_table.setItem(row, 5, address_item)

                price_item = QTableWidgetItem(str(order_price))  # Преобразование цены в строку
                self.orders_table.setItem(row, 6, price_item)

                # Создание кнопки "Выполнено"
                button = QPushButton("Выполнено")
                button.setProperty("order_id", order_id)  # Установка свойства с ID заказа
                button.clicked.connect(self.complete_order)
                self.orders_table.setCellWidget(row, 7, button)

            # Автоматическое изменение размеров столбцов таблицы
            self.orders_table.resizeColumnsToContents()

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при загрузке информации о заказах:", error)

    def complete_order(self):
        button = self.sender()  # Получение кнопки, вызвавшей событие
        order_id = button.property("order_id")  # Получение ID заказа из свойства кнопки

        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        try:
            # Установление соединения с базой данных
            conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
            cur = conn.cursor()

            # SQL-запрос для удаления заказа из таблицы orders
            sql_query_orders = "DELETE FROM orders WHERE id = %s"
            # SQL-запрос для удаления пользователя из таблицы users
            sql_query_users = "DELETE FROM users WHERE id = %s"

            # Выполнение SQL-запроса для удаления заказа
            cur.execute(sql_query_orders, (order_id,))
            # Выполнение SQL-запроса для удаления пользователя
            cur.execute(sql_query_users, (order_id,))

            # Подтверждение изменений в базе данных
            conn.commit()

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

            # Удаление строки из таблицы
            row = self.orders_table.indexAt(button.pos()).row()
            self.orders_table.removeRow(row)

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при удалении заказа:", error)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OrdersWindow()
    window.show()
    sys.exit(app.exec_())
#Меликсетян Девид ИСП 2-6