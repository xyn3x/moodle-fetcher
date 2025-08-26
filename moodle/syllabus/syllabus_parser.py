from google import genai
import pdfplumber
import os
import time
import requests
import urllib3
from io import BytesIO
from dotenv import load_dotenv, dotenv_values
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

syllabus_tree = {}

def parse_syllabus(driver, url, course_linklist):
    for course_link in course_linklist: 
        driver.get(course_link)
        time.sleep(2)
        linkcontainer_list = driver.find_elements(By.CLASS_NAME, "activityname")
        #print(linkcontainer_list)
        for cur_container in linkcontainer_list:
            try:
                cur_link = cur_container.find_element(By.TAG_NAME, "a")
            except NoSuchElementException:
                continue
            #print(cur_link)
            try: 
                cur_linkname = cur_link.find_element(By.TAG_NAME, "span")
            except NoSuchElementException:
                continue
            cur_linkname = (cur_linkname.get_attribute("innerHTML")).lower()
            if "syllabus" in cur_linkname:
                pdf_url = cur_link.get_attribute("href")
                cookies = {c['name']: c['value'] for c in driver.get_cookies()}
                res = requests.get(pdf_url, cookies=cookies)
                pdf_file = BytesIO(res.content)
                extracted_text = ''
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        if page.extract_text():
                            extracted_text += page.extract_text() + '\n'
               # print(extracted_text)
                client = genai.Client(api_key=os.getenv("genai_api"))

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Give me the answer as a json only. You need to analyze this text and give information of every assigment that affects the grade as a json file. Give information about each assignment like name, its weight and date (if none, then NULL). Also add info about attendance, also in json (maximum absence, and penalty as an object too). Here the texts itself:\n {extracted_text}",
                )
                print(response.text)
