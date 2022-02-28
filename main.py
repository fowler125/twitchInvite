
import webbrowser
from selenium import webdriver

def openBrowser():
    webbrowser.open('http://twitch.tv', new=2)

def searchCategories():
    browser = webdriver.Chrome('./chromedriver')

    browser.get('https://python.org')
    browser.save_screenshot("screenshot.png")

    browser.close()

def twitchChannel(name):

    print(f'Hi, {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    searchCategories()
    #openBrowser()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
