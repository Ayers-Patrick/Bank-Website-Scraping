# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def all_us_pr_bank_websiites():
    # source for banks and websites
    
    url = 'http://www.thecommunitybanker.com/bank_links/'
    
    # use state codes for easier df filtering
    
    two_letter_codes = {
        'Alabama' : 'AL',
        'Alaska' : 'AK',
        'Arizona' : 'AZ',
        'Arkansas' : 'AR',
        'California' : 'CA',
        'Colorado' : 'CO',
        'Connecticut' : 'CT',
        'Delaware' : 'DE',
        'Florida' : 'FL',
        'Georgia' : 'GA',
        'Hawaii' : 'HI',
        'Idaho' : 'ID',
        'Illinois' : 'IL',
        'Indiana' : 'IN',
        'Iowa' : 'IA',
        'Kansas' : 'KS',
        'Kentucky' : 'KY',
        'Louisiana' : 'LA',
        'Maine' : 'ME',
        'Maryland' : 'MD',
        'Massachusetts' : 'MA',
        'Michigan' : 'MI',
        'Minnesota' : 'MN',
        'Mississippi' : 'MS',
        'Missouri' : 'MO',
        'Montana' : 'MT',
        'Nebraska' : 'NE',
        'Nevada' : 'NV',
        'New Hampshire' : 'NH',
        'New Jersey' : 'NJ',
        'New Mexico' : 'NM',
        'New York' : 'NY',
        'North Carolina' : 'NC',
        'North Dakota' : 'ND',
        'Ohio' : 'OH',
        'Oklahoma' : 'OK',
        'Oregon' : 'OR',
        'Pennsylvania' : 'PA',
        'Puerto Rico' : 'PR',
        'Rhode Island' : 'RI',
        'South Carolina' : 'SC',
        'South Dakota' : 'SD',
        'Tennessee' : 'TN',
        'Texas' : 'TX',
        'Utah' : 'UT',
        'Vermont' : 'VT',
        'Virginia' : 'VA',
        'Washington' : 'WA',
        'Washington Dc' : 'DC',
        'West Virginia' : 'WV',
        'Wisconsin' : 'WI',
        'Wyoming' : 'WY',
    }
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
   
    states = []
    state_bank_dict = {}
    
    #retrieve urls for each state and PR
    
    for state in soup.select('body div:nth-of-type(2) td:nth-of-type(1) a'):
        states.append(state.get('href'))
        
    for state in states:
        bank_dict = {}
        
        #convert state names to two letter codes
        
        p = re.compile('(?<=usa_)[a-z_]+')
        state_code = two_letter_codes[p.search(state)[0].replace('_', ' ').title()]
        
        state_url = url + state
        state_response = requests.get(state_url)
        state_soup = BeautifulSoup(state_response.text, 'html.parser')
        banks_and_urls = state_soup.select('body table:nth-of-type(2) table:nth-of-type(2) ul a[href]')
        
        for b in banks_and_urls:
            
            #remove formatting from bank names
            
            bank_name = re.sub('(\\r\\n( {13}| {11})|\\r\\n\\t\\t\\t|\\n)', '', b.get_text())
            bank_dict[bank_name] = b.get('href')
        
        state_bank_dict[state_code] = bank_dict
        
        #make info into legible dataframe
        
        state_bank_df = pd.DataFrame.from_dict(state_bank_dict, orient='index').stack()
    
    return state_bank_df

all_us_pr_bank_websiites()