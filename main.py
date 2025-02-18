
import os

import cloudinary
import cloudinary.api
import requests
from dotenv import load_dotenv

load_dotenv(".env")

class CScrapper:
    def __init__(self) -> None:
        self.cloudName = os.getenv("CLOUD_NAME")
        try:
            self.cloud = cloudinary.config(
                cloud_name=self.cloudName,
                api_key=os.getenv("API_KEY"),
                api_secret=os.getenv("API_SECRET"),
            )
            self.all_resources = []  # Store resources with metadata
        except KeyError as e:
            raise ValueError("Missing environment variable: {}".format(e))

    def get_resources(self):
        print("Fetching resources...")
        max_results = 50  # Adjust as needed
        cursor = None
        page =1
        while True:
            try:
                resources = cloudinary.api.resources(max_results=max_results, next_cursor=cursor)
            except Exception as e:
                print("Error fetching resources:", e)
                break

            for resource in resources["resources"]:
                self.all_resources.append(resource)

            cursor = resources.get("next_cursor")
            print(f"Page {page} - {len(self.all_resources)} resources fetched")
            page += 1
            if not cursor:
                break


        self.direct_urls = {resource["public_id"]: resource["secure_url"] for resource in self.all_resources}
    
    def download_resource(self):
        chunk_size = 1024
        for publicId in self.direct_urls:

            try:
                response = requests.get(self.direct_urls[publicId], stream=True)
                response.raise_for_status()

                file_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                dir_path = os.path.join("downloads", os.path.dirname(self.cloudName), publicId)
                os.makedirs(os.path.dirname(dir_path), exist_ok=True)
                with open(dir_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size):
                        downloaded += len(chunk)
                        f.write(chunk)
                        print(f"Downloading {publicId} ({downloaded}/{file_size} bytes)")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading {publicId}: {e}")


        
if __name__ == "__main__":
    app = CScrapper()
    app.get_resources()
    app.download_resource()