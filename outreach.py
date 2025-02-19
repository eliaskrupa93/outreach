import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import csv
import traceback

MESSAGES = [ # define messages that you want to be sent - I like to use 2 that are randomly picked to test which outreach message does better - MODIFY
    "message that you want to send #1 - MODIFY",
    "message that you want to send #2 - MODIFY"
]

with open("MODIFY", "r") as file: # read instagram profile links for the txt file - these are filtered already and consist of just the a link - in this specific use, an instagram link to a profile - MODIFY
    profile_links = [line.strip() for line in file if line.strip()]

base_profiles_dir = r"MODIFY" # folder for your seperate profile directories - each profile gets their own profile on chrome - directory in the format C:\x\y\z\n

MESSAGES_PER_PROFILE = { # hardcodede the number of messages each profile will send - the reason for this is some accounts get limimted before other accounts - its not as easy to detect when accounts are limited so you can hardcode these values
    "Profile 1": 10,
    "Profile 2": 60,
    "Profile 3": 20,
    "Profile 4": 35, # all of these values should be modified and remove and add profiles as needed
    "Profile 5": 25, # this instance used 9 instagrams accounts 
    "Profile 6": 25,
    "Profile 7": 30,
    "Profile 8": 25,
    "Profile 9": 60,
}

with open("MODIFY", "r") as file: # read proxies from the proxies txt file - MODIFY
    PROXY_LIST = [line.strip() for line in file if line.strip()]

EXTENSION_PATH = r"MODIFY" # folder for your exentsion directory - directory in the format C:\x\y\z\n

def human_type(element, text, delay_min=0.005, delay_max=0.05):
    for char in text: # simulates human typing by typing one character at a time with random delays
        element.send_keys(char)
        time.sleep(random.uniform(delay_min, delay_max))

def send_message(driver, profile_link): # sends a "random" message to a given profile
    try:
        if not profile_link.startswith("http"): # construct or validate URL
            profile_link = "https://www.instagram.com/" + profile_link.strip() + "/" # instagram for this instance
        print("\nNavigating to:", profile_link)
        driver.get(profile_link)
        time.sleep(random.uniform(3, 5))  # reduce the delay

        print("current", driver.current_url) # prints current url for debug

        WebDriverWait(driver, 5).until( # wait for a profile-specific element to make sure that the page has fully loaded
            EC.presence_of_element_located((By.XPATH, "//header"))
        )

        try: # try to click message button
            message_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Message')]"))
            )
        except Exception: # if the button is not click, try a new possible XPath
            message_button_xpath = "//div[@role='button' and contains(text(), 'Message')]"
            message_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, message_button_xpath))
            )
        message_button.click()

        message_input = WebDriverWait(driver, 5).until( # wait for the messaging input field to appear
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )
        time.sleep(random.uniform(1, 2))  # reduced delay to avoid detecetion

        message_input.click()  # click on the input field
        message = random.choice(MESSAGES)  # select the message
        human_type(message_input, message)  # humanize the delay
        message_input.send_keys(Keys.ENTER)  # send the message
        print(f"message sent to {profile_link}: {message}") # confirm that the messahe was sent

        return True

    except Exception as e:
        print("Error sending message to", profile_link, ":", e)
        traceback.print_exc()
        return False

def get_random_proxy():
    return random.choice(PROXY_LIST) # random proxy from the list 

def remove_link_from_filterfinal(profile_link): # removes the profile link from the input list
    with open("filterfinal.txt", "r") as file:
        lines = file.readlines()

    with open("filterfinal.txt", "w") as file:
        for line in lines:
            if line.strip() != profile_link:
                file.write(line)

def append_link_to_usedalready(profile_link): # add the messaged link to the used accounts list so that we do not message the same account twice
    with open("usedalready.txt", "a") as file:
        file.write(profile_link + "\n")

def is_account_limited(driver): # limitation check to see if the account has been limited by instagram - does not work well on chrome
    try:
        limitation_message = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'limit')]"))
        )
        return True
    except:
        return False

def main():
    updated_file_path = "MODIFY" # csv file to record the status of each profile - NOT NEEDED - MODIFY
    with open(updated_file_path, 'w', newline='', encoding='latin1') as updated_csv:
        writer = csv.writer(updated_csv)
        writer.writerow(['Profile Links', 'Status'])  # write header for format

        profile_index = 1 # iterate through each profile
        while True:
            profile_name = f"Profile {profile_index}"
            profile_dir = os.path.join(base_profiles_dir, profile_name)

            if not os.path.exists(profile_dir):
                print(f"out of profiles")
                break

            print(f"\nswitching profile to {profile_name}...")

            chrome_options = Options() # set up the chrome options for the profile
            chrome_options.add_argument(f"--user-data-dir={profile_dir}")
            chrome_options.add_argument(f"--profile-directory={profile_name}")
            chrome_options.add_argument("--disable-notifications")

            proxy = get_random_proxy() # set up a random proxy with authentication
            proxy_parts = proxy.split(":")
            proxy_host = proxy_parts[0]
            proxy_port = proxy_parts[1]
            proxy_user = proxy_parts[2]
            proxy_pass = proxy_parts[3]

            chrome_options.add_argument(f"--proxy-server=http://{proxy_host}:{proxy_port}") # configures the proxy server

            chrome_options.add_argument(f"--load-extension={EXTENSION_PATH}") # load chrome extension for proxy authentication

            driver = webdriver.Chrome(options=chrome_options) # launch browser for this profile

            driver.get("https://www.instagram.com") # go to the homepage to make sure that the session is logged in and active
            time.sleep(random.uniform(3, 5))  # reduce the delay to avoid detection

            messages_sent = 0 
            messages_to_send = MESSAGES_PER_PROFILE.get(profile_name, 0)  # number of message to send for this given profile

            for profile_link in profile_links[:]:  # iterate over a copy of the list
                if messages_sent >= messages_to_send:
                    break  # move to the next profile after needed amount of messages sent

                success = send_message(driver, profile_link)
                if success:
                    writer.writerow([profile_link, "Completed"])
                else:
                    writer.writerow([profile_link, "Failed"])

                append_link_to_usedalready(profile_link) # move the link to used acocunts regardless of success - this is used if a account has messages off or somethihng where there is no message button
                remove_link_from_filterfinal(profile_link)
                profile_links.remove(profile_link)  
                messages_sent += 1

                if is_account_limited(driver): # check if the account has been limited
                    print(f"account {profile_name} has been limited after {messages_sent} messages")
                    break

                time.sleep(random.uniform(3, 5))  

            driver.quit() # close the browser for this profile

            profile_index += 1 # move to the next profile

if __name__ == "__main__":
    main()