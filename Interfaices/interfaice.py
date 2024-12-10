import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QTabWidget, QVBoxLayout, QMessageBox
import psycopg2
from PyQt5.QtCore import Qt

class AddDataWindow(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Управление товарами")
        self.setWindowState(Qt.WindowMaximized)  # Устанавливаем окно в состояние максимизации

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(20, 20, self.width() - 40, self.height() - 40)  # Занимаем всю доступную площадь


        self.add_tab = QWidget()
        self.edit_tab = QWidget()
        self.search_tab = QWidget()


        self.tab_widget.addTab(self.add_tab, "Добавить товар")
        self.tab_widget.addTab(self.edit_tab, "Редактировать товар")
        self.tab_widget.addTab(self.search_tab, "Поиск")

        self.init_add_tab()
        self.init_edit_tab()
        self.init_search_tab()

    def init_add_tab(self):
        self.image_label = QLabel(self.add_tab)
        self.image_label.setText("Изображение:")
        self.image_label.move(20, 20)
        self.image_input = QLineEdit(self.add_tab)
        self.image_input.setGeometry(120, 20, 250, 20)

        self.title_label = QLabel(self.add_tab)
        self.title_label.setText("Название:")
        self.title_label.move(20, 60)
        self.title_input = QLineEdit(self.add_tab)
        self.title_input.setGeometry(120, 60, 250, 20)

        self.price_label = QLabel(self.add_tab)
        self.price_label.setText("Цена:")
        self.price_label.move(20, 100)
        self.price_input = QLineEdit(self.add_tab)
        self.price_input.setGeometry(120, 100, 250, 20)

        self.description_label = QLabel(self.add_tab)
        self.description_label.setText("Описание:")
        self.description_label.move(20, 140)
        self.description_input = QTextEdit(self.add_tab)
        self.description_input.setGeometry(120, 140, 250, 60)

        self.submit_button = QPushButton("Добавить", self.add_tab)
        self.submit_button.setGeometry(150, 210, 100, 30)
        self.submit_button.clicked.connect(self.add_data_to_table)

    def init_edit_tab(self):
        self.edit_id_label = QLabel(self.edit_tab)
        self.edit_id_label.setText("ID:")
        self.edit_id_label.move(20, 20)
        self.edit_id_input = QLineEdit(self.edit_tab)
        self.edit_id_input.setGeometry(120, 20, 250, 30)

        self.find_button = QPushButton("Найти", self.edit_tab)
        self.find_button.setGeometry(390, 20, 80, 30)
        self.find_button.clicked.connect(self.find_data_in_table)

        self.edit_image_label = QLabel(self.edit_tab)
        self.edit_image_label.setText("Картинка:")
        self.edit_image_label.move(20, 60)
        self.edit_image_input = QLineEdit(self.edit_tab)
        self.edit_image_input.setGeometry(120, 60, 250, 30)

        self.edit_title_label = QLabel(self.edit_tab)
        self.edit_title_label.setText("Название:")
        self.edit_title_label.move(20, 100)
        self.edit_title_input = QLineEdit(self.edit_tab)
        self.edit_title_input.setGeometry(120, 100, 250, 30)

        self.edit_price_label = QLabel(self.edit_tab)
        self.edit_price_label.setText("Цена:")
        self.edit_price_label.move(20, 140)
        self.edit_price_input = QLineEdit(self.edit_tab)
        self.edit_price_input.setGeometry(120, 140, 250, 30)


        self.edit_description_label = QLabel(self.edit_tab)
        self.edit_description_label.setText("Описание:")
        self.edit_description_label.move(20, 180)
        self.edit_description_input = QTextEdit(self.edit_tab)
        self.edit_description_input.setGeometry(120, 180, 250, 60)


        self.clear_button = QPushButton("Очистить", self.edit_tab)
        self.clear_button.setGeometry(280, 250, 80, 30)
        self.clear_button.clicked.connect(self.clear_fields)


        self.edit_submit_button = QPushButton("Редактировать", self.edit_tab)
        self.edit_submit_button.setGeometry(130, 250, 140, 30)
        self.edit_submit_button.clicked.connect(self.edit_data_in_table)


        self.delete_button = QPushButton("Удалить", self.edit_tab)
        self.delete_button.setGeometry(390, 250, 80, 30)
        self.delete_button.clicked.connect(self.delete_data_from_table)


        
    

    def init_search_tab(self):
        self.search_label = QLabel(self.search_tab)
        self.search_label.setText("Название:")
        self.search_label.move(20, 20)
        self.search_input = QLineEdit(self.search_tab)
        self.search_input.setGeometry(120, 20, 250, 30)

    
        self.search_button = QPushButton("Поиск", self.search_tab)
        self.search_button.setGeometry(390, 20, 80, 30)
        self.search_button.clicked.connect(self.search_data_by_title)


        self.search_result_label = QLabel(self.search_tab)
        self.search_result_label.setText("Результат:")
        self.search_result_label.move(20, 60)
        self.search_result_text = QTextEdit(self.search_tab)
        self.search_result_text.setGeometry(120, 60, 350, 200)
        self.search_result_text.setReadOnly(True)



    def clear_fields(self):
        self.edit_id_input.clear()
        self.edit_image_input.clear()
        self.edit_title_input.clear()
        self.edit_price_input.clear()
        self.edit_description_input.clear()


    def add_data_to_table(self):
        image = self.image_input.text()
        title = self.title_input.text()
        price = self.price_input.text()
        description = self.description_input.toPlainText()

        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        try:
            # Установление соединения с базой данных
            conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
            cur = conn.cursor()

            # SQL-запрос для вставки данных в таблицу
            sql_query = "INSERT INTO menu (image, title, price, description) VALUES (%s, %s, %s, %s)"
            data = (image, title, price, description)

            # Выполнение SQL-запроса с передачей данных
            cur.execute(sql_query, data)

            # Подтверждение изменений в базе данных
            conn.commit()

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

            QMessageBox.information(self, "Успех", "Товар добавлен в базу данных.")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при добавлении данных в таблицу:", error)

        # Очистка полей после добавления данных
        self.image_input.clear()
        self.title_input.clear()
        self.price_input.clear()
        self.description_input.clear()



    def find_data_in_table(self):
        id = self.edit_id_input.text()

        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        try:
            # Установление соединения с базой данных
            conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
            cur = conn.cursor()

            # SQL-запрос для поиска данных в таблице по идентификатору
            sql_query = "SELECT image, title, price, description FROM menu WHERE id = %s"
            data = (id,)

            # Выполнение SQL-запроса с передачей данных
            cur.execute(sql_query, data)

            # Извлечение найденных данных
            result = cur.fetchone()

            # Проверка наличия данных
            if result is not None:
                image, title, price, description = result

                # Заполнение полей данными, только если они не заполнены
                if self.edit_image_input.text().strip() == "":
                    self.edit_image_input.setText(image)
                if self.edit_title_input.text().strip() == "":
                    self.edit_title_input.setText(title)
                if self.edit_price_input.text().strip() == "":
                    self.edit_price_input.setText(price)
                if self.edit_description_input.toPlainText().strip() == "":
                    self.edit_description_input.setPlainText(description)

                QMessageBox.information(self, "Успех", "Товар найден.")
            else:
                QMessageBox.warning(self, "Ошибка", "Товар не найден.")

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при поиске данных в таблице:", error)


    def edit_data_in_table(self):
        id = self.edit_id_input.text()
        image = self.edit_image_input.text()
        title = self.edit_title_input.text()
        price = self.edit_price_input.text()
        description = self.edit_description_input.toPlainText()

        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        try:
            # Установление соединения с базой данных
            conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
            cur = conn.cursor()

            # SQL-запрос для обновления данных в таблице
            sql_query = "UPDATE menu SET image = %s, title = %s, price = %s, description = %s WHERE id = %s"

            data = (image, title, price, description, id)

            # Выполнение SQL-запроса с передачей данных
            cur.execute(sql_query, data)

            # Подтверждение изменений в базе данных
            conn.commit()

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

            QMessageBox.information(self, "Успех", "Товар обновлен в базе данных.")
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при редактировании данных в таблице:", error)

        # Очистка полей после редактирования данных
        self.edit_id_input.clear()
        self.edit_image_input.clear()
        self.edit_title_input.clear()
        self.edit_price_input.clear()
        self.edit_description_input.clear()


    def search_data_by_title(self):
        title = self.search_input.text()

        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        try:
            # Установление соединения с базой данных
            conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
            cur = conn.cursor()

            # SQL-запрос для поиска данных в таблице по названию
            sql_query = "SELECT id, image, title, price, description FROM menu WHERE title ILIKE %s"
            data = ('%' + title + '%',)

            # Выполнение SQL-запроса с передачей данных
            cur.execute(sql_query, data)

            # Извлечение найденных данных
            results = cur.fetchall()

            # Проверка наличия данных
            if results:
                search_results = ""
                for result in results:
                    id, image, title, price, description = result
                    search_results += f"ID: {id}\nНазвание: {title}\nЦена: {price}\nОписание: {description}\n\n"

                self.search_result_text.setPlainText(search_results)
            else:
                self.search_result_text.setPlainText("Товары не найдены.")

            # Закрытие соединения с базой данных
            cur.close()
            conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Ошибка при поиске")

    
    def delete_data_from_table(self):
        id = self.edit_id_input.text()

        # Параметры подключения к базе данных PostgreSQL
        db_host = 'localhost'
        db_name = 'postgres'
        db_user = 'admin'
        db_password = 'adminPOST'

        confirmation = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить товар?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            try:
                # Установление соединения с базой данных
                conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
                cur = conn.cursor()

                # SQL-запрос для удаления данных из таблицы
                sql_query = "DELETE FROM menu WHERE id = %s"
                data = (id,)

                # Выполнение SQL-запроса с передачей данных
                cur.execute(sql_query, data)

                # Подтверждение изменений в базе данных
                conn.commit()

                # Закрытие соединения с базой данных
                cur.close()
                conn.close()

                QMessageBox.information(self, "Успех", "Товар удален из базы данных.")
                self.clear_edit_fields()
            except (Exception, psycopg2.Error) as error:
                print("Ошибка при удалении данных из таблицы:", error)
        else:
            QMessageBox.information(self, "Отмена", "Удаление товара отменено.")

        self.clear_fields()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddDataWindow()
    window.showMaximized()
    sys.exit(app.exec_())
