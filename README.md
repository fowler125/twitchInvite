# Twitch Streamer Outreach Bot

## Overview
This project is a Python-based automation script that uses Selenium to interact with Twitch.

Please note as of February 4th, 2024 this project has been deprecated, due to Twitch not allowing automation software to access twitch thru selenium.
## Features
- Automatically launches Chrome and navigates to Twitch.
- Searches for streamers with a specific tag.
- Logs into a Twitch account using stored credentials.
- Sends a whisper message to selected streamers.
- Prevents sending duplicate messages by maintaining a log of contacted streamers.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Google Chrome
- ChromeDriver (managed via `webdriver-manager`)
- Required Python packages:
  ```sh
  pip install selenium webdriver-manager
  ```

## Setup
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Create a `credentials` file in the project directory containing:
   ```
   your_twitch_username
   your_twitch_password
   ```
3. Run the script:
   ```sh
   python main.py
   ```
4. When prompted, enter the Two-Factor Authentication (2FA) code.

## Usage
- The script will search for Twitch streamers based on the specified tag (default: "Black").
- It logs in using the provided credentials and navigates to a streamer's page.
- The bot checks if the streamer has already been contacted to avoid duplicates.
- A whisper message is sent with an invitation to join a Discord server.

## Notes
- The script uses Selenium WebDriver to interact with the Twitch UI.
- If Twitch updates its UI, XPath selectors might need to be updated.
- To modify the search tag, edit the `search_bar.send_keys("Black")` line in `startup()`.

## Disclaimer
This project is for educational purposes only. Automating interactions on Twitch may violate their terms of service. Use at your own risk.

## Author
Jabari Fowler

