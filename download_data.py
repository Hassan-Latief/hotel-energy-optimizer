import os
import urllib.request
import requests

def download_hotel_data():
    if not os.path.exists('hotel_bookings.csv'):
        print("Downloading dataset...")
        
        urls = [
            "https://raw.githubusercontent.com/nicholasgasior/hotel-booking-demand/main/hotel_bookings.csv",
            "https://raw.githubusercontent.com/dsrscientist/dataset1/master/hotel_bookings.csv",
            "https://raw.githubusercontent.com/nickg24/datasets/main/hotel_bookings.csv",
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv"
        ]
        
        for url in urls:
            try:
                print(f"Trying: {url}")
                response = requests.get(
                    url, timeout=30
                )
                if response.status_code == 200:
                    with open(
                        'hotel_bookings.csv', 'wb'
                    ) as f:
                        f.write(response.content)
                    print("Downloaded successfully!")
                    return
            except Exception as e:
                print(f"Failed: {e}")
                continue
                
        print("All downloads failed!")
    else:
        print("Dataset already exists!")
