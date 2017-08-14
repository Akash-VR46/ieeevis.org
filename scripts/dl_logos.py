#!/usr/bin/env python

import os
import urllib
import json

DOWNLOADS_DIR = 'attachments/supporters/2017/dl'
logo_links = json.load( open('scripts/tmp/logo-links.json') )

# For every line in the file
for row in logo_links:
    url = row['logo_url']
    # Split on the rightmost / and take everything on the right side of that
    name = row['logo_name']
    # Combine the name and the downloads directory to get the local filename
    filename = os.path.join(DOWNLOADS_DIR, name)
    # download if not already there
    if not os.path.isfile(filename):
        print('dl/making: ', os.path.join(DOWNLOADS_DIR, name))
        urllib.urlretrieve(url, filename)

