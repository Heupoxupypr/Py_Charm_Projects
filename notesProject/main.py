import sys
from os import system, name


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

    # парсим аргументы и их значения
    for count, arg in enumerate(arguments):
        # учитываем полные и сокращенные имена аргументов
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
