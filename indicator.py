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

# Bollinger Band(customize)
def bollinger_bands_customize(org, bb_df, window, num_std, min_width = 0):
    
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

# Bollinger Band
def bollinger_bands(data, window, num_std):
    
    """
    Parameters:
    org(dataframe): Close Data
    window (int): The period to calculate the moving average.
    num_std (int): The multiple of the standard deviation.
    """

    # Moving Average
    data['Middle Band'] = data['close'].rolling(window=window).mean().round(5)        # Rounding.
    
    # Standard Deviation
    data['Standard Deviation'] = data['close'].rolling(window=window).std(ddof=0).round(5) * num_std        # Rounding.

    # Upper Band & Lower Band
    data['Upper Band'] = data['Middle Band'] + data['Standard Deviation']
    data['Lower Band'] = data['Middle Band'] - data['Standard Deviation']

    # 원하는 return값 적기 
    return data['Lower Band']

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

# StopLoss(Test)
# stoploss_perc: perc사용 시 변수 사용 
def calculate_stoploss(data, period, atrmul): 

    '''
    Parameters:
    data(dataframe): dataframe
    period(int): rma length
    atrmul(int): ATR Multi
    stoploss_perc: stoploss percentage
    '''
    # StopLoss(ATR)
    data['high_low'] = data['high'] - data['low']
    data['high_close'] = data['high'] - data['close'].shift(1)
    data['high_close'] = np.abs(data['high_close'])
    data['low_close'] = data['low'] - data['close'].shift(1)
    data['low_close'] = np.abs(data['low_close'])

    true_range = data[['high_low', 'high_close', 'low_close']].max(axis = 1)

    # RMA 계산방식 
    # data['ATR'] = calculate_rma(true_range, period) 

    # SMA 계산방식
    data['ATR'] = true_range.rolling(window=period).mean().round(2)

    data['StopLoss_ATR'] = data['close'] - (data['ATR'] * atrmul)

    # StopLoss(perc)
    # data['perc'] = (data['close'] - (data['close'] * stoploss_perc / 100)).round(1)     # 반올림 조정

    # ATR과 Perc의 최대값 구하기 
    # data['Max StopLoss'] = (data[['stopLoss_ATR', 'perc']].max(axis = 1)).round(1)      # 반올림 조정

    return data['StopLoss_ATR'].round(2)

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

# RSI
def calculate_RSI(data, period=14):
    # 가격 변동을 계산
    delta = data['close'].diff()
    delta = delta[1:]

    # 상승분과 하락분을 분리
    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0).abs()
    
    # 평균 상승분과 평균 하락분을 계산
    avg_gain = gain.ewm(alpha=1 / period).mean()
    avg_loss = loss.ewm(alpha=1 / period).mean()

    # RS와 RSI를 계산
    rs = avg_gain / avg_loss
    rsi = round(100.0 - (100.0 / (1.0 + rs)), 2)
    return rsi

# Relative Volume
def relative_volume(data, length_volume = 13, thresh = 11):

    nzVolume = data['volume']
    volAvgL = nzVolume.rolling(window = length_volume * 5).mean()
    volRel = nzVolume / volAvgL
    volDev = (volAvgL + 1.618034 * volAvgL.rolling(window = length_volume * 5).std(ddof=0)) / volAvgL * thresh / 100
    
    return volRel * 0.145898 > volDev

# 장악형 캔들(Long 기준) + Relative Volume
def emgulfing_candle(data):

    high      = data['high']
    pre_high  = data['high'].shift(1)
    pre2_high = data['high'].shift(2)
    pre3_high = data['high'].shift(3)

    low       = data['low']
    pre_low   = data['low'].shift(1)

    open      = data['open']
    close     = data['close']

    emgulfing_candle = (high > pre_high) & (low < pre_low) & (open > close) & (pre_high > pre2_high) & (pre2_high > pre3_high) & relative_volume(data= data)

    return emgulfing_candle

