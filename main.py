import sys
from logging import error, getLogger
from itertools import islice

import password_util

BATCH_SIZE = 1000
correct, incorrect = 0, 0
CORRECT_FILE = 'correct_passwords.txt'
INCORRECT_FILE = 'incorrect_passwords.txt'


def print_help():
    print("Incorrect usage of an application. Usage:\n"
          "\t- python3 main.py --report <path to file with passwords> <constraints>\n"
          "\t- python3 main.py --check <password> {constraints}\n"
          "\t- python3 main.py --generate {constraints}\n\n"
          "\t- python3 main.py --massive-generate <number of passwords> {constraints}\n\n"
          "Constraints should be provided in the following form:\n"
          "\t- <min length> <max length> [--upper] [--specials] [--digits]\n\n"
          "Arguments in square brackets are optional. <min length> should be less than or equal <max length.\n"
          "If password contains space character, please, surround it with quotation marks.")

    exit(0)


def extract_preferences(arguments):
    if len(arguments) == 0:
        print_help()

    local_upper_case = False
    local_special_chars = False
    local_numbers = False

    local_min_length = 0
    local_max_length = 256

    try:
        local_min_length = int(arguments[0])
    except ValueError:
        error(f'Unexpected token: {arguments[0]}, expected: integer value of min password length.\n\n')
        print_help()

    try:
        local_max_length = int(arguments[1])
    except ValueError:
        error(f'Unexpected token: {arguments[1]}, expected: integer value of max password length.\n\n')
        print_help()

    for i in arguments[2:]:
        if i == '--upper':
            local_upper_case = True
        elif i == '--specials':
            local_special_chars = True
        elif i == '--digits':
            local_numbers = True
        else:
            error(f'Unexpected token: {i}, expected: "--upper", "--specials" or "--digits".\n\n')
            print_help()

    local_preferences = password_util.Preferences(min_length=local_min_length, max_length=local_max_length,
                                                  upper_case=local_upper_case, special_chars=local_special_chars,
                                                  numbers=local_numbers)

    return local_preferences


def process(local_batch, local_preferences: password_util.Preferences):
    global correct, incorrect

    for pwd in local_batch:
        pwd = pwd.strip()

        valid = password_util.check_password(pwd, local_preferences)
        if valid:
            with open(CORRECT_FILE, 'a') as corrects_file:
                corrects_file.write(pwd)
                corrects_file.write('\n')
            correct += 1
        else:
            with open(INCORRECT_FILE, 'a') as incorrect_file:
                incorrect_file.write(pwd)
                incorrect_file.write('\n')
            incorrect += 1


def clear_files_contents():
    with open(CORRECT_FILE, 'w'):
        pass

    with open(INCORRECT_FILE, 'w'):
        pass


args = sys.argv[1:]

if len(args) == 1:
    print_help()

if args[0] == '--report':
    logger = getLogger()
    logger.disabled = True

    file_name = args[1]
    preferences = extract_preferences(args[2:])

    clear_files_contents()

    with open(file_name, 'r') as f:
        for n_lines in iter(lambda: tuple(islice(f, BATCH_SIZE)), ()):
            process(n_lines, preferences)

    print('All correct passwords were written to files: correct_passwords.txt and incorrect_passwords.txt')
    print(f'Number of correct passwords: {correct}')
    print(f'Number of incorrect passwords: {incorrect}')
elif args[0] == '--check':
    password = args[1]
    preferences = extract_preferences(args[2:])

    ok = password_util.check_password(password, preferences)

    print('=' * 13)
    if ok:
        print("Valid password!")
    else:
        print("Invalid password!")
elif args[0] == '--generate':
    preferences = extract_preferences(args[1:])
    print('Generated password: ', end='')
    print(password_util.generate_password(preferences))
elif args[0] == '--massive-generate':
    n = 0
    try:
        n = int(args[1])
    except ValueError:
        error(f'Unexpected token: {args[1]}, expected: integer value of the number of passwords.\n\n')
        print_help()
    preferences = extract_preferences(args[2:])

    for _ in range(n):
        print(password_util.generate_password(preferences))
else:
    print_help()
