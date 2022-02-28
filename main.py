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
        username = f.readline()
        password = f.readline()

    print(username)
    print(password)



startup()
login()

