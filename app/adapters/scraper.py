from playwright.sync_api import sync_playwright
import time
import requests
from bs4 import BeautifulSoup
import urllib3
from app.core.config import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class webScraper:
    def __init__(self):
        # A shared disguise for both scrapers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        }
    
    def scrape_with_bs4(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                page_title = soup.title.string if soup.title else ""
                og_title = soup.find("meta", property="og:title")
                og_desc = soup.find("meta", property="og:description")

                extracted_text = f"Title: {page_title}\n"

                if og_title:
                    extracted_text += f"Product: {og_title.get('content')}\n"
                
                if og_desc:
                    extracted_text += f"Description: {og_desc.get('content')}\n"
                
                extracted_text += "\n" + soup.get_text(separator=' ', strip=True)
                return extracted_text
            else:
                return f"Failed to scrape. Status code: {response.status_code}"
        except Exception as e:
            return f"Error scraping URL: {str(e)}"

    def scrape_with_playwright(self, url: str) -> str:
        try:
            with sync_playwright() as p:
                # Launch a hidden Chrome browser
                browser = p.chromium.launch(headless=False)
                page = browser.new_page(
                    user_agent=self.headers["User-Agent"]
                )

                try:
                    # Go to the URL and wait for the page JavaScript to load
                    page.goto(url, wait_until="networkidle", timeout=15000)
                    time.sleep(3)
                except Exception:
                    # Asian marketplaces are heavy, sometimes it times out waiting for ads to load. We ignore it.
                    pass 
                
                # Copy absolutely all visible text on the page
                raw_text = page.evaluate("document.body.innerText")

                browser.close()

                return raw_text
        except Exception as e:
            return f"Playwright Error: {str(e)}"
    
    def scrape_with_browserless(self, url: str) -> str:
        try:
            # We use the REST API of Browserless so the firewall doesn't block it!
            api_url = f"https://chrome.browserless.io/content?token={settings.BROWSERLESS_API_KEY}"
            
            # We tell Browserless to go to the URL and wait 5 seconds for Shopee's heavy JavaScript to render
            payload = {
                "url": url,
                "waitFor": 5000
            }

            # Send the request (verify=False to bypass your firewall as before)
            response = requests.post(api_url, json=payload, timeout=30, verify=False)

            if response.status_code == 200:
                # Browserless gives us the FULLY RENDERED HTML, just like a real browser!
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract the visible text
                page_title = soup.title.string if soup.title else ""

                extracted_text = f"Title: {page_title}\n\n"
                extracted_text += soup.get_text(separator=' ', strip=True)

                return extracted_text
            else:
                return f"Browserless Error. Status code: {response.status_code}. Response: {response.text}"
        except Exception as e:
            return f"Error contacting Browserless: {str(e)}"