import numpy as np

# PivotHigh 
# 출처(PivotHigh, PivotLow): https://toniteifly.tistory.com/65
def pivothigh(data, left:int, right:int):

    '''
    Pinescript ta.PivotHigh()와 동일
    '''

    data['pivothigh'] = 0

    for i in range(left + right, len(data), 1):

        # 범위내 최고점 계산
        mh = data['high'][i - right - left: i + 1].max()

        # Pivothigh - center의 고가와 범위내 최고점의 비교
        if data['high'].iat[i - right] == mh:
            data['pivothigh'].iat[i] = mh

        # 새로운 pivothigh가 출현하지 않을 경우 기존 변곡점 유지
        else:
            data['pivothigh'].iat[i] = data['pivothigh'].iat[i - 1]

    return data

# PivotLow
def pivotlow(data, left:int, right:int):
    
    '''
    Pinescript ta.PivotLow()와 동일
    '''

    data['pivotlow'] = 0

    for i in range(left + right, len(data), 1):

        # 범위내 최고 및 최저점 계산
        ml = data['low'][i - right - left: i + 1].min()

        # Pivotlow - center의 저가와 범위내 최저점의 비교
        if data['low'].iat[i - right] == ml:
            data['pivotlow'].iat[i] = ml

        # 새로운 pivotlow가 출현하지 않을 경우 기존 변곡점 유지
        else:
            data['pivotlow'].iat[i] = data['pivotlow'].iat[i - 1]

    return data

# Bollinger Band(customize)
def bollinger_band_customize(bb_df, window, num_std, round_num, min_width = 0):
    
    """
    Parameters
    org(dataframe): Close Data
    window (int)  : The period to calculate the moving average.
    num_std (int) : The multiple of the standard deviation.
    min_width(int): Minimum width.
    round_num(int) : Rounding.
    """

    # Moving Average
    bb_df['Middle Band'] = bb_df['close'].rolling(window=window).mean()
    bb_df['Middle Band'] = bb_df['Middle Band'].apply(lambda x: round(x , round_num))
    
    # Standard Deviation
    bb_df['Standard Deviation'] = bb_df['close'].rolling(window=window).std(ddof=0)
    bb_df['Standard Deviation'] = bb_df['Standard Deviation'].apply(lambda x: round(x , round_num))
    
    # Minimum width.
    bb_df['Value1'] = (bb_df['Standard Deviation'] * num_std)
    bb_df['Value1'] = bb_df['Value1'].apply(lambda x: round(x , round_num))

    bb_df['Value2'] = (bb_df['Middle Band'] * min_width / 100)
    bb_df['Value2'] = bb_df['Value2'].apply(lambda x: round(x , round_num))

    bb_df['Max Value'] = bb_df[['Value1','Value2']].max(axis = 1)

    # Upper Band & Lower Band
    bb_df['Upper Band'] = bb_df['Middle Band'] + bb_df['Max Value']
    bb_df['Lower Band'] = bb_df['Middle Band'] - bb_df['Max Value']

    return bb_df

# Bollinger Band
def bollinger_band(data, window:int, num_std:float, round_num:int):
    
    """
    Parameters:
    org(dataframe)  : Close Data
    window          : The period to calculate the moving average.
    num_std         : The multiple of the standard deviation.
    round_num       : round()
    """

    # Moving Average
    data['Middle_Band'] = data['close'].rolling(window=window).mean() # .round(5) 
    data['Middle_Band'] = data['Middle_Band'].apply(lambda x: round(x , round_num))

    # Standard Deviation
    data['Standard_Deviation'] = data['close'].rolling(window=window).std(ddof=0) * num_std # .round(2)
    data['Standard_Deviation'] = data['Standard_Deviation'].apply(lambda x: round(x , round_num))

    # Upper Band & Lower Band
    data['Upper_Band'] = data['Middle_Band'] + data['Standard_Deviation']
    data['Lower_Band'] = data['Middle_Band'] - data['Standard_Deviation']

    return data

# AD Line
def AD_Line(self, stock_code: str):

    '''
    지수 종목들 중 하락 종목 대비 상승 종목의 비율
    '''
    
    df = stock.get_market_ohlcv_by_date(self.start_date, self.end_date, stock_code)
    
    df['state'] = df.apply(lambda row: 'bullish' if row['시가'] < row['종가'] else ('bearish' if row['시가'] > row['종가'] else 'neutral'), axis=1)
    
    return df['state']
            
# SMA
def sma(data, length:int, round_num:int):

    '''
    data(dataframe) : data
    length          : sma length
    round_num       : round()
    '''

    data['SMA'] = data['close'].rolling(window=length).mean()
    data['SMA'] = data['SMA'].apply(lambda x: round(x , round_num))

    return data

# EMA
def ema(data, length: int, round_num):

    '''
    data(dataframe): dataframe
    length         : ema length
    round_num      : round()
    '''

    data['ema'] = data.ewm(span=length, adjust=False).mean().round(1)
    data['ema'] = data['ema'].apply(lambda x: round(x , round_num))

    return data

# RMA
def rma(data, length: int, round_num: int):

    '''
    Parameters:
    data(dataframe): dataframe
    length         : rma length
    round_num      : round()
    '''

    data['rma'] = data.ewm(alpha=1/length, adjust=False).mean()
    data['rma'] = data['rma'].apply(lambda x: round(x , round_num))
        
    return data

# HMA
def hma(df, period: int, round_num: int):
    
    '''
    df(dataframe) : dataframe
    period        : HMA Length
    round_num     : round()
    '''

    # Weighted Moving Average (WMA) 함수
    def WMA(series, period):
        weights = np.arange(1, period + 1)
        return series.rolling(period).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

    # HMA 계산 과정
    half_period = int(period / 2)
    sqrt_period = int(np.sqrt(period))

    # 중간 단계의 WMA 계산
    wma_half_period = WMA(df['close'], half_period)
    wma_full_period = WMA(df['close'], period)

    # 중간 단계의 값 계산
    hma_base = 2 * wma_half_period - wma_full_period

    # 최종 HMA 계산
    HMA = round(WMA(hma_base, sqrt_period), round_num)
    
    return HMA

# WMA
def wma(data, period: int, round_num: int):
    
    '''
    data(dataframe) : dataframe
    period          : WMA Length
    round_num       : round()
    '''
    series = data['close']

    weights = np.arange(1, period + 1)
    weighted_sum = np.convolve(series, weights[::-1], mode='valid')
    wma = weighted_sum / weights.sum()
    wma = np.round(wma, round_num)

    return np.concatenate([np.full(period - 1, np.nan), wma])

# vwma
def vwma(data, length:int, round_num:int):

    '''
    data(dataframe) : data
    length          : vwma length
    round_num       : round()
    '''
    data['vwv']= data['close'] * data['volume']
    data['vMA'] = data['vwv'].rolling(window=length).mean()

    data['vsma'] = data['거래량'].rolling(window=length).mean()

    data['vwma'] = data['vMA'] / data['vsma']
    data['vwma'] = data['vwma'].apply(lambda x: round(x , round_num))

    return data['vwma']

# StopLoss(Test)
# stoploss_perc: perc사용 시 변수 사용 
def atr(data, ma_period: int, round_num: int, ma_source): 

    '''
    data(dataframe): dataframe
    period         : ma length
    stoploss_perc  : stoploss percentage
    round_num      : round()
    '''
    def wma(series, period):
        weights = np.arange(1, period + 1)
        return series.rolling(period).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

    # StopLoss(ATR)
    data['high_low'] = data['high'] - data['low']
    data['high_close'] = data['high'] - data['close'].shift(1)
    data['high_close'] = np.abs(data['high_close'])
    data['low_close'] = data['low'] - data['close'].shift(1)
    data['low_close'] = np.abs(data['low_close'])

    true_range = data[['high_low', 'high_close', 'low_close']].max(axis = 1)

    # RMA 계산방식
    if ma_source == "rma":
        data['ATR'] = rma(true_range, ma_period, round_num) 

    # SMA 계산방식
    elif ma_source == "sma":
        data['ATR'] = true_range.rolling(window=ma_period).mean()
        data['ATR'] = data['ATR'].apply(lambda x: round(x , round_num))

    # WMA 계산방식 
    elif ma_source == "wma":
        data['ATR'] = wma(true_range, ma_period)
        data['ATR'] = data['ATR'].apply(lambda x: round(x , round_num))

    # StopLoss(perc)
    # data['perc'] = (data['close'] - (data['close'] * stoploss_perc / 100)).round(1)     # 반올림 조정
    
    # ATR과 Perc의 최대값 구하기 
    # data['Max StopLoss'] = (data[['stopLoss_ATR', 'perc']].max(axis = 1)).round(1)      # 반올림 조정

    return data['ATR']

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

# RSI
def rsi(data, round_num: int, period=14):
    
    '''
    data(dataframe) : dataframe
    period          : RSI Length
    round_num       : round()
    '''

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
    rsi = round(100.0 - (100.0 / (1.0 + rs)), round_num)
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

# invert_hammer(역망치)
def invert_hammer(data, wu_length = 2, ws_length = 2):

    '''
    Parameters:
    data(dataframe): dataframe
    wu_length(int) : wick_upows_length, 기본값: 2
    ws_length(int) : wick_slows_length, 기본값: 2
    '''

    body_siz = abs(data['open'].iloc[-2] - data['close'].iloc[-2])

    # 밑꼬리
    wick_slows = abs(data['low'].iloc[-2] - data['close'].iloc[-2])

    # 윗꼬리
    wick_upows = abs(data['high'].iloc[-2] - data['open'].iloc[-2])

    invert_hammer  = (wick_upows > body_siz * wu_length and wick_upows > wick_slows * ws_length) and data['high'].iloc[-2] >= data['high'].iloc[-3]

    return invert_hammer

# hammer(망치) + Relative Volume
def hammer_candle(data):
    body_size  = np.abs(data['open'] - data['close'])
    wick_slows = np.abs(data['low'] - data['close'])
    wick_upows = np.abs(data['high'] - data['open'])

    condition1 = wick_slows > body_size * 2
    condition2 = wick_upows * 2 < wick_slows
    condition3 = data['low'].shift(1) >= data['low']

    hammer = (condition1 & condition2) & condition3  & relative_volume(data= data)

    return hammer

