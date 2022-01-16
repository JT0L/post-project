from selenium import webdriver
import random
import libraries.reading_and_saving as rs
import libraries.letter_processing as lp


DRIVER_PATH = ""
LINK = "https://emonitoring.poczta-polska.pl/"
POTENTIAL_BASES_NUMBERS_TO_CHECK = 5
FIRST_DIGITS = "00259007731" 
BASES_PATH = ""



# reading current set of bases -------------------
list_of_bases = rs.get_bases(BASES_PATH)
bases_set = set()
for base in list_of_bases:
    bases_set.add(base)
# reading current set of bases -------------------


driver = webdriver.Chrome(DRIVER_PATH)
driver.get(LINK)

for i in range(POTENTIAL_BASES_NUMBERS_TO_CHECK):
    if(i % 10 == 1):
        print("Checked", i , "from", POTENTIAL_BASES_NUMBERS_TO_CHECK , "bases, progress:", "{:.2f}".format(100*i/POTENTIAL_BASES_NUMBERS_TO_CHECK), "%")
        print("Founded", len(bases_set)," bases, to it's about", "{:.2f}".format(100*len(bases_set)/7800), "% of all")

    guess = random.randint(10000, 99999)
    potential_base = FIRST_DIGITS + str(guess)

    for j in range(5):   # for each base we try five low numbers to check if this base exists
        number = lp.create_existing_number(potential_base, random.randint(0,50))
        lp.send_query(driver, number)

        try: # if passes without error it means that this base exists and we can add it
            potential_letter = lp.get_letter(driver, number)
            bases_set.add(number[:16]) # base is the first 16 digits
            break
        
        except: # otherwise this letter doesn't exist and we continue our search
            pass


# saving to file ------------------------------------
list_of_bases_to_file = str()

for base in bases_set:
    list_of_bases_to_file = list_of_bases_to_file + str(base) + ','

rs.write_to_file(BASES_PATH, list_of_bases_to_file[:-1])
# saving to file ------------------------------------
