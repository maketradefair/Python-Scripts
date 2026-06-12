import requests
import logging
import bs4
from urllib.parse import urlencode

logging.basicConfig(level=logging.DEBUG)

filename = "asset_groups.xml"

soup = bs4.BeautifulSoup(open(filename).read(), 'lxml-xml')

sections = soup.find_all('ASSET_GROUP')

mydict_single_items = {
    'TITLE':None, 
    'BUSINESS_IMPACT':None, 
    'CVSS_ENVIRO_CDP':None, 
    'CVSS_ENVIRO_CR':None, 
    'CVSS_ENVIRO_IR':None, 
    'CVSS_ENVIRO_AR':None,
}
my_dict_lists = {
    'IP_SET': 'ips',
    'DNS_LIST': 'dns_names',
    'DOMAIN_LIST': 'domains',
}

for key, value in mydict_single_items.items():
    if value is None:
        mydict_single_items[key] = key.lower()   # If value is none, we'll use key as urlParameter

creds = ('tatac8sa6','Sw0rdf1sh@090')
requested_with = {"X-Requested-With" : "Python"}
url_fmt = 'https://qualysguard.qg1.apps.qualys.in/api/2.0/fo/asset/group/?action=add&{args}'

for section in sections:
    urlParameters = []
    # Process all single-parameter elements
    for elementname, parameter_name in mydict_single_items.items():      #elementname = mydict keys
        elements = section.find_all(elementname)
        for el in elements:
            if el.text not in ('0', '', 'Not Defined', None):   #if el checks if el exists then does and el.text
                urlParameters.append('{}={}'.format(parameter_name, el.text))
    # Process list-type elements
    for elementname, parameter_name in my_dict_lists.items():
        urlsection = f"{parameter_name}="
        urlsection_values = ""
        # Find all elements of type elementname
        elements = section.find_all(elementname)
        # For each one, comma-join it's child element `text` values
        for parent in elements:
            urlsection_values += ','.join(child.text for child in parent.find_all(True))
        # Append the urlsection for this parameter into urlParameters in the normal way
        if urlsection_values:
            urlParameters.append(urlsection + urlsection_values)

    url = url_fmt.format(args= "&".join(urlParameters))
    #print(url)
    
    response = requests.post(url, auth=creds, headers=requested_with, verify=False)
    print(response.text)