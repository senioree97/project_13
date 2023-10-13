def add_command():
    ... 
def find_command():
    ...
def change_command():
    ...
def show_all_command():
    ...
def delete_all_command():
    ...
def delete_command():
    ...
def help_command():
    ...
def exit_command():
    ...
def sort_command():
    ...
def unknown_command():
    ...



def parser(ui, text):
    for cmd, kwds in CMD_LIST.items():
        for kwd in kwds:
            if text.strip().lower().split()[0] == kwd:
                return cmd, text[len(kwd):].strip().split(" ")
    
    closest_cmd = levenshtein_distance(text.strip().split()[0].lower())
    if closest_cmd:
       return parser(ui, text.replace(text.strip().split()[0], closest_cmd, 1)) 

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
        print(f'Did you mean "{possible_cmd} "?')
        if input('Y/n:  ').lower() in ('y', 'yes'):
            return possible_cmd


CMD_LIST = {
    add_command: ("add", "+"),
    find_command: ("find",),
    change_command: ("change",),
    show_all_command: ("show all", "show"),
    delete_all_command: ("delete all", "remove all"),
    delete_command: ("delete", "del", "remove"),
    help_command: ("help", "h", "?"),
    exit_command: ("exit", "quit", "goodbye",  "."),
    sort_command: ("sort"),
}