
import numpy as np
import pandas as pd

# Pivot_High(Dataframe 형태만 가능)
def calculate_pivot_high(df):
    """
    피봇 하이를 계산하는 함수
    df: DataFrame, 주식 데이터 (열: 'High')
    """
    df['Pivot_High'] = np.where(
        (df['high'] > df['high'].shift(1)) & 
        (df['high'] > df['high'].shift(-1)) & 
        (df['high'] > df['high'].shift(-2)) & 
        (df['high'] > df['high'].shift(-3)),
        df['high'], np.nan
    )
    return df

# Bollinger Band
def bollinger_bands(org, bb_df, window, num_std, min_width = 0):
    
    """
    Parameters:
    org(dataframe): Close Data
    window (int): The period to calculate the moving average.
    num_std (int): The multiple of the standard deviation.
    min_width(int): Minimum width.
    """

    # Moving Average
    bb_df['Middle Band'] = org['close'].rolling(window=window).mean().round(5)        # Rounding.
    
    # Standard Deviation
    bb_df['Standard Deviation'] = org['close'].rolling(window=window).std(ddof=0).round(5)        # Rounding.
    
    # Minimum width.
    bb_df['Value1'] = (bb_df['Standard Deviation'] * num_std).round(5)      # Rounding.
    bb_df['Value2'] = (bb_df['Middle Band'] * min_width / 100).round(5)     # Rounding.
    
    bb_df['Max Value'] = bb_df[['Value1','Value2']].max(axis = 1)

    # Upper Band & Lower Band
    bb_df['Upper Band'] = bb_df['Middle Band'] + bb_df['Max Value']
    bb_df['Lower Band'] = bb_df['Middle Band'] - bb_df['Max Value']

    return bb_df

# EMA
def calculate_ema(data, span):

    '''
    Parameters:
    data(dataframe): dataframe
    span(int): ema length
    '''
    return data.ewm(span=span, adjust=False).mean().round(1)        # 반올림 조정

# RMA
def calculate_rma(data, span):

    '''
    Parameters:
    data(dataframe): dataframe
    span(int): rma length
    '''
        
    return data.ewm(alpha=1/span, adjust=False).mean().round(1)     # 반올림 조정

# StopLoss
def calculate_stoploss(data, period, atrmul, stoploss_perc):

    '''
    Parameters:
    data(dataframe): dataframe
    period(int): rma length
    atrmul(int): ATR Multi
    stoploss_perc: stoploss percentage
    '''

    # StopLoss(ATR)
    high_low = data['high'] - data['low']
    high_close = (data['high'] - data['close'].shift(1)).abs()
    low_close = (data['low'] - data['close'].shift(1)).abs()

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    data['ATR'] = calculate_rma(true_range, period)

    data['stopLoss_ATR'] = data['close'] - (data['ATR'] * atrmul)

    # StopLoss(perc)
    data['perc'] = (data['close'] - (data['close'] * stoploss_perc / 100)).round(1)     # 반올림 조정

    # ATR과 Perc의 최대값 구하기 
    data['Max StopLoss'] = (data[['stopLoss_ATR', 'perc']].max(axis = 1)).round(1)      # 반올림 조정

    return data

# three_black_crows_candle(흑삼병)
def three_black_crows_candle(data):

    '''
    Parameters:
    data(dataframe): dataframe
    '''

    first_three_black_crows_candle  = data['open'].iloc[-4] > data['close'].iloc[-4]
    second_three_black_crows_candle = data['open'].iloc[-3] > data['close'].iloc[-3]
    thrid_three_black_crows_candle  = data['open'].iloc[-2] > data['close'].iloc[-2]

    three_black_crows_candle = first_three_black_crows_candle and second_three_black_crows_candle and thrid_three_black_crows_candle \
        and data['close'].iloc[-4] > data['close'].iloc[-3] and data['close'].iloc[-3] > data['close'].iloc[-2]
    
    return three_black_crows_candle

# invert_hammer(역망치)
def invert_hammer(data, wu_length = 2, ws_length = 2):

    '''
    Parameters:
    data(dataframe): dataframe
    wu_length(int): wick_upows_length, 기본값: 2
    ws_length(int): wick_slows_length, 기본값: 2
    '''

    body_siz = abs(data['open'].iloc[-2] - data['close'].iloc[-2])

    # 밑꼬리
    wick_slows = abs(data['low'].iloc[-2] - data['close'].iloc[-2])

    # 윗꼬리
    wick_upows = abs(data['high'].iloc[-2] - data['open'].iloc[-2])

    invert_hammer  = (wick_upows > body_siz * wu_length and wick_upows > wick_slows * ws_length) and data['high'].iloc[-2] >= data['high'].iloc[-3]

    return invert_hammer

