#!/usr/bin/env python

"""
Create supporters JSON file (per year)

Lane Harrison and Carlos Scheidegger, 2017

We recommend you use this under a virtual environment. Create
a virtualenv and then install the required libraries with

$ pip install -r requirements.txt

If you need to run this locally, please contact Lane or Carlos for
the private key to access the spreadsheet from the script.

"""

from data import *
from pandas import *
import pandas as pd
import json
import os

YEAR = 2017
LOGOS_DIR = '/attachments/supporters/2017/dl/converted'

##############################################################################

def sortable_date(t):
    try:
        d = t['Date Paid']
        d = d.split('/')
        r = int(d[2]), int(d[0]), int(d[1])
    except:
        print t
        raise
    return r # YMD is sortable

sponsors_category_order = {
    "Diamond": 0,
    "Platinum": 1,
    "Gold": 2,
    "Silver": 3,
    "Academic": 4,
    "NonProfit/Small Company/Startup": 5,
    "Non-profit": 5,
    "Publisher": 6
    }

sponsors_category_remap = {
    "Non-profit": "NonProfit/Small Company/Startup"
    }

gc1 = get_spreadsheet("Finance Fast Facts")
supporters = load_sheet_by_name(gc1, "Supporters").get_all_records()

# payment exception
for i,d in enumerate(supporters):
    if d['Company']=='Uncharted Software Inc.':
        supporters[i]['Received'] = 3000
        supporters[i]['Date Paid'] = "8/2/2017"

supporters = sorted(filter(lambda t: (t['Company'] != "TOTAL" and
                                      t['Received'] != "" and t['Date Paid'] != ""), supporters), key=sortable_date)

logo_file = json.load(open("scripts/tmp/logo-links.json"))
# logo exception
logo_file.append( {"Company": 'Tableau Software', "logo_name": 'logo-tableau'})
supporters = inner_join(logo_file, supporters, 'Company')

link_file = json.load(open("js/sponsor_links.json"))
supporters = left_outer_join(supporters, link_file, 'Company')

supporters = group_by(supporters, lambda t: t['Category'])
supporters = sorted(supporters, key=lambda t: sponsors_category_order[t['Key']])

old_supporters = json.load(open("js/all_sponsors.json"))
# filter out this year's supporters, since we're going to update it to the spreadsheet
new_supporters = filter(lambda t: t['year'] != YEAR, old_supporters)

for group in supporters:
    for supporter in group['Value']:
        d = {
            "company": supporter["Company"],
            "class": sponsors_category_remap.get(supporter['Category'], supporter['Category']),
            "href": supporter['href'] if supporter.get('href') else '', 
            "src": os.path.splitext( os.path.join(LOGOS_DIR, supporter["logo_name"]) )[0]+'.png' , # FIXME
            "year": YEAR
            }
        new_supporters.append(d)

print json.dumps(new_supporters, indent=4)
