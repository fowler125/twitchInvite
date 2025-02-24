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
from selenium.common.exceptions import TimeoutException


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
    time.sleep(3)
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
    try:
        button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value="//button[@data-a-target='player-overlay-mature-accept']")
        )
        button.click()
    except TimeoutException:
        pass

def check_for_update_password():
    button = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value="//button[@data-a-target='account-checkup-generic-modal-secondary-button']")
    )
    try:
        button.click()
    except Exception as e:
        log.msg("Selenium Exception: {0} Message: {1}".format("my message", str(e)))

def whisper_button():
    button = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH,value="//button[@data-a-target='whisper-box-button']")
    )
    try:
        button.click()
    except Exception as e:
        log.msg("Selenium Exception: {0} Message: {1}".format("my message", str(e)))

def whisper_message(channel):
    whisper_field = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value="//input[@id='threads-box-filter']")
    )
    whisper_field.click()
    whisper_field.send_keys(channel)
    whisper_field.send_keys(Keys.RETURN)

def whisper_click(channel):
    channel_lower = channel.lower()
    first = f"//div[@data-a-target='whisper-search-result-{channel_lower}']"
    print(first)
    time.sleep(3)
    #whisper_button = driver.find_element(by=By.XPATH, value=f"//input[@id='whisper-search-result-{channel_lower}']")
    whisper_click = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value=f"//div[@data-a-target='whisper-search-result-{channel_lower}']")
    )
    whisper_click.click()

def check_for_whisper_off():
    try:
        whisper_click = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value="//p[contains(text(),'This user has turned on')]")
        )
        whisper_click.click()
    except Exception as e:
        pass

def copy_paste(channel):
    channel_lower = channel.lower()
    whisper_click = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value="//input[@type='text']")
    )
    #whisper_click.click()
    whisper_click.send_keys('Whats good i was in your stream earlier, '
                            'i dont mean to disturb you, we got a black streamers discord, and '
                            'we help support each other, so im going around twitch and trying to get all the '
                            'black streamers so we can make this bread together: https://discord.gg/MBa7FaK9Ee')
    whisper_click.send_keys(Keys.RETURN)
    whisper_close = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value=f"//button[@data-a-target='thread-close-button-{channel_lower}']")
    )
    whisper_close.click()

def main():
    startup()
    login()
    check_for_update_password()
    #sort_high_to_low()
    time.sleep(10)
    count = 0
    while count < 5:
        channel = get_random_black_channel()
        ActionChains(driver).move_to_element(channel).perform()
        channel.click()
        check_for_start_watching()
        channel_name = name_extractor()
        redundancy_checker(channel_name)
        whisper_button()
        whisper_message(channel_name)
        whisper_click(channel_name)
        check_for_whisper_off()
        copy_paste(channel_name)
        count+1
        driver.execute_script("window.history.go(-1)")

if __name__ == '__main__':
    main()

