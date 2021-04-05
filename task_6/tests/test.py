from selenium import webdriver
from selenium.webdriver.chrome.options import Options

    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")

    # browser = webdriver.Chrome(options=chrome_options)

browser = webdriver.Remote(
    command_executor='http://selenium-hub:4444',
    desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})

def test_1():
    browser.get("http://www.facebook.com")
    page_title = browser.title

    assert page_title == "Facebook - Log In or Sign Up"
    print("test_1 PASSED")

def test_2():
    browser.get("http://stackoverflow.com")
    page_title = browser.title

    assert page_title == "Stack Overflow - Where Developers Learn, Share, & Build Careers"
    print("test_2 PASSED")

def test_3():
    browser.get("http://google.com")
    page_title = browser.title

    assert page_title == "Google"
    print("test_3 PASSED")

if __name__ == "__main__":
    test_1()
    test_2()
    test_3()