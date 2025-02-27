from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
from datetime import datetime, timedelta
import os

def get_review(div: BeautifulSoup) -> dict:
    """
    Receives an HTML div or review, and it will return a dictionary with the review's information.
    """
    review = {}
    Rating = {}

    try:
        name = div.find('p', class_ = '_1p30XHjz2rI- C7Tp-bANpE4-')                     # For getting the name of Customers
        review["Name"] = name.text
    except Exception as e:
        review["Name"] = "N/A"

    try:
        content = div.find("span", class_ = "l9bbXUdC9v0- ZatlKKd1hyc- ukvN6yaH1Ds-")  # For getting the Content of Customers
        review["Content"] = content.text
    except Exception as e:
        review["Content"] = "N/A"

    try:
        date = div.find("p", class_ = "iLkEeQbexGs-").text                                  # For getting the Date of Review
        if "Dined on " in date:
            review["Date"] = date.removeprefix("Dined on ")
        else:                                                                               # If the date is similar to "Dined 6 days ago" then this case will handle that
            formatted_date = datetime.now().date() - timedelta(days=int(date[6]))
            review["Date"] = formatted_date.strftime("%B %d, %Y")
    except Exception as e:
        review["Date"] = "N/A"

    try:
        ratings = div.find_all("li" , class_ = "-k5xpTfSXac-")                         # Getting Each Sub review
        for rating in ratings:
            rating_type, rating_number = rating.text.split(' ')
            Rating[rating_type] = int(rating_number)
    except Exception as e:
        review["Rating"] = {}

    review["Rating"] = Rating
    return review

# Saving the Reviews in the JSON File

def save_to_file(file_path :str,reviews: dict):
    with open(file_path, "w") as json_file:
        json.dump(reviews, json_file, indent=4)
    print(f"All reviews Saved to {file_path}")
    return file_path

def get_dict(file_path: str)->OrderedDict:
    try:
        with open(file_path, 'r') as file:
            return OrderedDict(json.load(file))
    except FileNotFoundError:
        print(f"Reviews file not found. Please ensure '{file_path}' exists.")
        return OrderedDict()

def scrape_website(url: str):
    """
    Given a URL, it saves the reviews of that website in JSON file named with the title of that website
    Returns the JSON file name
    """
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    driver.execute_script("window.scrollTo(0,5000);")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_1BEc9Aeng-Q-")))         # Next Button Location
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gRlAhBweGeE-")))
    reviews = OrderedDict()
    title = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div[1]/div[2]/div/div/div/h1").text
    title = title.replace(" ","_")
    if title + "_reviews.json" in os.listdir("."):
        driver.quit()
        return title + "_reviews.json"
    total_pages = int(driver.find_element(By.CLASS_NAME, "_1BEc9Aeng-Q-").find_element(By.XPATH, ".//div/ul/li[5]/a").text)
    page_number = 1
    number = 0

    while(True):
        # print(f"Scrapping Page {page_number} of 635")
        page_number += 1
        response = BeautifulSoup(driver.page_source, 'html.parser')
        contents = response.find_all('li', class_ = "afkKaa-4T28-")
        for review in contents:
            number += 1
            reviews["Customer " + str(number)] = get_review(review)
        try:
            next_button = (driver.find_element(By.CLASS_NAME, "_1BEc9Aeng-Q-")).find_element(By.XPATH, ".//div/div[2]/a")
            next_button.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "afkKaa-4T28-")))
        except Exception as e:
            if page_number < total_pages:
                driver.refresh()
                driver.execute_script("window.scrollTo(0,5000);")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_1BEc9Aeng-Q-")))         # Next Button Locationr
                page_number -= 1
            else:
                print(e)
                break
    driver.quit()

    # Saving the result in JSON
    
    file_path = title + "_reviews.json"
    return save_to_file(file_path,reviews)
