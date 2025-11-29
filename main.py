import time
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

from detector import scorebug_present
from config import *

def create_driver():
    """Launch a Selenium-controlled Chrome browser."""
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def screenshot(driver):
    """Capture and return a screenshot of the YouTube TV window."""
    driver.save_screenshot("scores/last_frame.png")
    return cv2.imread("scores/last_frame.png")

def switch_to(driver, url):
    """Navigate to a new channel/game URL."""
    print(f"Switching to: {url}")
    driver.get(url)
    time.sleep(3)  # Allow page to load

def main():
    driver = create_driver()

    print("Opening main game...")
    switch_to(driver, MAIN_GAME_URL)

    on_main_game = True

    while True:
        frame = screenshot(driver)

        if frame is None:
            print("Screenshot failed. Retrying...")
            time.sleep(CHECK_INTERVAL)
            continue

        game_active = scorebug_present(frame, SCOREBUG_REGION, BRIGHTNESS_THRESHOLD)

        if not game_active and on_main_game:
            print("Commercial detected — switching to backup game...")
            switch_to(driver, BACKUP_GAME_URL)
            on_main_game = False

        elif game_active and not on_main_game:
            print("Main game resumed — switching back...")
            switch_to(driver, MAIN_GAME_URL)
            on_main_game = True

        else:
            print("No change — staying on current channel.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
