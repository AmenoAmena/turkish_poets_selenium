from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.xn--trkeiir-wxa0q61b.com/")

poem_dict = {}

total_pages = 3

counter = 0

for page in range(0, total_pages):
    try:
        links = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "poetLink"))
        )

        for link in links:
            try:
                current_window = driver.current_window_handle
                inner_link = link.get_attribute("innerHTML")
                sleep(2)
                if inner_link not in poem_dict:
                    link.click()

                    all_windows = driver.window_handles
                    for windows in all_windows:
                        if windows != current_window:
                            driver.switch_to.window(windows)
                            break

                    sleep(5)

                    poet = driver.find_element(By.TAG_NAME, "h1")
                    poet_name = poet.find_element(By.TAG_NAME, "a")
                    poem = driver.find_element(By.CLASS_NAME, "poetShow")

                    poet_name_real = poet_name.get_attribute("innerHTML")
                    poem_name = poem.find_element(By.TAG_NAME, "h1").get_attribute("innerHTML")

                    poem_dict[poem_name] = poet_name_real

                    counter +=1

                    sleep(2)

                    driver.back()

            except:
                print(f"Error at: {inner_link}")
                continue

        sleep(2)

        next_page_link = driver.find_element(By.XPATH, f"//a[@href='?page={page + 1}']")
        next_page_link.click()

    except Exception as err:
        print(f"Error: {err}")
        break

sleep(2)

new_poem_dict = {}
for key, value in poem_dict.items():
    modified_key = key.lower().replace('ı', 'i').replace('ü', 'u').replace('ö', 'o').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g')
    modified_value = value.lower().replace('ı', 'i').replace('ü', 'u').replace('ö', 'o').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g') if isinstance(value, str) else value
    new_poem_dict[modified_key] = modified_value

with open("poem.csv", "w", newline="", encoding="utf-8") as poem_file:
    writer = csv.writer(poem_file, delimiter=",")
    writer.writerow(["name", "poem"])
    for key, value in new_poem_dict.items():
        writer.writerow([key, value])

print(new_poem_dict.keys())
print(counter)