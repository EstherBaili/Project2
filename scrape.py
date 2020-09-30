#importing modules for web-scraping
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd
import time
import math
from collections import ChainMap

import json

# Google API Key
from config import gkey

# Defining scrape & dictionary
def scrape():

    #Site Navigation
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)   

    #Web Scraping 1- need to interact with the job-seeking website first of all

    jobs_find_url ="https://www.seek.com.au/jobs/in-All-Australia?keywords=%22data%20%20analyst%22"

    browser.visit(jobs_find_url)
    jobs_html=browser.html  


    # Retrieve page with the requests module

    #it was noticed that the seek page had 22 jobs listed per page. Thus in order to obtain the number of pages, first need to obtain the number of pages:
    #Number of jobs listed at the top of the page, the following code obtains this:
    job_soup=bs(jobs_html, 'html.parser')
    job_number=job_soup.find('span', class_="_3FrNV7v _3PZrylH _2heRYaN").text

    number=job_number.strip('jobs found')

    number_1=float(number)
    print(number_1)

    number_pages=math.ceil(number_1/22)
    print(number_pages)

    time.sleep(2)

    #getting the browser html
    #text_list=[]
    job_location=[]
    job_title1=[]
    job_company=[]
    x=range(1,number_pages+1)

    for n in x:
        seek_url=f"https://www.seek.com.au/jobs/in-All-Australia?keywords=%22data%20%20analyst%22&page={n}"
        browser.visit(seek_url)
        seek_html=browser.html  
        seek_soup=bs(seek_html, 'html.parser')
        all_text=seek_soup.find('div', class_='_3MPUOLE')
        job_title=all_text.find_all('span', class_='_3FrNV7v _2IOW3OW HfVIlOd _2heRYaN E6m4BZb')
        extra_class=all_text.find_all('span', class_="Eadjc1o")
        job_characteristics=all_text.find_all('span', class_="_3FrNV7v _3PZrylH E6m4BZb")

        
        #converting each of the elements to text 
    
        #modifying the job location element and tidying up this element

        for element in extra_class:
            element1=element.text
            if "location:" in element1:
                element2=element1.lstrip('location: ')
                job_location.append(element2) 
        
        job_title=all_text.find_all('span', class_='_3FrNV7v _2IOW3OW HfVIlOd _2heRYaN E6m4BZb') 
        
        #editing both the job title and job characterstics

        for item in job_title:
            job1=item.text
            job_title1.append(job1)
        
        for company in job_characteristics:
            company1=company.text
            if company1[:3]=='at ':
                company2=company1.lstrip('at ')
                job_company.append(company2) 
        
        for job_class in extra_class:
            classification1=job_class.text
            if "classification:" in classification1:
                classification2=classification1.lstrip('classification: ')
                job_classification.append(classification2) 
    

        time.sleep(3)

        browser.quit()

    #zip two lists together 

    Job_df = pd.DataFrame(
        {'Job Title': job_title1,
        'Job Location': job_location,
        'Job Company': job_company,
        })

    #removing duplicates if all three columns are the same: 

    Job_df2=Job_df.drop_duplicates()
    #setting up search to use in the API call 
    Job_df2["Search Engine"] = Job_df2["Job Company"].astype(str) + " " + Job_df2["Job Location"].astype(str)

    
    #adding latitude and longitude columns
    Job_df2['Lat'] = ""
    Job_df2['Lng']=""

    for index, row in Job_df2.iterrows():
    
        search_string=row["Search Engine"]
        
        try:
            url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={search_string}&inputtype={gkey}'
            # Run request
            response = requests.get(url)
            search_geo = response.json()
            
        
            Job_df2.loc[index, 'Lat'] = search_geo["candidates"][0]['geometry']['location']['lat']
            Job_df2.loc[index, "Lng"]=search_geo["candidates"][0]['geometry']['location']['lng']

        
        #in the case of a JSONDecode Error, this ensures the code will keep running
        except (KeyError, IndexError, ValueError):
            Job_df2.loc[index, 'Lat'] = "No Coordinates"
            Job_df2.loc[index, 'Lng'] = "No Coordinates"

    #Then delete the ones with no co-ordinates
    final_Job_df=Job_df2.loc[Job_df2['Lat'] != "No Coordinates"]
    
    
    return final_Job_df