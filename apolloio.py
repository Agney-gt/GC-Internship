import time
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, SoupStrainer
import requests
from random import shuffle
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.common.exceptions import WebDriverException
import pyautogui
import undetected_chromedriver as uc
import pickle
import gspread
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials

option = uc.ChromeOptions()
option.headless = False
option.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
driver=uc.Chrome(use_subprocess=True, options=option, executable_path=r"C:\Users\agney\Desktop\chromedriver-win32\chromedriver.exe")
driver.maximize_window()
dff=pd.DataFrame()
dfaf=pd.DataFrame()
y=0#171
z=0
action = ActionChains(driver)

ay=["https://smartrecruiters.com",
"https://csolsinc.com",
"https://acoustic.com",
"https://novusfunnel.com",
"https://qatalyst.com",
"https://hostland.com",
"https://default.com",
"https://refer.me",
"https://telehost.ch",
]

def AutoLogin():
    driver.get("https://app.apollo.io/")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
def Login():
    driver.get("https://app.apollo.io/#/login")
    time.sleep(10)
    WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,'//input[contains(@name, "email")]')))
    driver.find_element(By.XPATH,'//input[contains(@name, "email")]').send_keys("acc")
    time.sleep(10)
    driver.find_element(By.XPATH,'//input[contains(@name, "password")]').send_keys("pass")
    time.sleep(10)

    driver.find_element(By.XPATH,'//button[.= "Log In"]').click()
    time.sleep(40)
    driver.get('https://app.apollo.io/#/companies?finderViewId=5b6dfc5a73f47568b2e5f11d')

def CompanyWebsite(x,y,df):
    print("Abbc")
    driver.get("https://app.apollo.io/#/companies?finderViewId=5a205be49a57e40c095e1d60&qOrganizationName="+x)
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//div[@data-cy-loaded="true"]')))
            time.sleep(2)
            break
        except Exception as e:
            driver.refresh()
            pass
    time.sleep(5)
    try:
        link=driver.find_element(By.XPATH,'//tr[contains(.,"")]//a').get_attribute('href')
        driver.get(link)
        time.sleep(2)
        driver.find_element(By.XPATH,'//a[contains(.,"Show More")]').click()
        time.sleep(2)
    except Exception as e:
        pass
    try:
        try:
            driver.find_element(By.XPATH,'//a[contains(.,"Show More")]').click()
            time.sleep(2)
        except Exception as e:
            pass
        cdesc=driver.find_element(By.XPATH,'//a[contains(.,"Show Less")]//..').text
        df.at[y,"Company Description"]=cdesc
    except Exception as e:
        pass
    try:
        phone=driver.find_element(By.XPATH,"//button//i[contains(@class,'icon-phone')]/following::span").text
        df.at[y,"Phone Number"]=phone
    except Exception as e:
        pass
    try:
        adesc=driver.find_element(By.XPATH,'//div[contains(text( ), "Company Keywords")]/../div[2]').text
        df.at[y,"Keywords"]=adesc
        #print("ADDESC:",adesc)
    except Exception as e:
        print(e)
        pass
    try:
        aindustry=driver.find_element(By.XPATH,'//div[contains(text( ), "Industry")]/../div[2]/div').text
        df.at[y,"Industry"]=aindustry
        #print("INDUSTRY",aindustry)
    except Exception as e:
        print(e)
        pass
    try:
        employeeCount=driver.find_element(By.XPATH,'//div[contains(text( ), "Employees")]/..//span').text
        df.at[y,"Linkedin_Employee_Count"]=employeeCount
        #print("EMPCOUNT",employeeCount)
        if int(employeeCount.replace(",",""))>200:
            flag=1
        else:
            flag=0
    except Exception as e:
        print(e)
        pass
    
    try:
        loc=driver.find_elements(By.XPATH,"//div[contains(.,'Location')]/following::div[contains(@class,'zp-inline-edit')]")[-1].text
        df.at[y,"Company_Location"]=loc
    except Exception as e:
        pass
    try:
        revenue=driver.find_element(By.XPATH,'//div[contains(text( ), "Revenue")]/../div[@class="zp_hYCdb"]').text
        df.at[y,"Revenue"]=revenue
        #print("REVENUE",revenue)
    except Exception as e:
        print(e)
        pass
    df.to_csv("Company_Details.csv")
    
    q=driver.find_elements(By.XPATH,'//a[contains(@href,"people")]')
    for k in q:
        if("people" in k.get_attribute('href')):
            #print("Lead list link",k.get_attribute('href'))
            mgmt=k.get_attribute('href')+'&personSeniorities[]=owner&personSeniorities[]=founder&personSeniorities[]=c_suite&personSeniorities[]=partner&personSeniorities[]=vp&personSeniorities[]=head&personSeniorities[]=director"'
            senior=k.get_attribute('href')+"&personSeniorities[]=owner&personSeniorities[]=founder&personSeniorities[]=c_suite&personSeniorities[]=vp&personSeniorities[]=director&personSeniorities[]=manager&page=1"
            cto=k.get_attribute('href')+"&personTitles[]=chief&personTitles[]=head&personTitles[]=cto&personTitles[]=founder&personTitles[]=ceo&page=1"
            director=k.get_attribute('href')+"&personTitles[]=director%20Business Development&personTitles[]=director%20Supply Chain&personTitles[]=director%20Operations&personTitles[]=director%20Partnerships&personTitles[]=director%20IT"
            lead=k.get_attribute('href')+"&personTitles[]=lead%20Business Development&personTitles[]=lead%20Supply Chain&personTitles[]=lead%20Operations&personTitles[]=lead%20Partnerships&personTitles[]=lead%20IT"
            head=k.get_attribute('href')+"&personTitles[]=head%20Business Development&personTitles[]=head%20Supply Chain&personTitles[]=head%20Operations&personTitles[]=head%20Partnerships&personTitles[]=head%20IT"
            vp=k.get_attribute('href')+"&personTitles[]=vp%20Business Development&personTitles[]=vp%20Supply Chain&personTitles[]=vp%20Operations&personTitles[]=vp%20Partnerships&personTitles[]=vp%20IT"
            lessthan50=k.get_attribute('href')+"&personSeniorities[]=founder&personSeniorities[]=c_suite"
            sales=k.get_attribute('href')+"&qPersonTitle=Sales&personSeniorities[]=c_suite&personSeniorities[]=vp&personSeniorities[]=head&personSeniorities[]=partner&personSeniorities[]=director"
            
    return lessthan50,sales,flag,df#cto,director,lead,head,vp

def Scrape(dff,df,x,y,z,lessthan50,sales,flag):
    sequence=df['Visited_URL'].to_list()[y]
    #print(sequence)
    toScrape=[]
    if flag==0:
        toScrape=[lessthan50]
    else:
        toScrape=[sales,lessthan50]
    lead_count=0
    for i in toScrape:#[cto,director,lead,head,vp]:
        if 'people?' in i:
            driver.get(i)
            time.sleep(5)
            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//div[@data-cy-loaded="true"]')))
                    time.sleep(2)
                    break
                except Exception as e:
                    driver.refresh()
                    pass#time.sleep(5)
            #print("Got Lead List")
            tablerow=driver.find_elements(By.XPATH,'//tbody[contains(@class, "zp_")]')
            driver.find_element(By.XPATH,'//body').send_keys(Keys.END)
            #if int(employeeCount) < 2000:
            for i in tablerow:
                dff=pd.concat([dff, df.iloc[[y]]], ignore_index = True)

                try:
                    
                    row=i.get_attribute("outerHTML")
                    soup=BeautifulSoup(row,"lxml")
                    name=soup.find("div", class_=re.compile(".*zp_xVJ20.*"))
                    #print(name.text)
                    dff.at[z,"Name"]=name.text
                    desig=soup.find_all("span", class_="zp_Y6y8d")
                    #print(desig)
                    designation=desig[0].text
                    location=desig[1].text
                    dff.at[z,"Designation"]=desig[0].text
                    dff.at[z,"Location"]=desig[1].text
                    try:
                        linkedinURL=i.find_element(By.XPATH,".//a[contains(@href,'linkedin.com/in/')]").get_attribute('href')
                        #print(linkedinURL)                   
                        dff.at[z,"LinkedinURL"]=linkedinURL
                    except Exception as e:
                        pass
                    print(lead_count)
                    if lead_count<4:
                        try:
                        
                            ele=driver.find_element(By.XPATH,'//div[contains(text(), "Access email")]').click()
                            #action.move_to(ele).perform()
                            #time.sleep(5)
                            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "zp_t08Bv")]')))
                            email=driver.find_element(By.XPATH,'//span[contains(@class, "zp_t08Bv")]')
                            #print(email.text)
                            
                            #print("Here")
                            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE*5).perform()
                            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE*5).perform()
                            #print("Pressed ESC")
                            seq_button=WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//button[@data-cy='apollo-sequence-button']")))
                            seq_button[-1].click()
                            #print("Clicked seq_button")
                            time.sleep(5)
                            seq_choice=WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='apolloio-css-vars-reset zp zp-overlay']//input[contains(@class,'Select-input')]")))
                            seq_choice[0].send_keys("",sequence)
                            seq_choice[0].send_keys(Keys.RETURN)
                            #print("Entered Sequence")
                            time.sleep(1)
                            add=driver.find_element(By.XPATH,"//button[contains(.,'Add Now')]")
                            driver.execute_script("arguments[0].scrollIntoView(true);", add)
                            add.click()
                            time.sleep(2)
                            z=z+1
                            lead_count+=1
                            dff.to_csv("Profsp2.csv")
                            #print(dff)
                        except Exception as e:
                            print("Exception",lead_count)
                            print(e)
                            z=z+1
                            dff.to_csv("Profsp2.csv",index=False)
                            pass
                    
                        
                        #linkedinURL=driver.find_element(By.XPATH,'//a[contains(@class, "zp-link zp_3")]')
                        
                        

                except Exception as e:
                    print(e)
    return z,dff
#171 - PSC
for x in ay[y:]:
    if y>0:
        #time.sleep(60)
        
        print(y)
        print(x)
        print(ay[y-1])
        if x==ay[y-1]:
            y=y+1
            continue
        else:
            try:
                print("We are at point 0")
                time.sleep(5)
                #cto,director,lead,head,vp
                lessthan50,sales,flag,df=CompanyWebsite(x.replace("https://",""),y,df)
                z,dff=Scrape(dff,df,x.replace("https://",""),y,z,lessthan50,sales,flag)
                sheet.update_cell(y_count[y]+2,10,1)
                y=y+1
            except Exception as e:
                print("Error Finding the company",e)
                sheet.update_cell(y_count[y]+2,10,1)
                y=y+1
                pass
        if y%100==0:
            print(y,"Here")
            try:
                driver.find_element(By.XPATH, '//button[@class="zp-button zp_zUY3r zp_rhXT_ zp_daRtr"]').click()
                time.sleep(2)
                print("pressed menu")
                driver.find_elements(By.XPATH, '//div[contains(.,"Logout")]')[-1].click()
                time.sleep(2)
                print("logout")
                driver.quit()
            except Exception as e:
                print(e)
                pass
            option = uc.ChromeOptions()
            option.headless = False
            option.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
            driver=uc.Chrome(use_subprocess=True, options=option, executable_path=r"C:\Users\agney\Desktop\chromedriver-win32\chromedriver.exe")
            driver.maximize_window()
            action = ActionChains(driver)
            Login()
            
    else:
        try:
            print("We are at point 1")
            Login()
            #cto,director,lead,head,vp
            lessthan50,sales,flag,df=CompanyWebsite(x.replace("https://",""),y,df)
            z,dff=Scrape(dff,df,x.replace("https://",""),y,z,lessthan50,sales,flag)
            sheet.update_cell(y_count[y]+2,10,1)
            y=y+1
        except Exception as e:
            print("Error Finding the company",e)
            sheet.update_cell(y_count[y]+2,10,1)
            y=y+1
            pass
