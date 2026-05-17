import os
import urllib.request

def download_hotel_data():
    if not os.path.exists('hotel_bookings.csv'):
        print("Downloading dataset...")
        url = "https://raw.githubusercontent.com/nicholasgasior/hotel-booking-demand/main/hotel_bookings.csv"
        urllib.request.urlretrieve(
            url,
            'hotel_bookings.csv'
        )
        print("Downloaded successfully!")
    else:
        print("Dataset already exists!")