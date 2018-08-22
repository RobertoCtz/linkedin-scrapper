from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pprint as pprint
import time
import copy
import csv



def main():
    profileDict = {}
    driver = webdriver.Chrome(r"C:\Utilities\chromedriver")
    linkedin_login(driver,"robto.ctz@gmail.com", "22Q1!td2Xk^CPLRt")
    access_person_profile(driver, "Mario Chavez")
    profileDict = {**get_contact_info_from_profile(driver), **profileDict}
    profileDict["Jobs"] = get_jobs_experience(driver)
    profileDict["Skills"] = get_skills(driver)

    pprint.pprint(profileDict)

#Returns a string with all the skills separated by a ,
def get_skills(driver):
    time.sleep(2)
    skillList = ""
    #Clicks on website
    driver.find_element_by_class_name("profile-view-grid").click()
    #Expands skill section
    wait_for_element_by_class_name(driver, "pv-skills-section__chevron-icon")
    seeMoreButton = driver.find_element_by_class_name \
        ("pv-skills-section__chevron-icon")
    seeMoreButton.click()
    wait_for_element_by_class_name \
     (driver, "pv-skill-categories-section__expanded")
    time.sleep(0.5)

    #Gets all skills and joins them in a string separated by ,
    skillset = driver.find_elements_by_class_name \
        ("pv-skill-category-entity__name")
    for skill in skillset:
        skillList = skillList + skill.text + ", "

    return skillList[:-1]



#Return a list of dictionaries with all the job experience of the person
def get_jobs_experience(driver):
    dict = {}
    list = []
    jobs = driver.find_elements_by_class_name("pv-position-entity")
    job = driver.find_elements_by_class_name("pv-entity__summary-info")


    for element in jobs:
        details = element.find_elements_by_tag_name("h4")
        position = element.find_element_by_tag_name("h3").text
        dict["Position"] = position

        for field in details:
            text = field.text.splitlines()
            dict[text[0]] = text[1]
        list.append(copy.deepcopy(dict))

    return list




#Returns a dictionary with all the personal information from the candidate
def get_contact_info_from_profile(driver):

    #Get full name from profile
    wait_for_element_by_class_name \
        (driver, "pv-top-card-v2-section__link--contact-info" )
    contactButton = driver.find_element_by_class_name \
        ("pv-top-card-v2-section__link--contact-info")
    nameText = driver.find_element_by_class_name("pv-top-card-section__name")
    dict = {"Name" : nameText.text}

    #Access contact information
    contactButton.click()
    wait_for_element_by_class_name(driver, "pv-contact-info__header" )
    elements = driver.find_elements_by_class_name("pv-contact-info__header")
    for i, element in enumerate(elements):
        if "Connect" in element.text:
            continue

        attribute = driver.find_elements_by_class_name \
            ("pv-contact-info__ci-container")[i].text

        if "Profile" in element.text:
            dict["Profile"] = attribute
            continue

        dict[element.text] = attribute

    #Close window
    exitButton = driver.find_element_by_class_name("artdeco-dismiss")
    exitButton.click()
    time.sleep(0.5)
    return(dict)


#Access a person profile from any page of linkedin
def access_person_profile(driver, name):
    #Search for searchbox
    wait_for_element_by_xpath(driver, "//*[@aria-owns='ember1217-results']" )
    searchTextfield = \
    driver.find_element_by_xpath("//*[@aria-owns='ember1217-results']")
    searchTextfield.clear()
    searchTextfield.send_keys(name)
    time.sleep(0.5)
    #Wait for list to show
    wait_for_element_by_class_name(driver, "search-typeahead-v2__hit")
    hits = driver.find_elements_by_class_name("search-typeahead-v2__hit")
    hits[0].click()
    wait_for_element_by_class_name(driver, "pv-top-card-section__name")

#Login into main page
def linkedin_login(driver, user, password):
    driver.get('https://www.linkedin.com/');
    userTextfield = driver.find_element_by_id("login-email")
    passwordTextfield = driver.find_element_by_id("login-password")
    loginButton = driver.find_element_by_id("login-submit")
    userTextfield.send_keys(user)
    passwordTextfield.send_keys(password)
    loginButton.click()
    time.sleep(0.5)



def wait_for_element_by_class_name(driver, className):
    timeout = 10
    try:
        myElem = WebDriverWait(driver, timeout). \
            until(EC.presence_of_element_located((By.CLASS_NAME, className)))
    except TimeoutException:
        print("Loading took too much time!")

def wait_for_element_by_id(driver, id):
    timeout = 10
    try:
        myElem = WebDriverWait(driver,
         timeout).until(EC.presence_of_element_located((By.ID, id)))
    except TimeoutException:
        print("Loading took too much time!")

def wait_for_element_by_xpath(driver, xpath):
    timeout = 10
    try:
        myElem = WebDriverWait(driver,
         timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Loading took too much time!")

def check_exists_by_class_name(driver, class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True


if __name__ == "__main__":
    main()
