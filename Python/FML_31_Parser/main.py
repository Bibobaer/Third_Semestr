from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from DateBaseConnect import Connect
from time import sleep
import asyncio

async def main():
    try:
        db = Connect()
        await db.initialize_connection()
    except Exception:
        exit()
        
    driver = webdriver.WebDriver()
    driver.get("http://fml31.ru")
    news_div = driver.find_element(By.CSS_SELECTOR, "main[id=main]")
    news_list = news_div.find_elements(By.CSS_SELECTOR, "article")

    for news in news_list:
        title = news.find_element(By.CSS_SELECTOR, 'h2 > a').text
        date = news.find_element(By.CSS_SELECTOR, 'div > span > a > time').text
        desct = news.find_element(By.CSS_SELECTOR, 'div > p').text
        auther = news.find_element(By.CSS_SELECTOR, 'div > span > span > a').text
        tags = [tag.text for tag in news.find_elements(By.CSS_SELECTOR, 'footer > span > a')]
        
        if not await db.is_news_exists(title=title):
            await db.add_news(title, date,desct,auther,tags)

        sleep(2)

    driver.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())