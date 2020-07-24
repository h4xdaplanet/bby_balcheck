import pandas as pd
from proxy_helper import get_chromedriver
import time
import config
from datetime import datetime


# load gcs from csv
# dtype str to keep from losing leading zeros on pins
gc_dict = pd.read_csv(config.gcFileName, dtype=str).to_dict()
gc_count = len(gc_dict['GC'])
print('Loaded {} cards'.format(str(gc_count)))

# stuff to run this headless in the future
# chrome_options.add_argument("--headless")
# chrome_options = webdriver.ChromeOptions()

loop = 0
ip_loop = 0
retry_flag = False
driver = get_chromedriver(config.proxy_dict, use_proxy=True)

while loop < gc_count:
    card = gc_dict['GC'][loop]
    pin = gc_dict['Pin'][loop]
    bal = gc_dict['Bal'][loop]
    print('{}, {}, {}, {}'.format(loop, card, pin, bal))
    driver.get("https://www.bestbuy.com/gift-card-balance")
    driver.find_element_by_id('gift-card-number').send_keys(card)
    driver.find_element_by_id('pin-number').send_keys(pin)
    driver.find_element_by_xpath(config.submitButton).click()
    time.sleep(2)
    # Do this later
    # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "element_id")))
    if driver.find_elements_by_class_name('has-error'):
        if retry_flag is False:
            driver.quit()
            time.sleep(60)
            retry_flag = True
            driver = get_chromedriver(config.proxy_dict, use_proxy=True)
            ip_loop = 0
            continue
        else:
            gc_dict['Bal'][loop] = 'Error'
            print('Error for card {}'.format(card))


    else:
        try:
            new_bal = driver.find_element_by_class_name('card-balance__on-card').text
            print(new_bal)
            gc_dict['Bal'][loop] = new_bal
        except:
            if retry_flag is False:
                driver.quit()
                time.sleep(60)
                retry_flag = True
                driver = get_chromedriver(config.proxy_dict, use_proxy=True)
                ip_loop = 0
                continue
            else:
                gc_dict['Bal'][loop] = 'Error'

    loop += 1
    ip_loop += 1
    if ip_loop > 19:
        driver.quit()
        time.sleep(60)
        driver = get_chromedriver(config.proxy_dict, use_proxy=True)
        ip_loop = 0
    retry_flag = False
    time.sleep(1)

df = pd.DataFrame.from_dict(gc_dict)
dt_string = now.strftime("%d-%m-%Y-%H%M")
df.to_excel('output-{}.xlsx'.format(dt_string))
driver.quit()
