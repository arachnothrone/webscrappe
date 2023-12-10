"""
scrap numbers of signatures from petition page:
https://www.ourcommons.ca/petitions/en/Petition/Details?Petition=e-4701

"""

import sys
from cmath import log
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# /usr/local/bin/chromedriver - macos
# /usr/bin/chromedriver       - linux
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

url = 'https://www.ourcommons.ca/petitions/en/Petition/Details?Petition=e-4701'
# driver = webdriver.Chrome()
driver = webdriver.Chrome(options=options)
driver.get(url)

log_file_name = "log.txt"
log_file = open(log_file_name, "a")
data_file = open("data.csv", "a")
nr_of_loops = 2

if len(sys.argv) > 1:
    nr_of_loops = int(sys.argv[1])

print("Number of loops: ", nr_of_loops)

for i in range(nr_of_loops):
    try:
        # Need to expand the table with provinces
        button = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div/div/div[3]/div[4]/a")
        button.click()
        time.sleep(1)

        # button.text - has all signatures value

        # Get provinces table
        canada_table = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div/div/div[3]/div[4]/div/div/table/tbody")
        rows = canada_table.find_elements(By.TAG_NAME, "tr")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Current time: {}, overall: {}".format(current_time, button.text))

        # Write time stamp
        data_file.write(current_time)
        data_file.write(",")

        # Extract number of Canada signatures from button text (e.g. "1234 signatures" -> "1234")
        maybe_sigs = button.text.split(" ")[0]
        sigs = maybe_sigs if maybe_sigs.isdecimal() else ""
        data_file.write(sigs)       # signatures

        # Table contains 13 rows, 2 columns in a row
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 2:
                print("Province: {0:30s}, signatures: {1:6d}".format(cols[0].text, int(cols[1].text)))
                log_file.write("{:20s} {:30s} {:s}\n".format(current_time, cols[0].text, cols[1].text))
                data_file.write(",")
                data_file.write(cols[0].text)       # province
                data_file.write(",")
                data_file.write(cols[1].text)       # signatures
            else:
                log_file.write("{:s},".format(current_time))
                data_file.write(current_time)
                for col in cols:
                    print(" ", col.text, end='')
                    log_file.write(" {:s}".format(col.text))
                    data_file.write(",{:s}".format(col.text))
                log_file.write("\n")
                print()
        data_file.write("\n")
        data_file.flush()
        log_file.write("--------------------------------------------------------\n")
        print("--------------------------------------------------------\n")
        log_file.flush()

    except Exception as e:
        print("Exception: ", e)
        log_file.write("Exception: {:s}\n".format(str(e)))
        log_file.flush()


    driver.refresh()
    time.sleep(300)

driver.quit()
log_file.close()
data_file.close()
