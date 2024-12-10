import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QInputDialog
import psycopg2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продукты")
        self.setGeometry(100, 100, 600, 400)

        # Создание виджета и размещение его на главном окне
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создание компонентов пользовательского интерфейса
        self.search_label = QLabel("ПОИСК:")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Поиск")
        self.update_button = QPushButton("Обновить")
        self.delete_button = QPushButton("Удалить")
        self.add_button = QPushButton("Добавить")
        self.table = QTableWidget()

        # Создание главного вертикального макета и добавление в него компонентов
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.search_label)


        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        layout.addWidget(self.delete_button)
        layout.addWidget(self.add_button)
        
        layout.addWidget(self.table)
        layout.addWidget(self.update_button)

        # Подключение событий к кнопкам
        self.search_button.clicked.connect(self.search_products)
        self.update_button.clicked.connect(self.update_data)

        self.delete_button.clicked.connect(self.delete_data)
        self.add_button.clicked.connect(self.add_data)
        
        # Установка заголовков таблицы
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "product_name", "unit_of_measurement", "price_of_1_unit", "amount", "actual_amount", "required_purchase"])

        # Загрузка данных из базы данных
        self.load_data()

    def load_data(self):
        # Подключение к базе данных PostgreSQL
        conn = psycopg2.connect(database="postgres", user="admin", password="adminPOST",
                                        host="localhost", port="5432")
        cur = conn.cursor()

        # Выполнение запроса для получения данных из таблицы "products"
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()

        # Заполнение таблицы данными
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

        # Закрытие соединения с базой данных
        cur.close()
        conn.close()

    def search_products(self):
        search_text = self.search_input.text()
        if search_text:
            # Подключение к базе данных PostgreSQL
            conn = psycopg2.connect(database="postgres", user="admin", password="adminPOST",
                                        host="localhost", port="5432")
            cur = conn.cursor()

            # Выполнение запроса для поиска данных в таблице "products"
            cur.execute("SELECT * FROM products WHERE product_name ILIKE %s", (f"%{search_text}%",))
            rows = cur.fetchall()

            # Заполнение таблицы найденными данными
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(i, j, item)

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()
        else:
            self.load_data()

    def update_data(self):
        # Получение выбранной строки и ячейки
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            col = selected_items[0].column()

            # Получение нового значения из ячейки
            new_value, ok = QInputDialog.getText(self, "Update Data", "Enter new value:")
            if ok:
                # Подключение к базе данных PostgreSQL
                conn = psycopg2.connect(database="postgres", user="admin", password="adminPOST",
                                        host="localhost", port="5432")
                cur = conn.cursor()

                # Получение ID продукта из выбранной строки
                product_id = self.table.item(row, 0).text()

                # Обновление значения в базе данных
                column_name = self.table.horizontalHeaderItem(col).text()
                cur.execute(f'UPDATE products SET "{column_name}" = %s WHERE id = %s',
                            (new_value, product_id))
                conn.commit()

                # Закрытие соединения с базой данных
                cur.close()
                conn.close()

                # Обновление отображаемых данных
                self.load_data()

    def delete_data(self):
        # Получение выбранной строки
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()

            # Получение ID продукта из выбранной строки
            product_id = self.table.item(row, 0).text()

            # Подключение к базе данных PostgreSQL
            conn = psycopg2.connect(database="postgres", user="admin", password="adminPOST",
                                    host="localhost", port="5432")
            cur = conn.cursor()

            # Удаление выбранной записи из базы данных
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

            # Обновление отображаемых данных
            self.load_data()

    def add_data(self):
        # Создание диалогового окна для ввода данных
        dialog = QInputDialog()
        dialog.setWindowTitle("Добавить запись")

        # Создание полей для ввода данных
        product_name, ok1 = dialog.getText(self, "Добавить запись", "Название продукта:")
        unit_of_measurement, ok2 = dialog.getText(self, "Добавить запись", "Единица измерения:")
        price_of_1_unit, ok3 = dialog.getDouble(self, "Добавить запись", "Цена за 1 шт:")
        amount, ok4 = dialog.getInt(self, "Добавить запись", "Количество:")
        actual_amount, ok5 = dialog.getInt(self, "Добавить запись", "Фактическое количество:")
        required_purchase, ok6 = dialog.getInt(self, "Добавить запись", "Необходимый закуп:")

        if ok1 and ok2 and ok3 and ok4 and ok5 and ok6:
            # Подключение к базе данных PostgreSQL
            conn = psycopg2.connect(database="postgres", user="admin", password="adminPOST",
                                    host="localhost", port="5432")
            cur = conn.cursor()

            # Вставка новой записи в базу данных
            cur.execute("INSERT INTO products (product_name, unit_of_measurement, price_for_1_unit, amount, actual_amount, required_purchase) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (product_name, unit_of_measurement, price_of_1_unit, amount, actual_amount, required_purchase))
            conn.commit()

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

            # Обновление отображаемых данных
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
