import csv
import json
import urllib.request

# URLs for the data
url_1 = (
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
)
url_2 = (
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
)


# Fetching data from URLs using urllib
def fetch_data(url):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data)


# Processing the data to create spot.csv
def create_spot_csv(data1, data2, file_name):
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["SpotTitle", "District", "Longitude", "Latitude", "ImageURL"])
        for spot in data1:
            spot_title = spot.get("stitle")
            for mrt in data2:
                if mrt["SERIAL_NO"] == spot.get("SERIAL_NO"):
                    district = [
                        district
                        for district in [
                            "中正區",
                            "萬華區",
                            "中山區",
                            "大同區",
                            "大安區",
                            "松山區",
                            "信義區",
                            "士林區",
                            "文山區",
                            "北投區",
                            "內湖區",
                            "南港區",
                        ]
                        if district in mrt.get("address", "")
                    ]
                    break
            longitude = spot.get("longitude")
            latitude = spot.get("latitude")
            image_url = spot.get("filelist", "").split("https://")
            image_url = "https://" + image_url[1] if len(image_url) > 1 else ""
            writer.writerow(
                [
                    spot_title,
                    district.pop() if len(district) > 0 else "",
                    longitude,
                    latitude,
                    image_url,
                ]
            )


# Processing the data to create mrt.csv
def create_mrt_csv(data1, data2, file_name):
    mrt_dict = {}
    for mrt in data2:
        mrt_station = mrt.get("MRT")
        if mrt_station:
            if mrt_station not in mrt_dict:
                mrt_dict[mrt_station] = []

            for spot in data1:
                if mrt["SERIAL_NO"] == spot["SERIAL_NO"]:
                    mrt_dict[mrt_station].append(spot.get("stitle"))

    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for station, titles in mrt_dict.items():
            writer.writerow([station] + titles)


# Main function to run the script
def main():
    data_1 = fetch_data(url_1)["data"]["results"]
    data_2 = fetch_data(url_2)["data"]
    # combined_data = data_1 + data_2

    create_spot_csv(data_1, data_2, "spot.csv")
    create_mrt_csv(data_1, data_2, "mrt.csv")


if __name__ == "__main__":
    main()
