import time
from urllib.parse import urljoin
import uuid
from celery import shared_task
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from .utils import normalize_url, should_visit_url
from .models import ScreenshotTask, Screenshot


@shared_task
def capture_screenshots(task_id, start_url, num_links):
    driver = webdriver.Chrome()

    task = ScreenshotTask.objects.get(task_id=task_id)

    urls_to_visit = [normalize_url(start_url)]
    visited_urls = set()

    for url in urls_to_visit:
        if len(visited_urls) >= num_links:
            break

        driver.get(url)
        time.sleep(3)
        try:
            accept_button = driver.find_element(By.XPATH, '//button[text()="Accept"]')
            accept_button.click()
        except NoSuchElementException:
            try:
                agree_button = driver.find_element(By.XPATH, '//button[text()="I Agree"]')
                agree_button.click()
            except NoSuchElementException:
                try:
                    agree_button = driver.find_element(By.XPATH, '//button[text()="Accept All"]')
                    agree_button.click()
                except NoSuchElementException:
                    print("Neither 'Accept' or 'Accept All' nor 'I Agree' button found.")

        screenshot_binary = driver.get_screenshot_as_png()
        screenshot_filename = f'{url}--{uuid.uuid4()}.png'

        task = ScreenshotTask.objects.get(task_id=task_id)
        screenshot = Screenshot.objects.create(task=task, url=url)
        screenshot.image.save(screenshot_filename, ContentFile(screenshot_binary))
        screenshot.save()

        visited_urls.add(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in soup.find_all('a', href=True):

            link_url = urljoin(url, link['href'])
            if should_visit_url(link_url, start_url, visited_urls):
                urls_to_visit.append(normalize_url(link_url))
                if len(urls_to_visit) >= num_links + 1:
                    break

    driver.quit()
