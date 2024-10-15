
import re
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime, timedelta
import time
import os
import glob
import warnings


def filter_contracts(df):

    '''
    This function aims to keep only the most important futures contracts
    and to simplify the names of the contracts
    '''

    print('Keeping the most important futures contracts in progress ...')

    contracts_target = pd.read_excel('target_contracts.xlsx')
    
    contracts_to_keep = list(contracts_target['MARKET'])
    
    contracts_name_to_replace = {
        
        'UST 2Y NOTE':'2-YEAR NOTES',
        'UST 5Y NOTE':'5-YEAR NOTES',
        'UST 10Y NOTE':'10-YEAR NOTES',
        'E-MINI RUSSEL 1000 VALUE INDEX':'EMINI RUSSEL VALUE INDEX',
        'E-MINI S&amp;P CONSU STAPLES INDEX':'S&P CONSUMER STAPLES INDEX',
        'E-MINI S&amp;P ENERGY INDEX':'S&P ENERGY INDEX',
        'E-MINI S&amp;P FINANCIAL INDEX':'S&P FINANCIAL INDEX',
        'E-MINI S&amp;P HEALTH CARE INDEX':'S&P HEALTH CARE INDEX',
        'E-MINI S&amp;P UTILITIES INDEX': 'S&P UTILITIES INDEX',
        'E-MINI S&amp;P 400 STOCK INDEX': 'S&P 400 MID CAP',
        'S&amp;P 500 ANNUAL DIVIDEND INDEX' : 'S&P 500 ANNUAL DIVIDEND',
        'NZ DOLLAR':'NEW ZEALAND DOLLAR',
        'S&P 500 Consolidated':'S&P 500 CONSOLIDATED',
        'SO AFRICAN RAND':'SOUTH AFRICAN RAND',
        'ULTRA UST 10Y':'ULTRA 10-YEAR NOTES',
        'DOW JONES U.S. REAL ESTATE IDX':'DOW JONES U.S. REAL ESTATE',
        'MICRO E-MINI S&P 500 INDEX':'MICRO S&P 500',
        'UST BOND':'30-YEAR BONDS',
        'DJIA x $5':'DOW JONES',
        'RUSSELL E-MINI':'RUSSELL 2000',
        'NASDAQ-100 Consolidated':'NASDAQ-100 Consolidated',
        'NASDAQ MINI':'NASDAQ-100',
        'E-MINI S&amp;P 500':'S&P 500',
        'ETHER CASH SETTLED':'ETHEREUM',
        'BBG COMMODITY':'BBG COMMODITY INDEX',
        'MICRO ETHER':'MICRO ETHER',
        'ULTRA UST BOND':'ULTRA 30-YEAR BONDS',
        'CHEESE (CASH-SETTLED)': 'CHEESE',
        'BUTTER (CASH SETTLED)' : 'BUTTER',
        'COFFEE C' : 'COFFEE',
        'COPPER- #1':'COPPER',
        'COTTON NO. 2': 'COTTON',
        'WTI-PHYSICAL': 'CRUDE OIL',
        'BRENT LAST DAY' : 'BRENT CRUDE OIL',
        'MILK, Class III': 'DC MILK, Class III',
        'COCOA':'COCOA',
        'NY HARBOR ULSD':'HEATING OIL',
        ' LUMBER': 'LUMBER',
        'NAT GAS NYME':'NATURAL GAS',
        'FRZN CONCENTRATED ORANGE JUICE':'ORANGE JUICE',
        'STEEL-HRC':'STEEL',
        'SUGAR NO. 11':'SUGAR',
        'WHEAT ':'WHEAT-SRW',
        'VIX FUTURES':'VIX',
        'MSCI EAFE ':'MSCI EAFE'
    }
    
    # replace the good names for historic fils
    df['Market_and_Exchange_Names'] = df['Market_and_Exchange_Names'].replace(contracts_name_to_replace)

    # we keep only the contracts on which we are focusing
    df = df[df['Market_and_Exchange_Names'].isin(contracts_to_keep)]

    contract_type = []
    contract_rank = []
    for i in df['Market_and_Exchange_Names']:
        ct = str(contracts_target[contracts_target['MARKET']==i]['CATEGORY NAME'].values[0])
        rank = str(contracts_target[contracts_target['MARKET']==i]['CATEGORY RANK'].values[0])
        contract_type.append(ct)
        contract_rank.append(rank)

    df['Asset Class'] = contract_type
    df['Asset Class ID'] = contract_rank

    df = df.sort_values(by='Asset Class ID').reset_index(drop=True)

    return df





def compute_new_columns():

    target_contracts = pd.read_excel('target_contracts.xlsx')

    ac_tff = ['EQUITIES', 'FIXED INCOME', 'CURRENCIES', 'CRYPTO CURRENCIES', 'COMMODITY INDEX']
    contracts_tff = []
    as_disaggregated = ['ENERGY', 'PRECIOUS METALS', 'BASE METALS', 'SOFTS', 'GRAINS', 'LIVESTOCK']
    contracts_disaggregated = []
    
    df_cot_tff = pd.DataFrame()
    cot_dealers = []
    cot_asset_managers = []
    cot_leverage = []
    df_cot_disaggregated = pd.DataFrame()
    cot_producers = []
    cot_swap_dealers = []
    cot_managed_money = []
    
    for i in target_contracts['MARKET'].values:
        
        df = pd.read_excel('Disaggregated/Historical/'+i+'.xlsx')
        df.reset_index(drop=True, inplace = True)

        category = target_contracts[target_contracts['MARKET']==i]['CATEGORY NAME'].values[0]

        with pd.ExcelWriter('Disaggregated/Historical/'+i+'.xlsx', mode='a', engine='openpyxl') as writer:
            writer.book.remove(writer.book['Sheet1'])

            # if category in ac_tff:
            #     df['Net - Dealers'] = df['Dealer_Positions_Long_All'] - df['Dealer_Positions_Short_All']
            #     df['Net - Asset Managers'] = df['Asset_Mgr_Positions_Long_All'] - df['Asset_Mgr_Positions_Short_All']
            #     df['Net - Leverage Funds'] = df['Lev_Money_Positions_Long_All'] - df['Lev_Money_Positions_Short_All']

            if category in as_disaggregated:
                df['Net - PMPU'] = df['Prod_Merc_Positions_Long_All'] - df['Prod_Merc_Positions_Short_All']
                df['Net - Swap Dealers'] = df['Swap_Positions_Long_All'] - df['Swap__Positions_Short_All']
                df['Net - Managed Money'] = df['M_Money_Positions_Long_All'] - df['M_Money_Positions_Short_All']

            df.to_excel(writer, index=False)