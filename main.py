from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


options = Options()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get("https://www.xn--trkeiir-wxa0q61b.com/")

links = driver.find_elements(By.CLASS_NAME,"poetLink")


done_titles = []

poem_dict = {

}


for link in links:
    try:
        current_window = driver.current_window_handle
        inner_link = link.get_attribute("innerHTML")
        sleep(2)
        if inner_link not in done_titles:
            link.click()

            all_windows = driver.window_handles
            for windows in all_windows:
                if windows != current_window:
                    driver.switch_to.window(windows)
                    break
            
            poet = driver.find_element(By.TAG_NAME,"h1")
            poet_name = poet.find_element(By.TAG_NAME,"a")
            poem = driver.find_element(By.TAG_NAME,"pre")

            poet_name_real = poet_name.get_attribute("innerHTML") 
            poem_name = poem.get_attribute("innerHTML")

            poem_dict.update({f"{poet_name_real}":f"{poem_name}"})

            sleep(2)

            driver.back()
            print(done_titles)
    except:
        print("not worked")
        continue
    

                
with open("poem.csv","w",newline="") as poem_file:
    writer = csv.writer(poem_file, delimiter=",")
    writer.writerow(["name"] + ["poem"])
    for key in poem_dict:
        writer.writerow([key] + [poem_dict[key]])

print(poem_dict.keys())