import time
import webbrowser
import random
import os
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


#keeps connection alive for Chrome driver so it does not close automatically after commands are done
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

def get_random_black_channel():
    time.sleep(5)
    channels = WebDriverWait(driver, 10).until(
        lambda x: x.find_elements(
            by=By.XPATH, value="//a[@data-a-target='preview-card-title-link']")
    )[:10]
    random.shuffle(channels)
    return(channels[0])

#for caching all of the twitch black streamer names, in order make sure we dont send a bunch on invites to same streamer
def data_exporter(name):
    with open('streamer_names','a+') as z:
        z.write('\n')
        z.write(name)


#checks the cached list of all streamers to see if they have already been added
def redundancy_checker(name):
    with open('streamer_names','r') as z:
        lines = [line.rstrip('\n') for line in z]
        if name in lines:
            print("They are already present")
        else:
            print("Adding the following user to the list:: " + name)
            data_exporter(name)

def sort_high_to_low():
    sorter = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value="//a[@data-a-target='browse-sort-menu']")
    )
    sorter.click()
    sorter.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.RETURN)


def name_extractor():
    twitch_channel = driver.current_url
    name = twitch_channel.removeprefix('https://www.twitch.tv/')
    return(name)

def check_for_start_watching():
    button = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value="//button[@data-a-target='player-overlay-mature-accept']")
    )
    try:
        button.click()
    except Exception as e:
        log.msg("Selenium Exception: {0} Message: {1}".format("my message", str(e)))


startup()
login()
channel = get_random_black_channel()
ActionChains(driver).move_to_element(channel).perform()
channel.click()
check_for_start_watching()

redundancy_checker(name_extractor())
#driver.quit()
