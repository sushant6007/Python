import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import csv

driver = None
balanceTotal = []

def launch():
    """Launch Edge WebDriver with required options."""
    global driver
    print('Launching Edge browser...')

    options = Options()
    options.add_argument("--start-maximized")  
    options.add_argument("--disable-blink-features=AutomationControlled") 

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)

    print("Edge WebDriver launched successfully!")

def check_card(card_number, card_pin, retry_count=0):
    """Enter card details and check balance."""
    try:
        # Reset button (if necessary)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/form/div[4]/button[1]').click()
        
        driver.find_element(By.ID, 'cardNumber').send_keys(card_number)
        driver.find_element(By.ID, 'cardPin').send_keys(card_pin)
        time.sleep(1)

        # Click submit button
        try:
            driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/form/div[4]/button[2]').click()
        except:
            driver.find_element(By.XPATH, '//*[@id="wzrk-cancel"]').click()
            driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/form/div[4]/button[2]').click()

        time.sleep(3)

        # Extract balance and expiry date
        balance = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[3]/dl/dd[2]').text
        expiry = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[3]/dl/dd[3]').text
        
        balance_value = float(balance.replace('Rs. ', '').strip())
        balanceTotal.append(balance_value)

        result = {'balance': balance, 'expiry': expiry, 'card_number': card_number, 'card_pin': card_pin}
        return result

    except:
        try:
            msg = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[4]/div').text
            print(msg)
            return {'card_number': card_number, 'card_pin': card_pin, 'error': msg}
        except:
            if retry_count < 5:
                print(f"Retrying... ({retry_count+1}/5)")
                return check_card(card_number, card_pin, retry_count + 1)
            else:
                print("Max retries reached.")
                return {'error': 'Max retries reached! Please check manually!'}

def setup_browser():
    """Navigate to the website and prepare for data entry."""
    driver.get('https://www.woohoo.in/balenq')
    time.sleep(2)

    print('Getting dummy data...')
    driver.find_element(By.ID, 'cardNumber').send_keys("1231231231")
    driver.find_element(By.ID, 'cardPin').send_keys("23234234234")

    try:
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/form/div[4]/button[2]').click()
    except:
        driver.find_element(By.XPATH, '//*[@id="wzrk-cancel"]').click()
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/form/div[4]/button[2]').click()

    time.sleep(2)
    driver.get('https://www.woohoo.in/balenq')

def quit_browser():
    """Close the browser."""
    driver.quit()

if __name__ == "__main__":
    cards = []
    print('Loading CSV file...')

    with open('gvs.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line or ',' not in line:
                print(f"Skipping invalid line: {line}")
                continue  

            parts = line.split(',', 1)  # Split at the first comma
            if len(parts) == 2:
                card_number, card_pin = parts
                cards.append((card_number.strip(), card_pin.strip()))
            else:
                print(f"Skipping malformed line: {line}")

    print(f'Loaded {len(cards)} card entries!')

    launch()
    setup_browser()

    final_data = []
    count = 1
    skip = int(input('Where to start? '))

    for card_number, card_pin in cards:
        if count < skip:
            count += 1
            continue

        result = check_card(card_number, card_pin)
        print(result, count)

        if 'error' not in result:
            final_data.append(result)
            with open('output.txt', 'a+') as f:
                f.write(f"{result['card_number']},{result['card_pin']},{result['balance']},{result['expiry']}\n")

        count += 1

    quit_browser()

    print('Saved data in output.txt!')
    print(f'TOTAL BALANCE: Rs. {sum(balanceTotal)}')
