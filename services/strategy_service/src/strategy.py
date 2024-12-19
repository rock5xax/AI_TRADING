def moving_average_strategy(data, short_window, long_window):
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    data['signal'] = 0
    data['signal'][short_window:] = np.where(
        data['short_ma'][short_window:] > data['long_ma'][short_window:], 1, 0
    )
    data['position'] = data['signal'].diff()
    return data
