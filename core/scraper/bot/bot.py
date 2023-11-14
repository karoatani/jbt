import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import json


class Bot(webdriver.Chrome):
    """
    Base class the scrapes indeed.com
    """

    def __init__(
        self, options: Options = None, service: Service = None, keep_alive: bool = True
    ) -> None:
        #
        super().__init__(options, service, keep_alive)
        self.implicitly_wait(10)

    def start_request(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
        return self.get(url)

    def search(self, field):
        search_form = self.find_element(By.ID, "jobsearch")
        search_field = search_form.find_element(By.ID, "text-input-what")
        btn = search_form.find_element(
            By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton"
        )
        search_field.send_keys(field)
        btn.click()

    def get_jobs(self):
        jobs = self.find_elements(By.CLASS_NAME, "job_seen_beacon")

        next_page = ""
        urls = []

        for job in jobs:
            url = (
                job.find_element(By.TAG_NAME, "h2")
                .find_element(By.TAG_NAME, "a")
                .get_attribute("href")
            )
            urls.append(url)

        for url in urls:
            obj = self.get_job_info(url)
            self.to_json(obj)

        try:
            next_page = self.find_element(
                By.XPATH, '//a[@data-testid = "pagination-page-next"]'
            )
            next_page.click()
            self.get_jobs()
        except:
            return

    def get_job_info(self, url):
        """Gets informaton about a job
        returns job(obj)
        """
        self.get(url)
        job_title = (
            self.find_element(By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
            .find_element(By.TAG_NAME, "span")
            .text
        )
        company_name = (
            self.find_element(By.CLASS_NAME, "jobsearch-CompanyInfoWithoutHeaderImage")
            .find_element(By.TAG_NAME, "a")
            .text
        )

        company_location = self.find_element(
            By.XPATH, '//div[@data-testid = "inlineHeader-companyLocation"]'
        ).text

        try:
            job_type = self.find_element(By.XPATH, "//p[text()='Job Type:']").text or ""
        except:
            job_type = " "
            pass

        job_content = self.find_element(By.ID, "jobDescriptionText").text

        return {
            "job title": job_title,
            "company_name": company_name,
            "company_location": company_location,
            "job type": job_type,
            "job content": job_content,
            "url": url,
        }

    def to_json(self, obj):
        """Convert dictionary objects to json"""
        path = os.path.join(os.getcwd(), "data")
        file_path = os.path.join(path, "data.json")

        if not os.path.exists(path):
            os.makedirs(path)
            with open(file_path, "w") as file:
                json.dump([], file)
        else:
            with open(file_path, "r+") as file:
                data = json.load(file)
                data.append(obj)
                file.seek(0)  # Move the file pointer to the beginning
                json.dump(data, file, indent=4)
                file.truncate()