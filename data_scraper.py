from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def etuovi_get_apartments():
    #Reads username and pw for login
    f = open("user.txt","r")
    lines = f.readlines()
    user_name = lines[0]
    password = lines[1]
    f.close()
    #create dataframe. In future will come as input?
    apart_cols = ['Osoite', 'Vmh', 'Pinta-ala', 'URL']
    df = pd.DataFrame(columns = apart_cols)

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

    #get all listings
    apartments = driver.find_elements_by_class_name("styles__cardLink__2Oh5I")

    links = []
    for result in apartments:
        links.append(result.get_attribute('href'))

    for link in links:
        driver.get(link)
        osoite_ele = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section/div[2]/div/div/div[3]/div[2]/div[1]/div/div[1]/div/div[1]/h1')
        osoite = osoite_ele.text
        vmh_ele = driver.find_element_by_xpath('//*[@id="previousDebtFreePrice"]')
        vmh = vmh_ele.text
        pinta_ele = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section/div[2]/div/div/div[3]/div[2]/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[7]/div[2]/span')
        pinta = pinta_ele.text
        kohde = {'Osoite' : osoite, 'Vmh' : vmh, 'Pinta-ala' : pinta , 'URL' : link}
        df = df.append(kohde, ignore_index=True)
    df.to_csv('data.csv', header=True)
    #return df

etuovi_get_apartments()