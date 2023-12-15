import qstock as qs

if __name__ == '__main__':
    df = qs.realtime_data('期货')
    print(df.head())

