import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libraries import reading_and_saving as rs
from libraries import postpy as postpy


def count_working_days(date1, date2):  # counting working days as specified by polish post
    date = date1
    counter = 0

    if date.day == date2.day:
        return counter

    while 1:
        date += datetime.timedelta(days=1)
        if date.weekday() < 5:
            counter += 1
        if date.day == date2.day:
            return counter


def check_if_on_time(letter):
    delta = count_working_days(letter.data_wyslania, letter.data_dotarcia)  # difference in working days
    if letter.typ == 'List polecony ekonomiczny':  # this type is supposed to be delivered in 3 days
        if delta <= 3:
            return 1  # on time
        else:
            return 0  # late
    elif letter.typ == 'List polecony priorytetowy':  # this type is supposed to be delivered in 1 day
        if delta <= 1:
            return 1  # on time
        elif delta == 2 and letter.data_wyslania.hour >= 15:
            return 1
        else:
            return 0  # late
    elif letter.typ == 'Przesyłka firmowa polecona zamiejscowa':
        if delta <= 4:
            return 1
        else:
            return 0
    else:  # if some other nonstandard letter type occur, then it will not be counted to statistics
        return 2


def checksum(kod):
    tab = list(kod)
    parity = 1
    suma = 0

    for i in range(2, 19, 1):
        c = int(tab[i])
        if parity: 
            suma = suma + c * 3
            parity = 0
        else:
            suma = suma + c * 1
            parity = 1
        d = suma % 10

    if d == 0:
        return 0
    else:
        return 10 - d


def create_existing_number(base, number):
    if len(str(number)) == 1:  # when we have one digit number
        letter_number = base + '00' + str(number)
    elif len(str(number)) == 2:  # when we have two digits number
        letter_number = base + '0' + str(number)
    else:  # three digits number
        letter_number = base + str(number)

    letter_number = letter_number + str(checksum(letter_number))
    return letter_number


def get_sending_info(row, current_letter):
    if row[0].text == "Rodzaj przesyłki" or row[0].text == "Rodzaj przesyłki: ":
        current_letter.typ = row[1].text
    if row[0].text == "Urząd nadania" or row[0].text == "Urząd nadania: ":
        current_letter.miejsce_wysylki = row[1].text

    return current_letter


def get_delivery_info(row, current_letter):
    if row[0].text == "Nadanie":
        current_letter.data_wyslania = rs.split_data(row[1].text)
    if (row[0].text == "Doręczono" or
            row[0].text == "Awizo - przesyłka do odbioru w placówce" or
            row[0].text == "Odebrano w placówce" or
            row[0].text == "Próba doręczenia" or
            row[0].text == "Decyzja o zwrocie przesyłki" or
            row[0].text == "Próba doręczenia - dosłanie"):
        if current_letter.miejsce_celu == "nie doszedl":
            current_letter.data_dotarcia = rs.split_data(row[1].text)
            current_letter.miejsce_celu = row[2].text

    return current_letter


def read_table(tab, letter, get_func):
    for row_number in range(1, len(tab)):
        row = tab[row_number].find_elements_by_tag_name("td")
        letter = get_func(row, letter)
    return letter


def send_query(driver, number):
    field = driver.find_element_by_id("searchInputPostalDelivery")
    field.clear()
    field.send_keys(number)
    field.send_keys(Keys.RETURN)


def get_letter(driver, number):
    time.sleep(0.1)
    info = WebDriverWait(driver, 0.5).until(
        EC.presence_of_element_located((By.ID, "infoTable"))
    )

    current_letter = postpy.Letter(None, "nie doszedl", None, "nie doszedl", None, number, None, None)
    letter_info_table = info.find_elements_by_tag_name("tr")  # array with information about letter
    current_letter = read_table(letter_info_table, current_letter, get_sending_info)

    tracking_table = driver.find_element_by_id("eventsTable")
    letter_info_table = tracking_table.find_elements_by_tag_name("tr")
    current_letter = read_table(letter_info_table, current_letter, get_delivery_info)
    current_letter.ilosc_dni_roboczych = count_working_days(current_letter.data_wyslania, current_letter.data_dotarcia)
    current_letter.on_time = check_if_on_time(current_letter)

    return current_letter

