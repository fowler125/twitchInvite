import time
import webbrowser
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


#keeps connection alive for Chrome driver
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

#function to boot up Chrome, and search for Black or African American Tags on twitch (tags can be changed)
def startup():

    driver.get("https://www.twitch.tv/directory/")
    print(driver.title)
    search_bar = driver.find_element(by=By.XPATH,value="//input[@id='dropdown-search-input']")
    search_bar.click()
    time.sleep(2)
    search_bar.send_keys("Black")
    time.sleep(2)
    search_bar.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

#login function for logging you into your twitch
def login():

    login_button = driver.find_element(by=By.XPATH,value="//*[contains(text(), 'Log In')]")
    login_button.click()

    #read in the username and password from credentials file
    with open('credentials') as f:
        #reads first line of file, stores in func variable username
        username = f.readline()
        #reads second line of file, stores in func variable password
        password = f.readline()

    #entering in the twitch username for login
    username_field = WebDriverWait(driver,10).until(
        lambda x: x.find_element(by=By.XPATH,value="//input[@id='login-username']")
    )
    username_field.click()
    username_field.send_keys(username)


    #entering in the twitch password for login
    password_field = WebDriverWait(driver,10).until(
        lambda x : x.find_element(by=By.XPATH, value="//input[@id='password-input']")
    )
    password_field.click()
    password_field.send_keys(password)

    #click Login button
    time.sleep(1)
    submit_login = driver.find_element(by=By.XPATH, value="//*[@data-a-target='passport-login-button']")
    submit_login.click()

    #Two Factor Code from Authy App

    confirmation_code_input = WebDriverWait(driver, 30).until(
        lambda x: x.find_element(
            by=By.XPATH, value="//*[@autocomplete='one-time-code']")
    )
    code = input('Please enter 2FA Code: ')
    confirmation_code_input.send_keys(code)

    submit_button = driver.find_element(
        by=By.XPATH, value="//*[contains(text(), 'Submit')]")
    submit_button.click()

    #print(username)
    #print(password)



startup()
login()

