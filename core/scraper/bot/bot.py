import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.conf import settings
import os
import json


class Bot(webdriver.Chrome):
    """
    Base class the scrapes indeed.com
    """

    def __init__(
        self, options: Options = None, service: Service = None, keep_alive: bool = True
    ) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        super().__init__(options, service, keep_alive)
        self.implicitly_wait(10)

    def start_request(self, url):
        """Make a request to a page"""
        return self.get(url)

    def search(self, field):
        """Search for job posting"""
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

        job_content = self.find_element(By.ID, "jobDescriptionText").text

        return {
            "job_title": job_title,
            "company_name": company_name,
            "company_location": company_location,
            "job_content": job_content,
            "job_url": url,
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
                if obj not in data:
                    data.append(obj)
                    file.seek(0)  # Move the file pointer to the beginning
                    json.dump(data, file, indent=4)
                    file.truncate()
