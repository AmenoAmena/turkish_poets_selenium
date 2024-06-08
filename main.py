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
        sleep(2)
        if inner_link not in done_titles:
            link.click()

            all_windows = driver.window_handles
            for windows in all_windows:
                if windows != current_window:
                    driver.switch_to.window(windows)
                    break
            
            sleep(2)

            poet = driver.find_element(By.TAG_NAME,"h1")
            poet_name = poet.find_element(By.TAG_NAME,"a")
            poem = driver.find_element(By.CLASS_NAME,"poetShow")

            poet_name_real = poet_name.get_attribute("innerHTML") 
            poem_name = poem.find_element(By.TAG_NAME,"h1").get_attribute("innerHTML")

            poem_dict.update({f"{poem_name}":f"{poet_name_real}"})

            sleep(2)

            driver.back()

    except:
        print(f"not worked: {inner_link}")
        continue
    
sleep(2)

new_poem_dict = {}

for key, value in poem_dict.items():
    modified_key = key.lower().replace('ı', 'i').replace('ü', 'u').replace('ö','o').replace('ş','s').replace('ç','c').replace('ğ','g')
    modified_value = value.lower().replace('ı', 'i').replace('ü', 'u').replace('ö','o').replace('ş','s').replace('ç','c').replace('ğ','g') if isinstance(value, str) else value
    
    new_poem_dict[modified_key] = modified_value

                
with open("poem.csv","w",newline="",encoding="utf-8") as poem_file:
    writer = csv.writer(poem_file, delimiter=",")
    writer.writerow(["name","poem"])
    for key in new_poem_dict:
        writer.writerow([key] + [new_poem_dict[key]])

print(new_poem_dict.keys())