# Define constants.
import os

BILL_TITLE = ['Water', 'Sewer', 'Electric', 'Gas', 'Cellular', 'Internet']
MONTH_DICT = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar',
    '04': 'Apr', '05': 'May', '06': 'Jun',
    '07': 'Jul', '08': 'Aug', '09': 'Sep',
    '10': 'Oct', '11': 'Nov', '12': 'Dec'
}
ERROR_STRING = 'Invalid input. Exiting to menu.\n'
DONE_TEXT = 'Saved to file.'
FILE_PATH = 'bills.txt'


def build_insert_string(title_selection: int,
                        date: str, value: float,
                        num_roommates: any,
                        user_title: any
                        ) -> str:
    # Build title.
    if user_title is not None:
        title = user_title.ljust(8)
    else:
        title = BILL_TITLE[title_selection - 1].ljust(8)

    # Format date and due.
    date_list = date.split('/')
    month = MONTH_DICT[date_list[0]]
    day = date_list[1]
    year = date_list[2]

    # Calculate roommate's half.
    roommate_due = 'NA'.ljust(7)
    if num_roommates is not None:
        roommate_value = value / num_roommates
        roommate_value = '%.2f' % round(roommate_value, 2)
        roommate_due = '$' + str(roommate_value).ljust(6)

    # Format value and due.
    value = '%.2f' % value
    due = '$' + value.ljust(6)

    # Build and return final string.
    return f' {title} - {month} {day} {year} - {due} - {roommate_due} - NOT PAID'


def update_list(old_line: str, new_line: str, file_list: list) -> list:
    for line in file_list:
        if old_line == line:
            line_index = file_as_list.index(line)
            file_list.pop(line_index)
            file_list.insert(line_index, new_line)
    return file_list


# Main application.
if __name__ == '__main__':
    print('Welcome to Nector-Kilo\'s Bill Calculator!')
    while True:

        # Menu selection.
        selection_switch = None
        try:
            selection_switch = int(input(
                'Please make a selection:\n'
                '[1]-View [2]-Insert [3]-Update [4]-Edit [5]-Exit\n'
            ))
        except ValueError:
            print('Invalid Selection.\n', end='')

        # View selection.
        if selection_switch == 1:
            print('+---------+-------------+---------+---------+--------+')
            print('| Bill    | Due Date    | Total   | Split   | Status |')
            print('+---------+-------------+---------+---------+--------+')
            with open(FILE_PATH, 'r') as file:
                print(file.read(), end='')

        # Insert selection.
        if selection_switch == 2:
            while True:

                # Build title prompt, get user input, handle errors.
                title_input = None
                try:
                    title_input = int(input(
                        '[1]-Water [2]-Sewer [3]-Electric [4]-Gas [5]-Cellular [6]-Internet [7]-Other\n'
                        'Select your bill: '
                    ))
                except ValueError:
                    print(ERROR_STRING, end='')
                    break

                # Handle if title not in range.
                if title_input < 1 or title_input > 7:
                    print(ERROR_STRING, end='')
                    break

                # If user chose custom, build it.
                user_title_input = None
                if title_input == 7:
                    user_title_input = 'xxxxxxxxx'
                    while len(user_title_input) > 8:
                        user_title_input = input('What would you like to call this bill?: ')
                        if len(user_title_input) > 8:
                            print('Must have no more than 8 characters.')

                # Build date prompt, get user input, handle errors.
                date_input = input('When is it due?[MM/DD/YYYY]: ')

                # Handle if date not in correct format.
                if date_input.count('/') != 2:
                    print(ERROR_STRING, end='')
                    break

                # Handle if date not in correct length.
                if len(date_input) != 10:
                    print(ERROR_STRING, end='')
                    break

                # Handle if month is invalid.
                if date_input.split('/')[0] not in MONTH_DICT.keys():
                    print(ERROR_STRING, end='')
                    break

                # Build due prompt, get user input, handle if not float.
                try:
                    due_input = float(input('How much is due?: $'))
                except ValueError:
                    print(ERROR_STRING, end='')
                    break

                # Handle if has roommate.
                num_of_roommates = None
                try:
                    roommate_switch = input('Do you split your bill?[Y/N]: ').lower()
                    if roommate_switch == 'y':
                        num_of_roommates = int(input('How many total household members?: '))
                except ValueError:
                    print(ERROR_STRING, end='')
                    break

                # Build data string.
                data_string = build_insert_string(
                    title_input,
                    date_input,
                    due_input,
                    num_of_roommates,
                    user_title_input
                )

                # Write to file.
                with open(FILE_PATH, 'a') as file:
                    file.write(data_string + '\n')
                print(DONE_TEXT)
                break

        # Update selection.
        if selection_switch == 3:
            file_as_list = []
            not_paid_list = []

            # Generate prompts and read in file as list.
            with open(FILE_PATH, 'r') as file:
                for line in file:
                    file_as_list.append(line)
                    if 'NOT PAID' in line:
                        not_paid_list.append(line)
            print('+-------------+-------------+---------+---------+--------+')
            print('|    Bill     | Due Date    | Total   | Split   | Status |')
            print('+-------------+-------------+---------+---------+--------+')
            for i in not_paid_list:
                print(f'[{not_paid_list.index(i) + 1}]-{i}', end='')

            # Try to select line.
            while True:
                try:
                    line_select = int(input('Select the bill to update: '))
                except ValueError:
                    print(ERROR_STRING, end='')
                    break

                # Try to change line and update list.
                try:
                    selected_line = not_paid_list[line_select - 1]
                    changed_line = selected_line.replace(' NOT PAID', ' PAID')
                    file_as_list = update_list(selected_line, changed_line, file_as_list)
                except IndexError:
                    print(ERROR_STRING, end='')
                    break

                # Write to file.
                else:
                    with open(FILE_PATH, 'w') as file:
                        for line in file_as_list:
                            file.write(line)
                    print(DONE_TEXT)
                    break

        # Edit selection.
        if selection_switch == 4:
            print('Opening in notepad.exe.')
            os.startfile(FILE_PATH)

        # Exit selection.
        if selection_switch == 5:
            print('Exiting.')
            break
