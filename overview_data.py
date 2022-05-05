import pandas as pd

from util import get_data_from_API


def preprocess_overview_data(df):
    df['id'] = df['id'].astype('string')
    df['rank'] = df['rank'].astype('int')
    df['symbol'] = df['symbol'].astype('string')
    df['name'] = df['name'].astype('string')
    df['supply'] = df['supply'].astype('float')
    df['maxSupply'] = df['maxSupply'].astype('float')
    df['marketCapUsd'] = df['marketCapUsd'].astype('float')
    df['volumeUsd24Hr'] = df['volumeUsd24Hr'].astype('float')
    df['priceUsd'] = df['priceUsd'].astype('float')
    df['changePercent24Hr'] = df['changePercent24Hr'].astype('float')
    df['vwap24Hr'] = df['vwap24Hr'].astype('float')
    df['explorer'] = df['explorer'].astype('string')
    return df


def get_overview_data():
    data = pd.DataFrame(get_data_from_API(
        'https://api.coincap.io/v2/assets'))
    data = preprocess_overview_data(data)
    return data


def get_crypto_id_list():
    data = get_overview_data()
    return data['id'].unique()


def get_rank_list():
    data = get_overview_data()
    return data['rank'].unique()


def get_exchangeId_list(base_id, quote_id):
    url = 'https://api.coincap.io/v2/markets?' + \
        '&baseId=' + base_id + '&quoteId=' + quote_id
    data = get_data_from_API(url)
    exchangeIdList = []
    for item in data:
        exchangeIdList.append(item['exchangeId'])
    return exchangeIdList
