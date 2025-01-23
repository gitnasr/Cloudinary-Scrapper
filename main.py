
import cloudinary,os, requests, logging
from dotenv import load_dotenv
import cloudinary.api

class CScrapper:
    def __init__(self) -> None:
        load_dotenv()
        try:
            self.cloud = cloudinary.config(
                cloud_name=os.getenv("CLOUD_NAME"),
                api_key=os.getenv("API_KEY"),
                api_secret=os.getenv("API_SECRET"),
            )
            self.all_resources = []  # Store resources with metadata
        except KeyError as e:
            raise ValueError("Missing environment variable: {}".format(e))

    def get_resources(self):
        print("Getting resources")
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
            print(f"Page {page} fetched")
            page += 1
            if not cursor:
                break

        # Example of storing URLs in a dictionary
        self.direct_urls = {resource["public_id"]: resource["secure_url"] for resource in self.all_resources}
    
    def download_resource(self):
        chunk_size = 1024
        for publicId in self.direct_urls:

            try:
                response = requests.get(self.direct_urls[publicId], stream=True)
                response.raise_for_status()

                file_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0

                with open(os.path.join("C1Test",publicId ), 'wb') as f:
                    for chunk in response.iter_content(chunk_size):
                        downloaded += len(chunk)
                        f.write(chunk)
                        logging.info(f"Downloading {publicId} ({downloaded}/{file_size} bytes)")

            except requests.exceptions.RequestException as e:
                # print(e)
                logging.error(f"Error downloading {publicId}: {e}")
            # logging.error(f"Error downloading {url}: {e}")


        
if __name__ == "__main__":
    app = CScrapper()
    app.get_resources()
    app.download_resource()