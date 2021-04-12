from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re


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
    try:
        driver.find_element_by_id("almacmp-modalConfirmBtn").click()
    except:
        pass
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
        try:
            vmh_ele = driver.find_element_by_xpath('//*[@id="previousDebtFreePrice"]')
        except:
            try:
                vmh_ele = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section/div[2]/div/div/div[3]/div[2]/div[3]/div[4]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[2]')
            except:
                vmh_ele = 0
            
        vmh = vmh_ele.text
        pinta_ele = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section/div[2]/div/div/div[3]/div[2]/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[7]/div[2]/span')
        pinta = pinta_ele.text
        posti_ele = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/section/div[2]/div/div/div[3]/div[2]/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[2]/ul')
        postire = re.search(r"\b\d{5}\b", posti_ele.text)
        try:
            posti = str(postire.group())
        except:
            posti = '00000'
        
        pinta = pinta.replace(',','.')
        
        kohde = {'Osoite' : osoite, 'Vmh' : vmh, 'Pinta-ala' : pinta , 'URL' : link, 'Postinmr' : posti}
        df = df.append(kohde, ignore_index=True)

    #Saving to csv, for logging and possible other usage. Later into SQL?    
    df.to_csv('dataactual.csv', header=True, index=False)
    driver.close()
    return df
    # In the end will just return dataframe?
    



def hintakehitys_scraper():
    df = pd.DataFrame(columns = ['Postinmr', 'Keskineliöhinta', '1v-muutosprosentti', '5v-muutosprosentti'])
    driver = webdriver.Firefox()
    driver.get("https://blok.ai/asuinaluevertailu/")
    driver.implicitly_wait(10) 
    try:
        driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/form/div/div[1]/button").click()
    except:
        print("no element found")
        pass
    Values_o = driver.find_elements_by_class_name("odd")
    Values_e = driver.find_elements_by_class_name("even")
    for value in Values_o:
        text = value.text
        text = text.split(' ')
        row = {
            'Postinmr' : str(text[2]),
            'Keskineliöhinta' : text[-3], 
            '1v-muutosprosentti': text[-2],
            '5v-muutosprosentti': text[-1]
            }
        df = df.append(row, ignore_index= True)
    for value in Values_e:
        text = value.text
        text = text.split(' ')
        row = {
            'Postinmr' : str(text[2]),
            'Keskineliöhinta' : text[-3], 
            '1v-muutosprosentti': text[-2],
            '5v-muutosprosentti': text[-1]
            }
        df = df.append(row, ignore_index= True)
    df.to_csv('Area_data.csv', header=True, index=False)
    
    driver.close()
    return df
#etuovi_get_apartments()
#hintakehitys_scraper()