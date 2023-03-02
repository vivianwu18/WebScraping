
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


### Selenium
### 2. write a script that goes to bestbuy.com, clicks on Deal of the Day, reads how much time is left for the Deal of the Day and prints the remaining time to screen (console), clicks on the Deal of the Day (the actual product), clicks on its reviews, and saves the resulting HTML to your local hard drive as "bestbuy_deal_of_the_day.htm"

### print the remaining time
driver = webdriver.Chrome(executable_path = '/Users/vivianwu/Desktop/BAX 422/chromedriver/chromedriver')
driver.implicitly_wait(5)
driver.set_script_timeout(120)
driver.set_page_load_timeout(200)

driver.get("https://www.bestbuy.com/")

dealoftheday = driver.find_element(By.CSS_SELECTOR, "a[data-lid = 'hdr_dotd']")
dealoftheday.click()
time.sleep(1)

### wait until the page finished loading
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class = 'seconds cdnumber']")))
hours = driver.find_element(By.CSS_SELECTOR, "span[class = 'hours cdnumber']").text
minutes = driver.find_element(By.CSS_SELECTOR, "span[class = 'minutes cdnumber']").text
seconds = driver.find_element(By.CSS_SELECTOR, "span[class = 'seconds cdnumber']").text

countdown = hours + ' hours ' + minutes + ' minutes ' + seconds + ' seconds'
print(countdown)

driver.quit()

### save the reviews
driver = webdriver.Chrome(executable_path = '/Users/vivianwu/Desktop/BAX 422/chromedriver/chromedriver')
driver.implicitly_wait(5)
driver.set_script_timeout(120)
driver.set_page_load_timeout(200)

driver.get("https://www.bestbuy.com/")

dealoftheday = driver.find_element(By.CSS_SELECTOR, "a[data-lid = 'hdr_dotd']")
dealoftheday.click()
time.sleep(1)

deal = driver.find_element(By.CSS_SELECTOR, "a[class = 'wf-offer-link v-line-clamp ']")
deal.click()
time.sleep(1)

reviews = driver.find_element(By.CSS_SELECTOR, "span[class = 'c-reviews order-2']")
reviews.click()
time.sleep(1)

try:
    with open('bestbuy_deal_of_the_day.htm', 'w') as file:
        file.write(driver.page_source)
    print('The file has downloaded successfully.')
except:
    print('The file has not download successfully.')

driver.quit()

