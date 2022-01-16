# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os, sys
import libraries.reading_and_saving as rs
import libraries.letter_processing as lp
from scrap_stats import scrap_stats


DRIVER_PATH = ""
LINK = "https://emonitoring.poczta-polska.pl/"
SCRAPPING_TIME = 3600
BASES_PATH = ""
LAST_DONE_BASE_PATH = ""
LETTERS_FILE_PATH = ""


def scrap_base(base_id, driver, list_of_letters):
    mail_id = 0
    while mail_id <= 999:
        number = lp.create_existing_number(base_id, mail_id)
        lp.send_query(driver, number)
        mail_id += 1
        
        try: # checks if the mail exists and is delivered
            current_letter = lp.get_letter(driver, number)
            rs.add_letter_to_list(list_of_letters, current_letter)
            rs.add_letter_to_file(LETTERS_FILE_PATH, current_letter)

        except Exception as e:  # no such mail
            print('Error:' + str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    return list_of_letters


def main():
    start_time = time.time()

    list_of_letters = []
    list_of_bases = rs.get_bases(BASES_PATH, rs.read_file(LAST_DONE_BASE_PATH))

    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(LINK)


    for base_id in list_of_bases:
        if time.time() - start_time > SCRAPPING_TIME:
            print("Ended after " + str(time.time() - start_time) + "s, next not checked base is:", base_id)
            rs.write_to_file(LAST_DONE_BASE_PATH, base_id)
            break

        scrap_base(base_id, driver, list_of_letters)
    
    scrap_stats(list_of_letters, start_time)



if __name__ == "__main__":
    main()
