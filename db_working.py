def to_db(db_table_file_name, db_class_name, names, texts, user_id=0, db_name="database.db"):
    try:
        Db, db_sess = create_session(db_table_file_name, db_class_name, db_name)[0], \
                      create_session(db_table_file_name, db_class_name, db_name)[1]
        db_string = Db()
        if type(names) == str:
            print(f"WARNING database logs | для записи был передан элемент, содержащий одну колонну в базе данных")
            exec(f"db_string.{names} = '{texts}'")
            print(f"database logs | Запись {texts} в таблицу {db_class_name}, "
                  f"колонна {names}. База данных: {db_table_file_name}")
            # write to database
            db_sess.add(db_string)
            print("database logs | Элемент добавлен успешно")
        elif type(names) == tuple:
            for i in range(len(names)):
                col_name = names[i]
                text = texts[i]
                if db_class_name == "Accounts":
                    current_username = user_id
                    exec(f"""db_string.user_id = '{[i.id for i in from_db("users", "Users", 
                                                                          {"id": current_username})][0]}'""")
                exec(f"db_string.{col_name} = '{text}'")
                print(f'database logs | Запись "{text}" в таблицу "{db_class_name}", '
                      f'колонна "{col_name}". База данных: "{db_table_file_name}"')
                # write to database
                db_sess.add(db_string)
                print("database logs | Элемент добавлен успешно")
        db_sess.commit()
        db_sess.close()
    except Exception as e:
        print(f"ERROR database logs | При создании элемента произошла ошибка\n{e}")


# в функцию передаётся имя бд (name.db), имя таблицы, как в файле в папке data (users),
# имя класса из этого файла (Users), имя столбца из таблицы (username), текст, который нужно записать ("Hello world!")


def from_db(db_table_file_name, db_class_name, filter_d=None, db_name="database.db"):
    try:
        db, db_sess = create_session(db_table_file_name, db_class_name, db_name)[0], \
                      create_session(db_table_file_name, db_class_name, db_name)[1]
        if filter_d is None:
            get_from_db = db_sess.query(db).all()
            return get_from_db
        else:
            s = ""
            for i in filter_d:
                if type(filter_d[i]) == str:
                    s += f"db.{i} == '{filter_d[i]}', "
                else:
                    s += f"db.{i} == {filter_d[i]}, "
            s = s.strip(", ")
            lst = []
            exec(f"for el in db_sess.query(db).filter({s}):lst.append(el)")
            return lst
    except Exception as e:
        print(f"ERROR database logs | При получении элемента(ов) произошла ошибка\n{e}")


# взять элемент из бд

def change_db(db_table_file_name, db_class_name, changing, filter_d=None, db_name="database.db"):
    try:
        db, db_sess = create_session(db_table_file_name, db_class_name, db_name)[0], \
                      create_session(db_table_file_name, db_class_name, db_name)[1]
        change_s = "{"
        for item in changing:
            if type(changing[item]) == str:
                change_s += f"db.{item}: '{changing[item]}', "
            else:
                change_s += f"db.{item}: {changing[item]}, "
        change_s = change_s.strip(", ")
        change_s += "}"
        if filter_d is None:
            print(f"WARNING database logs | Изменение таблицы {db_class_name}")
            exec(f"db_sess.query(db).update({change_s})")
            print("Успешно")
            db_sess.commit()
            print(f'database logs | Таблица изменена успешно')
        else:
            s = ""
            for i in filter_d:
                if type(filter_d[i]) == str:
                    s += f"db.{i} == '{filter_d[i]}', "
                else:
                    s += f"db.{i} == {filter_d[i]}, "
            s = s.strip(", ")
            print(f'database logs | Изменение элемента таблицы')
            exec(f"db_sess.query(db).filter({s}).update({change_s})")
            db_sess.commit()
            print(f'database logs | Элемент таблицы изменён успешно')
    except Exception as e:
        print(f"ERROR database logs | При изменении элемента(ов) произошла ошибка\n{e}")


def remove_from_db(db_table_file_name, db_class_name, filter_d=None, db_name="database.db"):
    try:
        db, db_sess = create_session(db_table_file_name, db_class_name, db_name)[0], \
                      create_session(db_table_file_name, db_class_name, db_name)[1]
        if filter_d is None:
            print(f"WARNING database logs | Удаление таблицы {db_class_name}")
            exec(f"db_sess.query(db).delete()")
            db_sess.commit()
            print(f'database logs | Удаление прошло успешно')
        else:
            s = ""
            for i in filter_d:
                if type(filter_d[i]) == str:
                    s += f"db.{i} == '{filter_d[i]}', "
                else:
                    s += f"db.{i} == {filter_d[i]}, "
            s = s.strip(", ")
            print(f'database logs | Удаление элемента(ов) из базы данных')
            exec(f"db_sess.query(db).filter({s}).delete()")
            db_sess.commit()
            print(f'database logs | Удаление прошло успешно')
    except Exception as e:
        print(f"ERROR database logs | При удалении элемента(ов) произошла ошибка\n{e}")


def create_session(db_table_file_name, db_class_name, db_name="database.db"):
    try:
        from data import db_session
        import data
        db_session.global_init(f"db/{db_name}")
        db_sess = db_session.create_session()
        db = eval(f"data.{db_table_file_name}.{db_class_name}")
        print(f'database logs | Сессия создана')
        return db, db_sess
    except Exception as e:
        print(f"ERROR database logs | При создании сессии произошла ошибка\n{e}")

# created by tehno_py (19.04.22)
