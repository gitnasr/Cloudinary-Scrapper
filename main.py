import os
import re
from datetime import datetime, timezone

import cloudinary
import cloudinary.api
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from tinydb import Query, TinyDB

load_dotenv(".env")


class CScrapper:
    def __init__(self) -> None:
        self.cloudName = os.getenv("CLOUD_NAME")
        self.scheduler = BlockingScheduler()
        try:
            self.cloud = cloudinary.config(
                cloud_name=self.cloudName,
                api_key=os.getenv("API_KEY"),
                api_secret=os.getenv("API_SECRET"),
            )
            self.all_resources = []
            self.next_run = {
                "last_cursor": None,
                "run_at": None,
                "page": 1
            }
            self.TinyDB = TinyDB("db.json")
        except KeyError as e:
            raise ValueError("Missing environment variable: {}".format(e))

    def extract_datetime(self, error_message):
        match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) UTC", error_message)
        if match:
            datetime_str = match.group(1)
            execution_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            return execution_time
        return None

    def schedule_next_run(self):
        if self.next_run["run_at"]:
            print(f"⏳ Rate limit exceeded. Retrying at {self.next_run['run_at']}...")
            self.scheduler.add_job(self.get_resources, 'date', run_date=self.next_run["run_at"])

    def get_resources(self, cursor=None, page=1):
        print("🔄 Fetching resources...")
        max_results = 50
        cursor = self.next_run["last_cursor"] or cursor
        page = self.next_run["page"] or page

        while True:
            try:
                resources = cloudinary.api.resources(max_results=max_results, next_cursor=cursor)
            except Exception as e:
                if "Rate Limit Exceeded" in str(e):
                    execution_time = self.extract_datetime(str(e))
                    if execution_time:
                        self.next_run["run_at"] = execution_time
                        self.next_run["last_cursor"] = cursor
                        self.next_run["page"] = page
                        self.schedule_next_run()
                    return  

            self.all_resources.extend(resources["resources"])
            cursor = resources.get("next_cursor")
            print(f"✅ Page {page} - {len(self.all_resources)} resources fetched")
            page += 1
            self.TinyDB.insert_multiple(resources["resources"])
            self.TinyDB.insert({"cursor": cursor, "page": page})
            if not cursor:
                break

        self.download_resource()

    def download_resource(self):
        print("📥 Downloading resources...")
        chunk_size = 1024
        download_path = os.path.join("downloads", self.cloudName)
        os.makedirs(download_path, exist_ok=True)

        for resource in self.all_resources:
            url = resource["secure_url"]
            file_path = os.path.join(download_path,self.cloudName, resource["folder"])
            os.makedirs(file_path, exist_ok=True)
            fileName = resource['asset_id'] + "." + resource['format']
            file_path = os.path.join(file_path, fileName)

            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size):
                        f.write(chunk)

                print(f"✅ Downloaded {fileName}")

            except Exception as e:
                print(f"❌ Failed to download {fileName} as {e}")
    def run(self):
        self.get_resources()
        self.scheduler.start()

if __name__ == "__main__":
    app = CScrapper()
    app.run()
