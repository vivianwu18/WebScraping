from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


### Selenium

### 1. please get Selenium to work on your system. e., try to code something up in Java or Python that starts a browser of your choice, navigates to google.com, and searches for "askew" as well as "google in 1998" (separate searches!)
### search "askew"

driver = webdriver.Chrome(executable_path = '/Users/vivianwu/Desktop/BAX 422/chromedriver/chromedriver')
driver.implicitly_wait(5)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)

driver.get("https://google.com")

inp = driver.find_element(By.CSS_SELECTOR, "input[type = text]")
time.sleep(1)
inp.send_keys("askew\n")
time.sleep(1)
driver.quit()

### search "google in 1998"
driver = webdriver.Chrome(executable_path = '/Users/vivianwu/Desktop/BAX 422/chromedriver/chromedriver')
driver.implicitly_wait(5)
driver.set_script_timeout(120)
driver.set_page_load_timeout(50)

driver.get("https://google.com")

inp = driver.find_element(By.CSS_SELECTOR, "input[type = text]")
time.sleep(1)
inp.send_keys("google in 1998\n")
time.sleep(1)
driver.quit()

