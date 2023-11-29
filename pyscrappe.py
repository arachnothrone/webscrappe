"""
scrap numbers of signatures from the website 
https://www.ourcommons.ca/petitions/en/Petition/Details?Petition=e-4701

"""

import sys
from cmath import log
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.ourcommons.ca/petitions/en/Petition/Details?Petition=e-4701'
driver = webdriver.Chrome()
driver.get(url)

log_file_name = "log.txt"
log_file = open(log_file_name, "w")
data_file = open("data.csv", "w")
nr_of_loops = 2

# allPageSourceText = driver.page_source
# specific_element = driver.find_element_by_class_name('pet-table-col')
# # Extract text content from the specific element

# variant 2
# a = driver.find_element(By.CLASS_NAME, "pet-table-col")
# b = driver.find_element(By.PARTIAL_LINK_TEXT, "signatures")
# print(b.text)   # '78350 signatures'

if len(sys.argv) > 1:
    nr_of_loops = int(sys.argv[1])

print("Number of loops: ", nr_of_loops)

for i in range(nr_of_loops):

    # Need to expand the table with provinces
    button = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div/div/div[3]/div[4]/a")
    button.click()
    time.sleep(1)

    # button.text - has all signatures number

    # Get provinces table:
    canada_table = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div/div/div[3]/div[4]/div/div/table/tbody")
    rows = canada_table.find_elements(By.TAG_NAME, "tr")

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Current time: {}, overall: {}".format(current_time, button.text))
    data_file.write(current_time)
    data_file.write(",")
    data_file.write(button.text)

    # Table contains 13 rows, 2 columns in a row
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) == 2:
            print("Province: {0:30s}, signatures: {1:6d}".format(cols[0].text, int(cols[1].text)))
            log_file.write("{:20s} {:30s} {:s}\n".format(current_time, cols[0].text, cols[1].text))
            data_file.write(",")
            data_file.write(cols[0].text)
            data_file.write("=")
            data_file.write(cols[1].text)
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
    log_file.write("--------------------------------------------------------\n")

    driver.refresh()
    time.sleep(10)

driver.quit()
log_file.close()
data_file.close()
