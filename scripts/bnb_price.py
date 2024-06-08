import os
import time
import datetime
import requests


root_dct = '.'
url_base = 'https://api.bscscan.com/api'
api_token = 'C1B7V96EQQCQ1I1BWHTAFAWFRJBADRGI8D'
user_address = '0xdca2Df565a4fFACc815957941C5ba727EdcA6A5a'
catgirl ='0x79eBC9A2ce02277A4b5b3A768b1C0A4ed75Bd936'
path_to_html = os.path.join(root_dct, '..', 'index.html')
path_to_html_2 = os.path.join(root_dct, '..', 'prizes.html')


def bnb_price(api_token):
    """
    Get the BNB price in USD.
    """
    
    url_base = 'https://api.bscscan.com/api'
    url = f'{url_base}?module=stats&action=bnbprice&apikey={api_token}'
    
    r = requests.get(url)
    result = r.content
    dct = eval(result)
    
    return dct
    
    
def get_current_prize(path_to_html, flag):
    """
    Get the current prize in the pool (monthly, annual, in BNB or USD).
    IMPORTANT: IN THE FUTURE, CHANGE THIS FUNCTION FOR THE ONE THAT ACTUALLY READS THE AMOUNT OF BNB IN THE MONTHLY PRIZE ADDRESS.
    """

    with open(path_to_html, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if flag in line:
            value = float(line.split(f'"{flag}">')[-1].split('<')[0])
            
    return value
    
    
def update_html(path_to_html, flag, value):
    """
    Read an html and overwrite the prize values for new ones.
    """
    
    with open(path_to_html, 'r') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if flag in line:
            newline = line.split(f'"{flag}">')[0] + f'"{flag}">' + str(round(value, 2)) + '</a>\n'
            lines[i] = newline

    with open(path_to_html, 'w') as f:
        lines = f.writelines(lines)
        
    return
    
    
while True:    
    # Get price of BNB in USD.
    dct = bnb_price(api_token)
    one_bnb_in_usd = float(dct['result']['ethusd'])

    # Update monthly prize.
    amount_of_bnb_month = get_current_prize(path_to_html, "bnb_month")
    amount_of_usd_month = amount_of_bnb_month * one_bnb_in_usd
    update_html(path_to_html, "bnb_month", amount_of_bnb_month)
    update_html(path_to_html, "usd_month", amount_of_usd_month)
    update_html(path_to_html_2, "bnb_month", amount_of_bnb_month)
    update_html(path_to_html_2, "usd_month", amount_of_usd_month)

    # Update annual prize.
    amount_of_bnb_annual = get_current_prize(path_to_html, "bnb_annual")
    amount_of_usd_annual = amount_of_bnb_annual * one_bnb_in_usd
    update_html(path_to_html, "bnb_annual", amount_of_bnb_annual)
    update_html(path_to_html, "usd_annual", amount_of_usd_annual)
    update_html(path_to_html_2, "bnb_annual", amount_of_bnb_annual)
    update_html(path_to_html_2, "usd_annual", amount_of_usd_annual)

    # Print changes.
    print(one_bnb_in_usd)
    print(amount_of_bnb_month, round(amount_of_usd_month, 2))
    print(amount_of_bnb_annual, round(amount_of_usd_annual, 2))
    
    time.sleep(25)
