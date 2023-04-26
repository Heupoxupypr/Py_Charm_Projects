import sys
import json
from datetime import time, date, datetime
import re

if __name__ == "__main__":
    if len(sys.argv) in [2, 3, 4, 5, 6, 7, 8]:

        # считываем аргументы
        arguments = [sys.argv[arg] for arg in range(1, len(sys.argv), 2)]
        # считываем значения аргументов
        values = [sys.argv[arg] for arg in range(2, len(sys.argv), 2)]

        # print(arguments)
        # print(values)


        def save_json_file(data):
            with open('task_note.json', 'w') as json_data:
                json.dump(data, json_data)


        # Функция считывания аргументов из консоли
        def read_console():
            last_val = ''
            note_title = ''
            note_msg = ''

            # TODO можно обернуть в функцию
            try:
                with open('task_note.json', 'r') as json_data:
                    try:
                        data = json.load(json_data)
                        # print(data, end='\n')
                    except json.decoder.JSONDecodeError:
                        print('decode error')
                        data = {}
                        last_val = 0
                    else:
                        last_val = len(data.items())
                        pass
                        # print(f'Data JSON:{data}')
            except FileNotFoundError:
                print('no found')
                f = open('task_note.json', "x")
                f.write('')
                f.close()
                data = {}
                last_val = 0

            # парсим аргументы и их значения
            for count, arg in enumerate(arguments):
                # учитываем полные и сокращенные имена аргументов

                if arg == '--title' or arg == '-t':
                    note_title = str(values[count])

                elif arg == '--message' or arg == '-m':
                    note_msg = str(values[count])
                    data[str(last_val)] = {"id": str(last_val),
                                           "head": str(note_title),
                                           "time": str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S')),
                                           "msg": str(note_msg)}

                    with open('task_note.json', 'w') as json_data:
                        json.dump(data, json_data)
                    print('Note was sucessful created')

                elif arg == '--view' or arg == '-v':
                    if values[count] == 'all':
                        for note in data.values():
                            print(note, end='\n')
                    if values[count] == 'last':
                        print(data[f'{last_val}'])

                elif arg == '--delete' or arg == '-d':
                    try:
                        data.pop(re.findall("\d+", values[count])[0])
                    except KeyError:
                        print(f"Note with key '{values[count][0]}' doesn't exist")
                    else:
                        for note in data.values():
                            print(note, end='\n')
                        save_json_file(data)
                        print("Note was sucessful deleted")

                elif arg == '--change' or arg == '-c':
                    for id in data.items():
                        # print(values[count])
                        if id[1]['id'] == values[count]:
                            note_title = id[1]['head']
                            last_val = id[1]['id']
                    last_val = values[count]
                    print("Note was sucessful changed")

                elif arg == '--add' or arg == '-a':
                    for count, arg in enumerate(arguments):
                        if arg == '--title' or arg == '-t':
                            note_title = str(values[count])
                            # print(note_title)
                            break
                    for count, arg in enumerate(arguments):
                        if arg == '--message' or arg == '-m':
                            note_msg = str(values[count])
                            # print(note_msg)
                            break

                    last_val += 1
                    # print(last_val)

                elif arg == '--help' or arg == '-h':
                    print('\nИспользование')
                    print("--title, -t\t заголовок заметки")
                    print("--message, -m\t тело заметки")
                    print("--view, -v\t посмотреть записи")
                    print("--change, -c\t редактировать запись с заданным id")
                    print("    Аргументы\t[all]\tвсе записи")
                    print("\t\t[last]\tпоследняя запись")
                    print("--delete, -d\t удалить запись по её id")
                    print('Пример записи крманды: \tpython notes.py -a note -t "Заголовок заметки" -m "Тело заметки"')
                    print('\t\t\tДанная команда создаст заметку с заголовком "Заголовок заметки" и записью ' \
                          "Тело заметки")
                    print("\n")

                else:
                    pass


        read_console()
    else:
        # ручной ввод
        pass
