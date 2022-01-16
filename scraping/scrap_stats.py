import pandas as pd
from pandasgui import show
import time

def scrap_stats(list_of_letters, start_time):
    good_l = 0
    all_l = 0
    good_l_ek = 0
    all_l_ek = 0
    good_l_pr = 0
    all_l_pr = 0
    good_fir = 0
    all_fir = 0

    for letter in list_of_letters:
        if letter.on_time != 2:  # is delivered
            good_l += letter.on_time
            all_l += 1

            if letter.typ == 'List polecony ekonomiczny':
                good_l_ek += letter.on_time
                all_l_ek += 1
            if letter.typ == 'List polecony priorytetowy':
                good_l_pr += letter.on_time
                all_l_pr += 1
            if letter.typ == 'Przesyłka firmowa polecona zamiejscowa':
                good_fir += letter.on_time
                all_fir += 1

    if all_l != 0 and all_l_ek != 0 and all_l_pr != 0:
        print("For", all_l, "letters that should have be delivered by now,", good_l, "has been delivered")
        print("Post efficiency:", 100 * good_l / all_l, "%")

        print("For", all_l_ek, "economical letters that should have be delivered by now,", good_l_ek, "has been delivered")
        print("Post efficiency:", 100 * good_l_ek / all_l_ek, "%")

        print("For", all_l_pr, "priority letters that should have be delivered by now,", good_l_pr, "has been delivered")
        print("Post efficiency:", 100 * good_l_pr / all_l_pr, "%")

    print("--- %s seconds ---" % (time.time() - start_time))

    df = pd.DataFrame.from_records([l.to_dict() for l in list_of_letters])
    show(df)
