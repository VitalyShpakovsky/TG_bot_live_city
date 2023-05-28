from settings import BotAPISettings
import requests
import json


token = BotAPISettings()
url = "https://cost-of-living-and-prices.p.rapidapi.com/cities"
headers = {"X-RapidAPI-Key": token.api_key.get_secret_value(),
           "X-RapidAPI-Host": token.api_host.get_secret_value()}
response = requests.get(url, headers=headers)
data = json.loads(response.text)
name_data = 'diploma.db'


def func_info_city(country: str, city: str) -> str:  # функция получения информации о передаваемом городе
    url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"
    querystring = {"city_name": city, "country_name": country.title()}
    headers = {
        "X-RapidAPI-Key": token.api_key.get_secret_value(),
        "X-RapidAPI-Host": token.api_host.get_secret_value()}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    price_bedroom = 'Нет данных'
    price_apartment = 'Нет данных'
    price_taxi = 'Нет данных'
    price_apartment_center = 'Нет данных'
    price_utilities = 'Нет данных'
    price_internet = 'Нет данных'
    for i_key in data['prices']:
        if i_key['item_name'] == "Price per square meter to Buy Apartment Outside of City Center":
            price_apartment = i_key['usd']['avg']
        if i_key['item_name'] == "Price per square meter to Buy Apartment in City Center":
            price_apartment_center = i_key['usd']['avg']
        if i_key['item_name'] == "Basic utilities for 85 square meter Apartment including Electricity, " \
                                 "Heating or Cooling, Water and Garbage":
            price_utilities = i_key['usd']['avg']
        if i_key['item_name'] == "Internet, 60 Mbps or More, Unlimited Data, Cable/ADSL":
            price_internet = i_key['usd']['avg']
        if i_key['item_name'] == "One bedroom apartment in city centre":
            price_bedroom = i_key['usd']['avg']
        if i_key['item_name'] == "Taxi, price for 1 km, Normal Tariff":
            price_taxi = i_key['usd']['avg']
    answer = f'Средняя стоимость 1 кв. метра жилья вне центра города $ {price_apartment}\n'\
             f'Средняя стоимость 1 кв. метра жилья в центре города $ {price_apartment_center}\n'\
             f'Стоимость коммунальных услуг квартиры 85 кв. метров $ {price_utilities}\n'\
             f'Стоимость интернета в месяц $ {price_internet}\n'\
             f'Средняя стоимость аренды однокомнатной квартиры $ {price_bedroom}\n'\
             f'Средняя стоимость 1 км поездки на такси ${price_taxi}'
    return answer


def func_weather_city(city: str) -> str:  # функция получения погоды о передаваемом городе
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": city, "days": "1"}
    headers = {
        "X-RapidAPI-Key": token.api_key.get_secret_value(),
        "X-RapidAPI-Host": token.api_host_weather.get_secret_value()}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    answer = f"Температура: {data['current']['temp_c']}°C\nВлажность: {data['current']['humidity']} %\n"\
             f"Давление: {data['current']['pressure_mb']} mbar."
    return answer