import datetime

def split_data(date_text):  # getting date from string
    day_and_hour = date_text.split(" ")
    day = day_and_hour[0].split("-")
    hour = day_and_hour[1].split(":")
    y = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(hour[0]), int(hour[1]))
    return y


def read_file(f_name: str):
    file = open(f_name, 'r')
    text = file.read()
    file.close()

    return text


def write_to_file(f_name: str, line):
    file = open(f_name, "w", encoding='utf-8')
    file.write(line)
    file.close()


def get_bases(f_name, last_done_base = "0") -> list:
    text = read_file(f_name)
    list_of_bases = text.split(',')
    print('Found ' + str(len(list_of_bases)) + " bases:")
    [print(b_id) for b_id in list_of_bases]
    
    if last_done_base == "0":
        return list_of_bases
        
    return list_of_bases[list_of_bases.index(last_done_base):]


def add_letter_to_list(list_of_letters, current_letter):
    list_of_letters.append(current_letter)


def add_letter_to_file(LETTERS_FILE_PATH, current_letter):
    f_2 = open(LETTERS_FILE_PATH, "a", encoding='utf-8')
    line = current_letter.to_file()
    f_2.write(line)
    f_2.write('\n')
    f_2.close()
    print(current_letter.to_file())
