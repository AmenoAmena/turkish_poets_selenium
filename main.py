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
all_windows = driver.window_handles

done_titles = []

poem_dict = {

}

for link in links:
    inner_link = link.get_attribute("innerHTML")
    current_window = driver.current_window_handle
    if inner_link not in done_titles:
        link.click()
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
        
        done_titles.append(poet_name_real)

        home_link = driver.find_element(By.TAG_NAME,"a")
                
with open("poem.csv","w",newline="") as poem_file:
    writer = csv.writer(poem_file, delimiter=",")
    writer.writerow(["name"] + ["poem"])
    for key in poem_dict:
        writer.writerow([key] + [poem_dict[key]])

print(poem_dict.keys())