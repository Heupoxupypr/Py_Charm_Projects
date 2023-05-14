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
            # time_note = str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S'))
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
            gui_mode()

        else:
            console_help()


def arg_parser(args):
    args.pop(0)
    args_dict = {}

    # change all arguments name to short name
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
        # else:
        #     data_to_json = {"id": str(args[2]),
        #                     "time": str(datetime.now().strftime('%d.%m.%Y - %H:%M:%S')),
        #                     "title": str(args[0]),
        #                     "msg": str(args[1])}
        #     data[args[2]] = data_to_json
        #     save_json_file(data)
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


def init_gui():
    clear_screen()
    sys.stdout.flush()
    print('Welcome to Manual mode', file=sys.stdout, flush=False)
    print('Please type \'help\' for instructions or CTRL+Z for exit')
    print('--------------------------------------------------------')
    print('                     NOTE EDITOR v.1.0                  ')
    print('                      List of commands                  ')
    print('                                                        ')
    print('--------------------------------------------------------')
    print('1) add note')
    print('2) change note')
    print('3) delete note')
    print('4) view all notes')
    print('5) view last note')
    print('0) exit from application')
    print('--------------------------------------------------------')
    cmd = input("Enter command:").strip().lower()
    return cmd


def gui_mode():
    clear_screen()
    sys.stdout.flush()

    while True:
        try:
            data = read_json_file()
            # arg_dict = arg_parser(sys.argv)
            try:
                last_val = max(list(map(int, data.keys()))) + 1
            except ValueError:
                last_val = 0

            cmd = init_gui()
            if cmd == 'выход' or cmd == 'exit' or cmd == '0':
                sys_exit()

            elif cmd == "view all" or cmd == '4':
                clear_screen()
                if len(data.values()) == 0:
                    print('no notes added yet...')
                else:
                    for note in data.values():
                        print(note, end='\n')
                input("press any key to continue...")

            elif cmd == "view last" or cmd == '5':
                clear_screen()
                if len(data.values()) == 0:
                    print('no notes added yet...')
                else:
                    print(data[f'{last_val - 1}'])
                input("press any key to continue...")

            elif cmd == "add note" or cmd == '1':
                title = input('Введите название заголовка: ')
                message = input('Введите заметку: ')
                note_add(title, message, last_val, verbose=True)

            elif cmd == "change note" or cmd == '2':

                while True:
                    for i in data.values():
                        print(i)
                    note_id = input('Введите id заметки: ')

                    try:
                        data_note = data[note_id]

                    except KeyError:
                        print('Заметки с указанным id нет')
                        time.sleep(1)
                    else:
                        title = data_note['title']
                        message = data_note['msg']
                        last_val = data_note['id']
                        title_input = input('Введите новое название заголовка (enter - пропустить): ')

                        if len(title_input) > 0:
                            title = title_input

                        time.sleep(0.1)

                        message_input = input('Отредактируйте содержание заметки (enter - пропустить): ')

                        if len(message_input) > 0:
                            message = message_input

                        time.sleep(0.1)
                        note_add(title, message, last_val, verbose=False)
                        print('Заметка отредактирована')
                        break

            elif cmd == "delete note" or cmd == '3':
                if len(data.values()) == 0:
                    print('no notes added yet...')
                    input("press any key to continue...")
                else:
                    for i in data.values():
                        print(i)
                    while True:
                        note_id = input('Enter id to delete (enter: go to main menu): ')

                        try:
                            data_note = data[note_id]

                        except KeyError:
                            if len(note_id) == 0:
                                break
                            else:
                                print(len(note_id))
                                print('Заметки с указанным id нет')
                            time.sleep(1)
                        else:
                            data.pop(data_note['id'])
                            save_json_file(data)
                            print(f'Note with id={note_id} was deleted')
                            input("Press any key to continue...")
                            break

            elif cmd == 'help':
                dialog_help()

            else:
                print("Команда не распознана")
                time.sleep(1)
        except (EOFError, KeyboardInterrupt):
            sys_exit()


def sys_exit():
    print('Exit...')
    sys.exit()


def dialog_help():
    clear_screen()
    print('-------------------------------------------------')
    print('                     HELP                        ')
    print('                 List of commands                ')
    print('-------------------------------------------------')
    print('1) add note')
    print('2) change note:')
    print('3) delete note:')
    print('4) view all notes:')
    print('5) view last note:')
    print('0) exit from application:')
    print('-------------------------------------------------')
    input("\n\npress Enter to continue...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        console_mode()
    else:
        console_help()
