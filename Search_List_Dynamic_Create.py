
import requests
import logging
import re
import bs4 
from urllib.parse import urlencode, quote_plus

logging.basicConfig(level=logging.DEBUG)

filename = "Dynamic-Search-Lists.xml"

soup = bs4.BeautifulSoup(open(filename).read(), 'lxml-xml')

creds = ('redfAmc','API@m!grati0n')
requested_with = {"X-Requested-With" : "Python"}
# print(soup)

def gettext(el):
    return el.text

def yes_no_to_binary(el):
    if el.text == 'Yes':
        return '1'
    else:
        return '0'

def greater_or_less_than_to_code(el):
    if '&gt;=' in el.text:
        return '1'
    elif '&lt;=' in el.text:
        return '2'
    raise Exception('Greater than or less than value not interpretted [' + str(el.text) + ']') 


def discovery_method(el):
    if el.text == 'All':
        return 'ALL'
    elif el.text == 'Authenticated Only':
        return 'Authenticated'
    else:
        return (el.text)


def qualys_top_lists(el):
    list_split = el.text.split(',')
    values = ["_".join(item.split()[1:]) for item in list_split]
    return ",".join(values)


def get_published_params(el):
    param_string = ''
    if "Last" in el.text:
        days = re.findall('\d+', el.text)
        if len(days) != 1:
            print("ERROR: could not extract number of days:", days)
            return ''
        days = days[0]
        param_string += '&published_date_within_last_days=' + days
    else:
        daterange = el.text
        daterange = daterange.replace('NOT', '').strip()
        param_string += '&published_date_between=' + daterange    
    if "NOT" in el.text:
        param_string += '&not_published=1'
    else:
        param_string += '&not_published=0'
    return param_string


element_mappings = {
    'TITLE': ('title', gettext), # lambda el: el.text),
    'GLOBAL': ('global', yes_no_to_binary), # lambda el: '1' if el.text == 'Yes' else '0') 
    'CRITERIA.VULNERABILITY_TITLE': ('vuln_title', gettext),  
    'CRITERIA.DISCOVERY_METHOD' : ('discovery_methods', discovery_method),
    'CRITERIA.CONFIRMED_SEVERITY' : ('confirmed_severities', gettext),
    'CRITERIA.CVE_ID' : ('cve_ids', gettext),
    'CRITERIA.VENDOR_REFERENCE' : ('vendor_refs', gettext),
    'CRITERIA.SUPPORTED_MODULES' : ('supported_modules', gettext),
    'CRITERIA.POTENTIAL_SEVERITY' : ('potential_severities', gettext),
    'CRITERIA.CONFIRMED_SEVERITY' : ('confirmed_severities', gettext),
    'CRITERIA.INFORMATION_SEVERITY' : ('ig_severities', gettext),
    'CRITERIA.QUALYS_TOP_20' : ('qualys_top_lists', qualys_top_lists),
    'CRITERIA.PATCH_AVAILABLE' : ('patch_available', yes_no_to_binary),
    'CRITERIA.PUBLISHED' : (None, get_published_params),
    'CRITERIA.VIRTUAL_PATCH_AVAILABLE' : ('virtual_patch_available', yes_no_to_binary),
    'CRITERIA.CVSS_BASE_SCORE' : ('cvss_base', gettext),
    'CRITERIA.CVSS3_BASE_SCORE' : ('cvss3_base', gettext),
    'CRITERIA.CVSS_BASE_SCORE_OPERAND' : ('cvss_base_operand', greater_or_less_than_to_code),
    'CRITERIA.CVSS3_BASE_SCORE_OPERAND' : ('cvss3_base_operand', greater_or_less_than_to_code),
    'CRITERIA.ASSOCIATED_MALWARE' : ('malware_associated', gettext),
    'CRITERIA.CATEGORY' : ('categories', gettext),
    'CRITERIA.VENDOR' : ('vendor_refs', gettext),
    'CRITERIA.CVE_ID' : ('cve_ids', gettext),
    'CRITERIA.COMPLIANCE_TYPE' : ('compliance_types=', gettext),

}


for search_list in soup.find_all('DYNAMIC_LIST'):
    api_url = 'https://qualysapi.qg1.apps.qualysksa.com/api/2.0/fo/qid/search_list/dynamic/?action=create'
    
    for element_names, (param_name, mapping_function) in element_mappings.items():
        element = search_list
        for element_name in element_names.split('.'):
            element = element.find(element_name)
            if element is None:
                break
        if element is None:
            continue
        if param_name is None:
            api_url += mapping_function(element)
        else:
            value = mapping_function(element)
            api_url += '&' + quote_plus(param_name) + '=' + quote_plus(value)

    #print(api_url)
    response = requests.post(api_url, auth=creds, headers=requested_with, verify=False)
    print(response.text)
