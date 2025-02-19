# Instagram Outreach Automation

This Python script leverages Selenium to humanize and automate Instagram outreach by sending messages from multiple profiles through proxies. It simulates human typing, cycles through different Instagram accounts, and logs the status of each message sent.

## Features

- **Humanized Typing:** Simulates human-like delays when typing messages.
- **Automated Messaging:** Automatically navigates to Instagram profiles and sends pre-defined messages.
- **Multi-Profile Support:** Uses separate Chrome profiles to manage multiple Instagram accounts.
- **Proxy Integration:** Randomly selects and applies proxies for each session.
- **Message Logging:** Records the status of each outreach message in a CSV file.
- **Customizable Configuration:** Easily modify messages, file paths, profile limits, and proxy settings.

## Prerequisites

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/)
- [ChromeDriver](https://chromedriver.chromium.org/) (Ensure it is installed and added to your system's PATH)
- Google Chrome installed
- A Chrome extension for proxy authentication (if needed)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/instagram-outreach-automation.git
   cd instagram-outreach-automation
   ```

2. **Install Required Python Packages:**

   ```bash
   pip install selenium
   ```

## Configuration

Before running the script, make sure to update the following placeholders in the code:

- **Messages:** Modify the `MESSAGES` list to include the outreach messages you want to send.
- **Profile Links File:** Replace `"MODIFY"` with the path to your text file containing Instagram profile links.
- **Profile Directories:** Set `base_profiles_dir` to the directory where your separate Chrome profile directories are stored.
- **Messages Per Profile:** Adjust the `MESSAGES_PER_PROFILE` dictionary to define how many messages each profile should send.
- **Proxies File:** Replace `"MODIFY"` with the path to your text file containing proxy information.
- **Chrome Extension Path:** Update `EXTENSION_PATH` with the path to your proxy authentication Chrome extension.
- **CSV Log File:** Modify the file path in the `updated_file_path` variable to where you want the CSV log to be saved.

## Usage

Run the script using Python:

```bash
python outreach.py
```

The script will:

1. Cycle through each defined Chrome profile.
2. Use a random proxy for each session.
3. Navigate to Instagram profiles from your list.
4. Send a random pre-defined message with human-like delays.
5. Log the status (Completed or Failed) of each sent message in a CSV file.
6. Remove messaged profiles from the pending list and record them as used.

## Disclaimer

**Important:** Use this script responsibly and in accordance with Instagram's terms of service. The author is not liable for any account limitations, bans, or other issues resulting from the use of this automation tool.
