from datetime import time, datetime
import time
import json
import sys
from os import system, name
import re


def save_json_file(data):
    with open('task_note.json', 'w') as json_data:
        json.dump(data, json_data)


def open_file():
    new_file_flag = False
    try:
        # read file
        open('task_note.json', 'r')
    except FileNotFoundError:
        # exception
        print('file not found...')
        print('attempt to create it...')
        f = open('task_note.json', "x")
        f.write('')
        f.close()
        new_file_flag = True
    finally:
        return new_file_flag


def read_json_file():
    if open_file():
        print('file created')
        return {}
    else:
        with open('task_note.json', 'r') as raw_file_data:
            try:
                json_data = json.load(raw_file_data)
            except json.decoder.JSONDecodeError:
                json_data = {}
            return json_data


def console_mode():
    note_title = ''
    note_msg = ''
    arg_dict = arg_parser(sys.argv)
    # acronyms_dict = {}
    arguments = list(arg_dict.keys())
    values = list(arg_dict.values())
    data = read_json_file()
    try:
        last_val = max(list(map(int, data.keys()))) + 1
    except ValueError:
        last_val = 0

    # parse arguments and data
    for count, arg in enumerate(arguments):
        # full name or short name of arguments
        if arg == '-a':
            time_note = str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S'))
            for _arg in arguments:
                if _arg == '-t' or _arg == '--title':
                    note_title = arg_dict[_arg]
                if _arg == '-m' or _arg == '--msg':
                    note_msg = arg_dict[_arg]
            if len(note_title) + len(note_msg) != 0:
                note_add(note_title, note_msg, last_val, data, verbose=False)
            # print("Note was successful added")
            break

        elif arg == '-v':
            if len(data.values()) > 0:
                if values[count] == 'all':
                    if len(data.values()) > 0:
                        for note in data.values():
                            print(note, end='\n')
                if values[count] == 'last':
                    if len(data.values()) > 0:
                        print(data[f'{last_val - 1}'])
                break
            else:
                print('No notes added yet...')

        elif arg == '-d':
            try:
                data.pop(re.findall("\d+", values[count])[0])
            except KeyError:
                print(f"Note with key '{values[count][0]}' doesn't exist")
            else:
                for note in data.values():
                    print(note, end='\n')
                save_json_file(data)
                # print("Note was successful deleted")
            break

        elif arg == '-c':
            last_val = arg_dict[arg]
            note_title = data[last_val]['title']
            note_msg = data[last_val]['msg']
            for _arg in arguments:
                if _arg == '-t' or _arg == '--title':
                    note_title = arg_dict[_arg]

                if _arg == '-m' or _arg == '--msg':
                    note_msg = arg_dict[_arg]
            note_add(note_title, note_msg, last_val, data, verbose=False)
            # print("Note was successful changed")
            break

        elif arg == '-h':
            console_help()

        elif arg == '-g' or arg == '--gui':
            gui_mode(data, last_val)

        else:
            console_help()


def arg_parser(args):
    args.pop(0)
    args_dict = {}

    # change all arguments name to short name
    z = ''
    for count, arg in enumerate(args):
        if arg.startswith('-'):
            z = re.search("^--\w+", arg)
            if z:
                # print(z.group()[1:3])
                try:
                    args_dict[z.group()[1:3]] = args[count + 1]
                except IndexError:
                    args_dict[z.group()[1:3]] = ""
                    # pass
            else:
                try:
                    args_dict[arg] = args[count + 1]
                except IndexError:
                    args_dict[arg] = ''
        elif arg == 'ADD':
            args_dict["-a"] = ''
        elif arg == "CHANGE":
            args_dict["-c"] = args[count + 1]
        elif arg == "DELETE":
            args_dict["-d"] = args[count + 1]
        elif arg == "VIEW":
            args_dict["-v"] = args[count + 1]
        elif arg == "GUI":
            args_dict["-g"] = ""
        elif arg == 'HELP':
            args_dict["-h"] = ""

    return args_dict


def note_add(*args, verbose=True):
    # print(args)
    # 0 - title
    # 1 - message
    # 2 - id
    # 3 - json data
    data: dict = {}
    data_to_json = {}
    try:
        data = args[3]

    except IndexError:
        data = read_json_file()
        if len(list(data.keys())) == 0:
            data_to_json = {args[2]: {"id": str(args[2]),
                                      "time": str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S')),
                                      "title": str(args[0]),
                                      "msg": str(args[1])}}
            save_json_file(data_to_json)
        else:
            data_to_json = {"id": str(args[2]),
                            "time": str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S')),
                            "title": str(args[0]),
                            "msg": str(args[1])}
            data[args[2]] = data_to_json
            save_json_file(data)
    else:
        data_to_json = {"id": str(args[2]),
                        "time": str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S')),
                        "title": str(args[0]),
                        "msg": str(args[1])}
        data[args[2]] = data_to_json
        save_json_file(data)

    finally:
        if verbose:
            print(data_to_json)
            input("Press any key to continue...")


def console_help():
    clear_screen()
    print('Console mode')
    print('Использование: --команда (-короткое написание) значение команды')
    print('Синтаксиc')
    print('Основные команды:')
    print("ADD (--add, -a)                  добавить заметку (с необязательным значением 'note')")
    print("CHANGE (--change, -c)            редактировать запись с заданным id")
    print("DELETE (--delete, -d)            удалить запись по её id")
    print("GUI (--gui, -g)                  переводит работу программы в графический режим")
    print("HELP (--help, -h)                вывести справку")
    print("VIEW (--view, -v) [all, last]    посмотреть все (последнюю) записи")
    print('Необязательные ключи:')
    print("--title, -t                      заголовок заметки")
    print("--message, -m                    тело заметки")

    print('[Пример]:')
    print('python notes.py -a note -t "Заголовок заметки" -m "Тело заметки"\tсоздаст заметку '
          'с заголовком "Заголовок заметки" и записью "Тело заметки"')
    print('python notes.py --view all   выведет все существующие заметки на экран')
    print('python notes.py --delete 5   удалит заметку, id которой равен 5')
    print("\n")


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        console_mode()
    else:
        console_help()
