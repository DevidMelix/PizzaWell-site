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
            sql_query = "UPDATE add_for_menu SET image = %s, title = %s, price = %s, description = %s WHERE id = %s"
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
