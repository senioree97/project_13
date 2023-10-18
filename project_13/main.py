from datetime import datetime

if __name__ == "__main__":
    from classes.uiclasses import ConsoleUserInterface    
    from classes.abclasses import AddressBook, Contact
    from classes.notes import Note 
    from sorter import clear
else:
    from .classes.uiclasses import ConsoleUserInterface    
    from .classes.abclasses import AddressBook, Contact
    from .classes.notes import Note
    from .sorter import clear




def main():
    global ui, ab
    ui = ConsoleUserInterface()
    ab = AddressBook()  

    ui.show_start_message()
    ab.load()
    
    while True:
        message = ui.user_input(f'\033[94m >>> \033[0m')
        cmd, data = parser(message)
        cmd(*data)


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except Exception as e:
            ui.show_message(e)
    return wrapper


@ input_error
def add_command(surname):
     if surname in ab:
         ui.show_red_message(f'Contact with surname {surname} already exists')
     else:
         ab.add_contact(ui, Contact(surname))

@ input_error
def change_command(surname):
     if surname in ab:
        ab.update_contact(ui, ab[surname])         
     else:
        ui.show_red_message(f'No contacts with surname {surname}')

def find_command(text, *_):
    ui.show_message("\n".join(str(contact) for contact in ab.values() if text in str(contact)))


def find_tag_command(tag, *_):
    ui.show_message("\n".join(str(note) for note in ab.notes if tag in note.tags))


def delete_all_command(*_):
    ab.delete_all(ui)


def delete_command(surname):
    if surname in ab:
        ab.delete_contact(ui, ab[surname])
    else:
        ui.show_red_message(f'No contacts with surname {surname}')


def help_command(*_):
    ui.show_help()


def unknown_command():
    ui.show_red_message('Unknown command')


def show_all_command(*_):
    ui.clear_screen()
    for contact in ab.values():
            ui.show_message(contact)

def show_contacts_command(*_):
    ui.show_green_message('Enter the number of contacts per page (default=10)  [Enter to skip]:')
    number_contacts = ui.user_input('>')
    if number_contacts:
        ab.show_contacts(ui, number_contacts)
    else:
        ab.show_contacts(ui)


def sort_command(*_):
    ui.show_green_message("Enter path you want to be sorted")
    dir = ui.user_input('>')
    clear(dir)
    ui.show_green_message("Successfully sorted!")


@ input_error    
def add_note_command(*_):
    ui.show_green_message('Here starts your new note:')
    new_note = ui.user_input('>')
    ui.show_green_message('Wanna add some tags? (comma separated)  [Enter to skip]:')
    tags = ui.user_input('>').replace(',',' ').split(' ')
    new_note_obj = Note(new_note, datetime.now().strftime('%H:%M:%S  %Y-%m-%d'))
    if tags:
        new_note_obj.add_tag(tags)
    ab.notes.append(new_note_obj)


def show_notes(*_):
    for note in ab.notes:
        ui.show_message(note)


def exit_command(*_):
    ui.show_green_message(f"\nGood bye!\n\n")
    ab.save()
    exit()
    

@ input_error
def nearby_birthdays_command(n_days, *_):
    ab.nearby_birthday(ui, n_days)


@ input_error
def parser(text):
    closest_cmd = ''
    text = f"{text} "
    try:    
        for cmd, kwds in CMD_LIST.items():
            for kwd in kwds:
                if text.lower().startswith(f'{kwd} '):
                    return cmd, text[len(kwd):].strip().split(" ")        
        closest_cmd = levenshtein_distance(text.strip().split()[0].lower())
        if closest_cmd:
            return parser(text.replace(text.strip().split()[0], closest_cmd, 1))       
    except IndexError as e:        
        return unknown_command, [] 
    return unknown_command, []


def levenshtein_distance(str_to_check):
    distance = len(str_to_check)
    possible_cmd = None
    for kwds in CMD_LIST.values():
        for cmd in kwds:
            m, n = len(str_to_check), len(cmd)
            dp = [[0 for _ in range(n+1)] for _ in range(m+1)]
            for i in range(m+1):
                dp[i][0] = i
            for j in range(n+1):
                dp[0][j] = j
            for i in range(1, m+1):
                for j in range(1, n+1):
                    substitution_cost = 0 if str_to_check[i-1] == cmd[j-1] else 1
                    dp[i][j] = min(dp[i-1][j] + 1,
                                dp[i][j-1] + 1,
                                dp[i-1][j-1] + substitution_cost) 
            if dp[m][n] < distance:
                distance = dp[m][n]
                possible_cmd = cmd
    if distance < len(str_to_check):
        ui.show_message(f'Did you mean "{possible_cmd} "?')
        if ui.user_input('Y/n:  ').lower() in ('y', 'yes'):
            return possible_cmd


CMD_LIST = {
    find_tag_command: ("find tag",),
    show_notes: ("show note", "show notes"),
    add_note_command: ("add notes", "add note"),
    add_command: ("add", "+"),
    find_command: ("find",),
    change_command: ("change",),
    show_all_command: ("show all", "show"),
    show_contacts_command: ("pages", "contacts"),
    delete_all_command: ("delete all", "remove all", "clean"), 
    delete_command: ("delete", "del", "remove"),
    help_command: ("help", "h", "?"),
    exit_command: ("exit", "quit", "goodbye",  "."),
    sort_command: ("sort",),
    nearby_birthdays_command: ("nearby bds", "nearby birthdays")
}


if __name__ == "__main__":
    main()