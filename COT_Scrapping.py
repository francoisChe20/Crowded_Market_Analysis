#################################################################################################################
### 1°/ IMPORT LIBRAIRIES
#################################################################################################################

from Tools import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import warnings
warnings.filterwarnings("ignore")

import requests

#################################################################################################################
### 2) SCRAP POSITIONING DATA:
###     - Traders in Financial Report
###     - The Disaggregated Report
###     - The Legacy Report
#################################################################################################################

def get_cot_data():

    print('Scrapping started')
    print('Legacy Report')

    df_legacy = get_legacy_data()
    time.sleep(2)
    df_legacy = filter_contracts(df_legacy)

    print('Disaggregated Report')

    df_disaggregated = get_disaggregated_data()
    time.sleep(2)
    df_disaggregated = filter_contracts(df_disaggregated)

    print('Traders in Financials Report')

    df_tff = get_tff_data()
    time.sleep(2)
    df_tff = filter_contracts(df_tff)

    print('End of the scrapping')

    return [df_legacy, df_disaggregated, df_tff]



def get_tff_data():

    print('Chrome Launching ...')
    chrome = webdriver.Chrome()

    future_name = []
    contracts_id = []
    open_interest = []
    long_pos_dealer = []
    long_pos_asset_manager = []
    long_pos_leveraged_funds = []
    long_pos_other = []
    long_pos_nonreportables = []
    short_pos_dealer = []
    short_pos_asset_manager = []
    short_pos_leveraged_funds = []
    short_pos_other = []
    short_pos_nonreportables = []
    spread_dealer = []
    spread_asset_manager = []
    spread_leveraged_funds = []
    spread_other = []


    df = pd.DataFrame({})
    url = 'https://www.cftc.gov/dea/futures/financial_lf.htm'

    chrome.get(url)
    print(url)
    time.sleep(1)
    response = chrome.page_source
    temp = response.split('<pre')[1]
    list = temp.split('Dealer')[1:]

    for i in list:

        sections = i.split('-----------------------------------------------------------------------------------------------------------------------------------------------------------\n')[1]
        future_name.append(sections.split(' -')[0])
        contracts_id.append(sections.split('CFTC Code #')[1].split()[0])
        open_interest.append(int(sections.split('Open Interest is')[1].split('\n')[0].replace(' ', '').replace(',','')))

        positions = sections.split('Positions')[1].split('\n')[1]
        split_values = positions.split()
        final = [value for value in split_values if value.strip() != '']
        
        # dealers
        total_long = int(final[0].replace(',',''))
        long_pos_dealer.append(total_long)
        total_short = int(final[1].replace(',',''))
        short_pos_dealer.append(total_short)
        spread = int(final[2].replace(',',''))
        spread_dealer.append(spread)

        # Asset Managers
        total_long = int(final[3].replace(',',''))
        long_pos_asset_manager.append(total_long)
        total_short = int(final[4].replace(',',''))
        short_pos_asset_manager.append (total_short)
        spread = int(final[5].replace(',',''))
        spread_asset_manager.append(spread)

        # Leveraged Funds
        total_long = int(final[6].replace(',',''))
        long_pos_leveraged_funds.append(total_long)
        total_short = int(final[7].replace(',',''))
        short_pos_leveraged_funds.append (total_short)
        spread = int(final[8].replace(',',''))
        spread_leveraged_funds.append(spread)

        # other reportables
        total_long = int(final[9].replace(',',''))
        long_pos_other.append(total_long)
        total_short = int(final[10].replace(',',''))
        short_pos_other.append (total_short)
        spread = int(final[11].replace(',',''))
        spread_other.append(spread)

        # nonreportables
        total_long = int(final[12].replace(',',''))
        long_pos_nonreportables.append(total_long)
        total_short = int(final[13].replace(',',''))
        short_pos_nonreportables.append(total_short)
        


    df['Market_and_Exchange_Names'] = future_name
    df['CFTC_Contract_Market_Code'] = contracts_id
    df['Open_Interest_All'] = open_interest
    df['Dealer_Positions_Long_All'] = long_pos_dealer
    df['Dealer_Positions_Short_All'] = short_pos_dealer
    df['Dealer_Positions_Spread_All'] = spread_dealer
    df['Asset_Mgr_Positions_Long_All'] = long_pos_asset_manager
    df['Asset_Mgr_Positions_Short_All'] = short_pos_asset_manager
    df['Asset_Mgr_Positions_Spread_All'] = spread_asset_manager
    df['Lev_Money_Positions_Long_All'] = long_pos_leveraged_funds
    df['Lev_Money_Positions_Short_All'] = short_pos_leveraged_funds
    df['Lev_Money_Positions_Spread_All'] = spread_leveraged_funds
    df['Other_Rept_Positions_Long_All'] = long_pos_other
    df['Other_Rept_Positions_Short_All'] = short_pos_other
    df['Other_Rept_Positions_Spread_All'] = spread_other
    df['NonRept_Positions_Long_All'] = long_pos_nonreportables
    df['NonRept_Positions_Short_All'] = short_pos_nonreportables

    print('Data successfully extracted')
    chrome.quit()
    print('Chrome closed')

    return df


def get_disaggregated_data():

    print('Chrome Launching ...')
    chrome = webdriver.Chrome()

    future_name = []
    contracts_id = []
    open_interest = []
    long_pos_producers = []
    long_pos_swap_dealers = []
    long_pos_managed_money = []
    long_pos_other = []
    short_pos_producers = []
    short_pos_swap_dealers = []
    short_pos_managed_money = []
    short_pos_other = []
    spread_swap_dealers = []
    spread_managed_money = []
    spread_other = []

    df = pd.DataFrame({})
    urls = [
            'https://www.cftc.gov/dea/futures/petroleum_sf.htm',
            'https://www.cftc.gov/dea/futures/nat_gas_sf.htm',
            'https://www.cftc.gov/dea/futures/electricity_sf.htm',
            'https://www.cftc.gov/dea/futures/other_sf.htm',
            'https://www.cftc.gov/dea/futures/ag_sf.htm',]
    
    for url in urls:
        print(url)

        chrome.get(url)
        time.sleep(1)
        response = chrome.page_source
        temp = response.split('<pre')[1]
        list = temp.split('Spreading :\n----------------------------------------------------------------------------------------------------------------\n')[1:]

        for i in list:

            future_name.append(i.split(' -')[0])
            contracts_id.append(i.split('CFTC Code #')[1].split()[0])
            open_interest.append(int(i.split('Open Interest is')[1].split(':')[0].replace(' ', '').replace(',','')))

            positions = i.split('Positions')[1].split(':\n:')[1].split(':')[0]
            split_values = positions.split()
            final = [value for value in split_values if value.strip() != '']
            
            # Producers
            total_long = int(final[0].replace(',',''))
            long_pos_producers.append(total_long)
            total_short = int(final[1].replace(',',''))
            short_pos_producers.append(total_short)

            # Swap Dealers
            total_long = int(final[2].replace(',',''))
            long_pos_swap_dealers.append(total_long)
            total_short = int(final[3].replace(',',''))
            short_pos_swap_dealers.append (total_short)
            spread = int(final[4].replace(',',''))
            spread_swap_dealers.append(spread)


            # Managed Money
            total_long = int(final[5].replace(',',''))
            long_pos_managed_money.append(total_long)
            total_short = int(final[6].replace(',',''))
            short_pos_managed_money.append (total_short)
            spread = int(final[7].replace(',',''))
            spread_managed_money.append(spread)

            # other reportables
            total_long = int(final[8].replace(',',''))
            long_pos_other.append(total_long)
            total_short = int(final[9].replace(',',''))
            short_pos_other.append(total_short)
            spread = int(final[10].replace(',',''))
            spread_other.append(spread)


    df['Market_and_Exchange_Names'] = future_name
    df['CFTC_Contract_Market_Code'] = contracts_id
    df['Open_Interest_All'] = open_interest
    df['Prod_Merc_Positions_Long_All'] = long_pos_producers
    df['Prod_Merc_Positions_Short_All'] = short_pos_producers
    df['Swap_Positions_Long_All'] = long_pos_swap_dealers
    df['Swap__Positions_Short_All'] = short_pos_swap_dealers
    df['Swap__Positions_Spread_All'] = spread_swap_dealers
    df['M_Money_Positions_Long_All'] = long_pos_managed_money
    df['M_Money_Positions_Short_All'] = short_pos_managed_money
    df['M_Money_Positions_Spread_All'] = spread_managed_money
    df['Other_Rept_Positions_Long_All'] = long_pos_other
    df['Other_Rept_Positions_Short_All'] = short_pos_other
    df['Other_Rept_Positions_Spread_All'] = spread_other


    print('Data successfully extracted')
    chrome.quit()
    print('Chrome closed')

    return df


def get_legacy_data():

    print('Chrome Launching ...')
    chrome = webdriver.Chrome()

    future_name = []
    contracts_id = []
    open_interest = []
    long_pos_noncommercials = []
    long_pos_commercials = []
    long_pos_nonrep = []

    short_pos_noncommercials = []
    short_pos_commercials = []
    short_pos_nonrep = []
    spread_noncommercials = []

    df = pd.DataFrame({})
    urls = [
            'https://www.cftc.gov/dea/futures/deacbtsf.htm',
            'https://www.cftc.gov/dea/futures/deacmesf.htm',
            'https://www.cftc.gov/dea/futures/deacboesf.htm',
            'https://www.cftc.gov/dea/futures/deamgesf.htm',
            'https://www.cftc.gov/dea/futures/deacmxsf.htm',
            'https://www.cftc.gov/dea/futures/deanybtsf.htm',
            'https://www.cftc.gov/dea/futures/deaiceusf.htm',
            'https://www.cftc.gov/dea/futures/deaifedsf.htm',
            'https://www.cftc.gov/dea/futures/deanymesf.htm',
            'https://www.cftc.gov/dea/futures/deanodxsf.htm'
            ]
    
    for url in urls:
        print(url)

        chrome.get(url)
        time.sleep(1)

        response = chrome.page_source
        temp = response.split('\n \n \n')[1:]

        for i in temp:

            future_name.append(i.split(' -')[0])
            contracts_id.append(i.split('Code-')[1].split('\n')[0])
            open_interest.append(int(i.split('OPEN INTEREST:')[1].split('\n')[0].replace(' ', '').replace(',','')))

            positions = i.split('\nCOMMITMENTS\n')[1]
            split_values = positions.split()
            final = [value for value in split_values if value.strip() != '']
            
            # Non Commercials
            total_long = int(final[0].replace(',',''))
            long_pos_noncommercials.append(total_long)
            total_short = int(final[1].replace(',',''))
            short_pos_noncommercials.append(total_short)
            spread = int(final[2].replace(',',''))
            spread_noncommercials.append(spread)

            # Commmercials
            total_long = int(final[3].replace(',',''))
            long_pos_commercials.append(total_long)
            total_short = int(final[4].replace(',',''))
            short_pos_commercials.append (total_short)

            # Non Reportables 
            total_long = int(final[7].replace(',',''))
            long_pos_nonrep.append(total_long)
            total_short = int(final[8].replace(',',''))
            short_pos_nonrep.append(total_short)




    df['Market_and_Exchange_Names'] = future_name
    df['CFTC_Contract_Market_Code'] = contracts_id
    df['Open_Interest_All'] = open_interest
    df['NonComm_Positions_Long_All'] = long_pos_noncommercials
    df['NonComm_Positions_Short_All'] = short_pos_noncommercials
    df['NonComm_Postions_Spread_All'] = spread_noncommercials
    df['Comm_Positions_Long_All'] = long_pos_commercials
    df['Comm_Positions_Short_All'] = short_pos_commercials
    df['NonRept_Positions_Long_All'] = long_pos_nonrep
    df['NonRept_Positions_Short_All'] = short_pos_nonrep


    print('Data successfully extracted')
    chrome.quit()
    print('Chrome closed')

    return df



def compute_cot_disaggregated():

    target_contracts = pd.read_excel('target_contracts.xlsx')

    ac_tff = ['EQUITIES', 'FIXED INCOME', 'CURRENCIES', 'CRYPTO CURRENCIES', 'COMMODITY INDEX']
    contracts_tff = []
    ac_disaggregated = ['ENERGY', 'PRECIOUS METALS', 'BASE METALS', 'SOFTS', 'GRAINS', 'LIVESTOCK']
    contracts_disaggregated = []
    
    df_cot_tff = pd.DataFrame()
    cot_dealers = []
    cot_asset_managers = []
    cot_leveraged_funds = []
    df_cot_disaggregated = pd.DataFrame()
    cot_producers = []
    cot_swap_dealers = []
    cot_managed_money = []
    
    for i in target_contracts['MARKET'].values:
        
        df = pd.read_excel('Disaggregated/Historical/'+i+'.xlsx')
        last_date = df['Date'].iloc[-1]
        df_histo = df[df['Date']>last_date-timedelta(days=740)].reset_index(drop=True)

        category = target_contracts[target_contracts['MARKET']==i]['CATEGORY NAME'].values[0]

        if category in ac_tff:

            contracts_tff.append(i)
            min = df_histo['Net - Dealers'].min()
            max = df_histo['Net - Dealers'].max()
            cot = round((df_histo['Net - Dealers'].iloc[-1]-min)/(max-min),2)*100
            cot_dealers.append(cot)
            min = df_histo['Net - Asset Managers'].min()
            max = df_histo['Net - Asset Managers'].max()
            cot = round((df_histo['Net - Asset Managers'].iloc[-1]-min)/(max-min),2)*100
            cot_asset_managers.append(cot)
            min = df_histo['Net - Leverage Funds'].min()
            max = df_histo['Net - Leverage Funds'].max()
            cot = round((df_histo['Net - Leverage Funds'].iloc[-1]-min)/(max-min),2)*100
            cot_leveraged_funds.append(cot)

        elif category in ac_disaggregated:

            contracts_disaggregated.append(i)
            min = df_histo['Net - PMPU'].min()
            max = df_histo['Net - PMPU'].max()
            cot = round((df_histo['Net - PMPU'].iloc[-1]-min)/(max-min),2)*100
            cot_producers.append(cot)
            min = df_histo['Net - Swap Dealers'].min()
            max = df_histo['Net - Swap Dealers'].max()
            cot = round((df_histo['Net - Swap Dealers'].iloc[-1]-min)/(max-min),2)*100
            cot_swap_dealers.append(cot)
            min = df_histo['Net - Managed Money'].min()
            max = df_histo['Net - Managed Money'].max()
            cot = round((df_histo['Net - Managed Money'].iloc[-1]-min)/(max-min),2)*100
            cot_managed_money.append(cot)

    df_cot_tff['Contract'] = contracts_tff
    df_cot_tff['COT Dealers'] = cot_dealers
    df_cot_tff['COT Asset Managers'] = cot_asset_managers
    df_cot_tff['COT Leveraged Funds'] = cot_leveraged_funds
    df_cot_disaggregated['Contract'] = contracts_disaggregated
    df_cot_disaggregated['COT Producers'] = cot_producers
    df_cot_disaggregated['COT Swap Dealers'] = cot_swap_dealers
    df_cot_disaggregated['COT Managed Money'] = cot_managed_money

    df_cot_disaggregated.to_excel('Results/COT_Index_Disaggregated.xlsx', index=False)
    df_cot_tff.to_excel('Results/COT_Index_TFF.xlsx', index=False)


    return [df_cot_tff, df_cot_disaggregated]


def update_databases(df, last_date, disclosure_type):

    contract_list = df['Market_and_Exchange_Names'].values

    dates = []
    for i in range(df.shape[0]):
        dates.append(datetime.strptime(last_date, '%Y-%m-%d'))
    df['Date'] = dates
    df.drop(['Asset Class', 'Asset Class ID'], axis=1, inplace=True)

    if disclosure_type == 'tff':

        df['Net - Dealers'] = df['Dealer_Positions_Long_All'] - df['Dealer_Positions_Short_All']
        df['Net - Asset Managers'] = df['Asset_Mgr_Positions_Long_All'] - df['Asset_Mgr_Positions_Short_All']
        df['Net - Leverage Funds'] = df['Lev_Money_Positions_Long_All'] - df['Lev_Money_Positions_Short_All']

    elif disclosure_type == 'disaggregated':

        df['Net - PMPU'] = df['Prod_Merc_Positions_Long_All'] - df['Prod_Merc_Positions_Short_All']
        df['Net - Swap Dealers'] = df['Swap_Positions_Long_All'] - df['Swap__Positions_Short_All']
        df['Net - Managed Money'] = df['M_Money_Positions_Long_All'] - df['M_Money_Positions_Short_All']

    elif disclosure_type == 'legacy':

        df['Net - NonCommercials'] = df['NonComm_Positions_Long_All'] - df['NonComm_Positions_Short_All']
        df['Net - Commercials'] = df['Comm_Positions_Long_All'] - df['Comm_Positions_Short_All']
        df['Net - NonReportables'] = df['NonRept_Positions_Long_All'] - df['NonRept_Positions_Short_All']

    for i in contract_list:

        print(i)
        if disclosure_type == 'tff' or disclosure_type == 'disaggregated':

            df_histo = pd.read_excel('Disaggregated/Historical/'+i+'.xlsx')
            df_histo = pd.concat([df_histo, df[df['Market_and_Exchange_Names'] == i]], ignore_index=True)
            df_histo.to_excel('Disaggregated/Historical/'+i+'.xlsx', index=False)

        elif disclosure_type == 'legacy':

            df_histo = pd.read_excel('Legacy/Historical/'+i+'.xlsx')
            df_histo = pd.concat([df_histo, df[df['Market_and_Exchange_Names'] == i]], ignore_index=True)
            df_histo.to_excel('Legacy/Historical/'+i+'.xlsx', index=False)

    
def compute_cot_legacy():

    target_contracts = pd.read_excel('target_contracts.xlsx')
    contracts = []
    
    df_cot_legacy = pd.DataFrame()
    cot_large_spec = []
    cot_commercials = []
    cot_small_spec = []

    for i in target_contracts['MARKET'].values:
        
        df = pd.read_excel('Legacy/Historical/'+i+'.xlsx')
        last_date = df['Date'].iloc[-5]
        df_histo = df[df['Date']>last_date-timedelta(days=740)].reset_index(drop=True)
        df_histo = df_histo.drop(df_histo.index[-4:])

        contracts.append(i)
        min = df_histo['Net - Commercials'].min()
        max = df_histo['Net - Commercials'].max()
        cot = round((df_histo['Net - Commercials'].iloc[-1]-min)/(max-min),2)*100
        cot_commercials.append(cot)
        min = df_histo['Net - NonCommercials'].min()
        max = df_histo['Net - NonCommercials'].max()
        cot = round((df_histo['Net - NonCommercials'].iloc[-1]-min)/(max-min),2)*100
        cot_large_spec.append(cot)
        min = df_histo['Net - NonReportables'].min()
        max = df_histo['Net - NonReportables'].max()
        cot = round((df_histo['Net - NonReportables'].iloc[-1]-min)/(max-min),2)*100
        cot_small_spec.append(cot)



    df_cot_legacy['Contract'] = contracts
    df_cot_legacy['COT Large Speculators'] = cot_large_spec
    df_cot_legacy['COT Commercials'] = cot_commercials
    df_cot_legacy['COT Small Speculators'] = cot_small_spec

    df_cot_legacy.to_excel('Results/COT_Index_Legacy.xlsx', index=False)


    return df_cot_legacy




securities = {
    'S&P 500':'SP500',
}



def get_price(ticker, start_date):
    global securities
     # Define the API endpoint and parameters
    api_url = "https://api.stlouisfed.org/fred/series/observations"
    api_key = "fab85be8c9e01cc886af340ce19bb2fa"  # Replace with your actual API key
    series_id = securities[ticker]  # Replace with the desired series ID
    observation_start = start_date
    file_type = "json"
    frequancy = "w"

    # Define the parameters for the request
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "observation_start":observation_start,
        "file_type": file_type,
        "frequency" : frequancy
    }

    # Make the GET request
    response = requests.get(api_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("Data retrieved successfully:", data)
    else:
        print(f"Failed to retrieve data: {response.status_code}, {response.text}")

    observations = data['observations']
    df=pd.DataFrame(observations)
    df.index = pd.to_datetime(df['date'])
    df.drop(columns=['realtime_start','realtime_end','date'],inplace=True)

    return df


def plot_net(start_date):

    target_contracts = pd.read_excel('target_contracts.xlsx')
    contracts = target_contracts['MARKET'].values

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    for i in contracts:
        print(i)
        df = pd.read_excel('Legacy/Historical/'+i+'.xlsx')
        df = df[df['Date']>=start_date].reset_index(drop=True)
        x = df['Date']
        y1 = df['Net - Commercials']/1000
        y2 = df['Net - NonCommercials']/1000
        y3 = df['Net - NonReportables']/1000
        fig, ax = plt.subplots(figsize=(7, 3), dpi=200)
        ax.bar(x, y1, color='b', width=4, label = 'Commercials')
        ax.bar(x, y2, color='r', width=4, label = 'Non Commercials')
        ax.bar(x, y3, color='y', width=4, label = 'Non Reportables')

        # fond noir
        ax.set_facecolor('k')
        fig.patch.set_facecolor('k')



        
        ax.set_xlim(start_date,)
        ax.tick_params(axis='y', color='w')
 
        ax.tick_params(axis='x', color='w')
        ax.spines['bottom'].set_color('w')
        ax.spines['left'].set_color('w')
        
        ax.set_ylabel('Net x 1000', color='w', fontsize=5)



        # Add a legend
       
        plt.xticks(color='w', fontsize=5)
        plt.yticks(color='w', fontsize=5)
        
  


        plt.show()