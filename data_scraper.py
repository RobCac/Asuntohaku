from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_element(id): #takes an element-id and returns true if it can be found
    try:
        webdriver.find_element_by_id(id)
    except:
        print("No cookie check")
        return False
    return True


#Reads username and pw for login
f = open("user.txt","r")
lines = f.readlines()
user_name = lines[0]
password = lines[1]
f.close()


#logs in to etuovi.com account
driver = webdriver.Firefox()
driver.get("https://www.etuovi.com")

#wait for cookie popup
driver.implicitly_wait(10) 
driver.find_element_by_id("almacmp-modalConfirmBtn").click()

#Log in with read credentials
element = driver.find_element_by_link_text("Kirjaudu")
element.click()
element = driver.find_element_by_id("alma-tunnus-username")
element.send_keys(user_name)
element = driver.find_element_by_id("alma-tunnus-password")
element.send_keys(password)
element.send_keys(Keys.RETURN)

#Confirm log in
element = driver.find_element_by_id("alma-tunnus-notification-button-close")
element.click()

#Go to saved search
driver.get("https://www.etuovi.com/myytavat-asunnot?haku=P1548857208")

apartments = driver.find_elements_by_class_name("ListPage__cardContainer__39dKQ")
print(len(apartments))
element.close()