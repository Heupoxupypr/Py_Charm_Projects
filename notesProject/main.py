import sys

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        console_mode()
    else:
        console_help()
