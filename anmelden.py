from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# going through all available Dates and checking if I want it. Stops when found a date that I don't have.
def chooseDay(Datum, Daten, other_active_days, driver, current_month):
    if Datum not in Daten:
        return Datum
    elif len(other_active_days)>0:
        anzahl=0
        for i in range(0, len(other_active_days)):
            day=other_active_days[i].text
            driver.find_element(By.XPATH, "//a[@class='ui-state-default'][contains(text(), '%s')]" % day).click()
            content = driver.find_element(By.ID, 'divSlotsList').text
            while day+'.'+current_month+'.2024' not in content:
                content = driver.find_element(By.ID, 'divSlotsList').text
            Datum = driver.find_element(By.XPATH, "//*[@id='divSlotsList']/div/b").text
            if Datum not in Daten:
                break
            else:
                anzahl+=1
        if anzahl < len(other_active_days):
            return Datum
        else:
            return 'nothing'
    else:
        return 'nothing'



def bookTermin1(url):
    driver = webdriver.Chrome()
    driver.get(url)
    while True:     #loops after successfully booking
        while True:     # loops when no date available and did not go to booking
            start_1=time.time()
            shouldRenew=False
            while True:    # Using WebDriverWait makes things slower, so I prefer While
                try:
                    driver.find_element(By.XPATH, "//*[contains(text(), 'Meldeangelegenheiten')]").click()
                    break
                except:
                    now_time=time.time()
                    if now_time-start_1>10:
                        shouldRenew=True
                        break
                    else:
                        continue
            if shouldRenew == True:
                driver.refresh()
                continue
            driver.find_element(By.XPATH, "//*[contains(text(), 'Wohnsitz an-/ ab-/ ummelden')]").click()
            driver.find_element(By.XPATH, "//*[contains(text(), 'Weiter zur Terminauswahl')]").click()
    
    # at the page to choose Termin
            start_2=time.time()
            content = driver.find_element(By.ID, 'divSlotsList').text
            while content == '':
                content = driver.find_element(By.ID, 'divSlotsList').text
                now_time=time.time()
                if now_time-start_2>10:
                    shouldRenew=True
                    break
            if shouldRenew == True:
                driver.refresh()
                continue
            if 'keine Termine' in content or 'Keine Termine' in content:
                driver.refresh()
                continue
            elif '10.2024' not in content and '11.2024' not in content:   # I only want Termine in Oct or Nov
                driver.refresh()
                continue
            else:
                if '10.2024' in content:
                    current_month='10'
                if '11.2024' in content:
                    current_month='11'
                    
            with open(r'the file where you store the dates you have booked.txt', 'r') as Daten_file:  # change this!
                Daten = Daten_file.read()
                other_active_days = driver.find_elements(By.XPATH, "//a[@class='ui-state-default']")
                Datum = driver.find_element(By.XPATH, "//*[@id='divSlotsList']/div/b").text
                dateOrNo = chooseDay(Datum, Daten, other_active_days, driver, current_month)
                if dateOrNo != 'nothing':
                    break
                elif current_month == '11':
                    driver.refresh()
                    continue
                else: # choose Nov
                    month = Select(driver.find_element(By.XPATH,"//select[@class='ui-datepicker-month']"))
                    month.select_by_visible_text('Nov')
                    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'loader')))
                    try:
                        Datum = driver.find_element(By.XPATH, "//*[@id='divSlotsList']/div/b").text
                    except:
                        driver.refresh()
                        continue
                    current_month = '11'
                    other_active_days = driver.find_elements(By.XPATH, "//a[@class='ui-state-default']")
                    dateOrNo = chooseDay(Datum, Daten, other_active_days, driver, current_month)
                    if dateOrNo != 'nothing':
                        break
                    else:
                        pass
            driver.refresh()
            continue

  # at the page to choose the time period
      
        Datum = dateOrNo

        try:
            driver.find_element(By.ID, "showMoreSlots").click()
        except:
            pass
        slots_list = driver.find_element(By.ID, "divSlotsList")
        items = slots_list.find_elements(By.TAG_NAME, "li")
        Termine = []
        for item in items:
            Termin = item.text
            if Termin !='':
                Termine.append(Termin)
        driver.find_element(By.XPATH, "//*[contains(text(), '%s')]" % Termine[-1]).click()
        
  # at the page to fill in personal information
        
        while True:
            try:
                Anrede = Select(driver.find_element(By.ID,"Salutation"))
                break
            except:
                continue
        Anrede.select_by_value('Frau')

        driver.find_element(By.ID, "FirstName").clear()
        driver.find_element(By.ID, "FirstName").send_keys("My First Name") # change this!
        driver.find_element(By.ID, "LastName").clear()
        driver.find_element(By.ID, "LastName").send_keys("My Last Name") # change this!
        driver.find_element(By.ID, "Email").clear()
        driver.find_element(By.ID, "Email").send_keys("myemail@gmail.com") # change this!

        driver.find_element(By.ID, "Birthday").clear()
        driver.find_element(By.ID, "Birthday").send_keys("1990") # change this!
        driver.find_element(By.ID, "Birthday").send_keys(Keys.ARROW_RIGHT)
        driver.find_element(By.ID, "Birthday").send_keys("01") # change this!
        driver.find_element(By.ID, "Birthday").send_keys(Keys.ARROW_RIGHT)
        driver.find_element(By.ID, "Birthday").send_keys("01") # change this!
        driver.find_element(By.ID, "Phone").clear()
        driver.find_element(By.ID, "Phone").send_keys("11111111111111") # change this!
        
        driver.find_element(By.XPATH, "//div[@class='iti__flag-container']").click()
        driver.find_element(By.XPATH, "//span[@class='iti__country-name' and contains(text(), 'China')]").click() # change this!
        
        # accept terms of service
        
        driver.find_element(By.XPATH, "//div[@id='divUserQueries']/label[1]/span[1]").click()
        driver.find_element(By.XPATH, "//div[@id='divUserQueries']/label[2]/span[2]").click()
        
        # book
        driver.find_element(By.ID, "cmdBookAppointment").click()

        try:
            Success = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'bookSuccess')))
            print('Successfully booked', Datum)
            anFile = open(r'C:\Users\nujiz\OneDrive\Desktop\My Files\an.txt', 'a')
            anFile.write(Datum + '\n')
            anFile.close()
        except:
            try:
                Failed = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'bookFailed')))
                print('Booking failed', Datum)
            except:
                print('sth went wrong')
        driver.refresh()



# Bahnhof
bookTermin1('https://qtermin.de/bahnhofplatzkatschhof?calendarid=57003,57091,57092,57093,57094,71058,71059,71060,71061,71062,77257,77289,77291,77292,133608,133610,133607,133612,133614,133615,133616')
