import re
from os import system
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIGURATION ===
VIDEO_URL = "https://vt.tiktok.com/ZSsJXGEEE/"
SERVICE = "followers"
MAX_ROUNDS = 10

class Bot:
    def __init__(self):
        system("clear")
        self._print_banner()
        self.driver = self._init_driver()
        self.services = self._init_services()

    def start(self):
        self.driver.get("https://zefoy.com")
        self._solve_captcha()
        sleep(2)
        self.driver.refresh()
        sleep(2)
        self.driver.refresh()
        self._check_services_status()

        if self.services[SERVICE]["status"] != "[WORKING]":
            print(f"[!] {SERVICE} is OFFLINE. Exiting.")
            self.driver.quit()
            return

        print(f"[+] Auto-running: {SERVICE} on {VIDEO_URL}")
        for round_num in range(1, MAX_ROUNDS + 1):
            print(f"\n[Round {round_num}/{MAX_ROUNDS}]")
            self._start_service(SERVICE, VIDEO_URL)
        print(f"\n[DONE] {MAX_ROUNDS} rounds completed.")
        self.driver.quit()

    def _print_banner(self):
        print("+-------------------------------------------+")
        print("|  Zefoy Auto-Follower — Modified by Rat    |")
        print("+-------------------------------------------+\n")

    def _init_driver(self):
        try:
            print("[~] Loading driver...")
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--width=800")
            options.add_argument("--height=700")
            options.binary_location = "/snap/bin/chromium"

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print("[+] Driver loaded")
        except Exception as e:
            print(f"[x] Driver error: {e}")
            exit(1)
        return driver

    def _init_services(self):
        return {
            "followers": {"title": "Followers", "selector": "t-followers-button", "status": None},
            "hearts": {"title": "Hearts", "selector": "t-hearts-button", "status": None},
            "comments_hearts": {"title": "Comments Hearts", "selector": "t-chearts-button", "status": None},
            "views": {"title": "Views", "selector": "t-views-button", "status": None},
            "shares": {"title": "Shares", "selector": "t-shares-button", "status": None},
            "favorites": {"title": "Favorites", "selector": "t-favorites-button", "status": None},
            "live_stream": {"title": "Live Stream", "selector": "t-livesteam-button", "status": None},
        }

    def _solve_captcha(self):
        self._wait_for_element(By.TAG_NAME, "input")
        print("[~] Waiting for captcha...")
        self._wait_for_element(By.LINK_TEXT, "Youtube")
        print("[+] Captcha solved")

    def _check_services_status(self):
        for service in self.services:
            selector = self.services[service]["selector"]
            try:
                el = self.driver.find_element(By.CLASS_NAME, selector)
                self.services[service]["status"] = "[WORKING]" if el.is_enabled() else "[OFFLINE]"
            except NoSuchElementException:
                self.services[service]["status"] = "[OFFLINE]"
        for s in self.services:
            print(f"  {self.services[s]['title']}: {self.services[s]['status']}")

    def _start_service(self, service, video_url):
        self._wait_for_element(By.CLASS_NAME, self.services[service]["selector"]).click()
        container = self._wait_for_element(By.CSS_SELECTOR, "div.col-sm-5.col-xs-12.p-1.container:not(.nonec)")
        inp = container.find_element(By.TAG_NAME, "input")
        inp.clear()
        inp.send_keys(video_url)

        while True:
            container.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
            sleep(3)
            try:
                container.find_element(By.CSS_SELECTOR, "button.btn.btn-dark").click()
                print(f"[✓] {self.services[service]['title']} sent")
            except NoSuchElementException:
                pass
            sleep(3)
            remaining = self._compute_remaining_time(container)
            if remaining:
                m, s = remaining // 60, remaining % 60
                print(f"[~] Sleeping {m}m {s}s")
                sleep(remaining)
                break
            else:
                break

    def _compute_remaining_time(self, container):
        try:
            el = container.find_element(By.CSS_SELECTOR, "span.br")
            text = el.text
            if "Please wait" in text:
                nums = re.findall(r"\d+", text)
                return int(nums[0]) * 60 + int(nums[1]) + 5
        except NoSuchElementException:
            pass
        return None

    def _wait_for_element(self, by, value):
        while True:
            try:
                return self.driver.find_element(by, value)
            except NoSuchElementException:
                sleep(1)

if __name__ == "__main__":
    bot = Bot()
    bot.start()
