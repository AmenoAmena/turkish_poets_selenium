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
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get("https://www.xn--trkeiir-wxa0q61b.com/")

links = WebDriverWait(driver,10).until(
    expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"poetLink"))
)



done_titles = []

poem_dict = {

}


for link in links:
    try:
        current_window = driver.current_window_handle
        inner_link = link.get_attribute("innerHTML")
        sleep(4)
        if inner_link not in done_titles:
            print(inner_link)
            link.click()

            all_windows = driver.window_handles
            for windows in all_windows:
                if windows != current_window:
                    driver.switch_to.window(windows)
                    break
            
#links = WebDriverWait(driver,10).until(
#    expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"poetLink"))
#)


            poet = WebDriverWait(driver,10).until(
                expected_conditions.presence_of_element_located((By.TAG_NAME,"h1"))
            )

            poet_name = WebDriverWait(driver,10).until(
                expected_conditions.presence_of_element_located((By.TAG_NAME,"a"))
            )

            poem = WebDriverWait(driver,10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME,"poetShow"))
            )


            poet_name = poet.find_element(By.TAG_NAME,"a")
            poem = driver.find_element(By.CLASS_NAME,"poetShow")

            poet_name_real = poet_name.get_attribute("innerHTML") 
            poem_name = poem.find_element(By.TAG_NAME,"h1").get_attribute("innerHTML")

            poem_dict.update({f"{poem_name}":f"{poet_name_real}"})

            sleep(2)

            driver.back()
            print(done_titles)
    except:
        print("not worked")
        continue
    
sleep(2)

                
with open("poem.csv","w",newline="") as poem_file:
    writer = csv.writer(poem_file, delimiter=",")
    writer.writerow(["name"] + ["poem"])
    for key in poem_dict:
        writer.writerow([key] + [poem_dict[key]])

print(poem_dict.keys())