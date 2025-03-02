import pandas as pd

if __name__ == "__main__":
    # kiwi = pd.read_csv('./Kiwi-Scraper.csv')
    # kayak = pd.read_csv('./Kayak-Scraper.csv')
    # # # momondo = pd.read_csv('./Momondo-Scraper.csv')
    # kiwi.rename(columns={'arrive_hour': 'landing_hour', 'arrive_airport': 'landing_airport', 'return_arrive_hour': 'return_landing_hour', 'return_arrive_airport': 'return_landing_airport'}, inplace=True)
    # kayak.rename(columns={'return_arrive_hour': 'return_landing_hour', 'return_arrive_airport': 'return_landing_airport'}, inplace=True)
    # # print(kiwi.info())
    # # print(kiwi['ttt'].value_counts())
    # # print(kiwi['los'].value_counts())
    # # print(kiwi['origin_city'].value_counts())
    # # print(kiwi['destination_city'].value_counts())
    # # print(kiwi['snapshot_date'].value_counts())
    # # print(kayak.info())
    # # print(kayak['ttt'].value_counts())
    # # print(kayak['los'].value_counts())
    # # print(kayak['origin_city'].value_counts())
    # # print(kayak['destination_city'].value_counts())
    # # print(kayak['snapshot_date'].value_counts())
    # # 3. Explicitly select columns in the order you want
    # desired_columns = [
    #     'departure_hour', 'departure_airport', 'flight_length',
    #     'landing_hour', 'landing_airport', 'to_dest_company',
    #     'return_departure_hour', 'return_departure_airport', 'return_flight_length',
    #     'return_landing_hour', 'return_landing_airport', 'return_company',
    #     'price', 'is_direct', 'ttt', 'los', 'snapshot_date',
    #     'origin_city', 'destination_city', 'departure_date', 'return_date', 'website'
    # ]
    # kiwi['website'] = 'Kiwi'
    # kayak['website'] = 'Kayak'
    #
    # # Apply to both DataFrames and then concatenate
    # all_flights = pd.concat([kayak, kiwi], ignore_index=True)
    # all_flights.info()
    #
    # # kayak.rename({'landing_hour': 'arrive_hour', 'landing_airport': 'arrive_airport'})
    # # all_flights = pd.concat([kayak, kiwi], axis='rows',ignore_index=True)
    # # # kiwi.to_csv('Flights.csv', header=False, mode='a', index=False)
    # all_flights.to_csv('Flights.csv', index=False)
    flights = pd.read_csv('./Flights.csv')
    print(flights.info())
    print(flights['ttt'].value_counts())
    print(flights['los'].value_counts())
    print(flights['origin_city'].value_counts())
    print(flights['destination_city'].value_counts())
    print(flights['snapshot_date'].value_counts())
    print(flights['website'].value_counts())

