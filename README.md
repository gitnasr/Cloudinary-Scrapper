# Cloudinary Scrapper
A Python utility for bulk downloading resources from your Cloudinary account. This tool allows you to fetch all resources from your Cloudinary storage and download them locally with progress tracking and rate limit handling.

## Features
- 🚀 Batch retrieval of Cloudinary resources
- 📥 Automatic downloading of resources to local storage
- 📊 Progress tracking for downloads
- 🔐 Secure authentication using environment variables
- 🔄 Pagination support for large resource collections
- ⏳ Smart rate limit handling with automatic retries
- 📅 Scheduled execution support

## Prerequisites
- Python 3.6 or higher
- Cloudinary account
- API credentials from Cloudinary

## Dependencies
```bash
pip install cloudinary python-dotenv requests apscheduler
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/cloudinary-scrapper.git
cd cloudinary-scrapper
```

2. Create a `.env` file in the project root with your Cloudinary credentials:
```env
CLOUD_NAME=your_cloud_name
API_KEY=your_api_key
API_SECRET=your_api_secret
```

## Usage
1. Configure your environment variables in `.env` file
2. Run the script:
```bash
python main.py
```

The script will:
- Connect to your Cloudinary account
- Fetch all available resources (50 per page)
- Handle rate limiting automatically with scheduled retries
- Download resources to a directory named after your cloud name under `downloads/`

## Code Structure
- `CScrapper`: Main class that handles all Cloudinary operations
  - `__init__`: Initializes the connection with Cloudinary and scheduler
  - `extract_datetime`: Parses rate limit reset times from error messages
  - `schedule_next_run`: Schedules the next execution after rate limit
  - `get_resources`: Fetches all resources from Cloudinary with pagination
  - `download_resource`: Downloads resources to local storage
  - `run`: Main execution method

## Rate Limiting
The script now includes sophisticated rate limit handling:
- Automatically detects rate limit errors
- Extracts the reset time from the error message
- Schedules the next execution for when the rate limit resets
- Maintains cursor position to resume from where it left off

## Error Handling
The script includes comprehensive error handling for:
- Missing environment variables
- API connection issues
- Rate limiting
- Download failures
- Resource access problems

## Logging
The script provides detailed logging information including:
- Download progress for each file
- Error messages for failed downloads
- Page fetching progress
- Rate limit notifications and scheduled retry times

## Storage Structure
Downloaded files are organized as follows:
```
downloads/
└── your_cloud_name/
    ├── resource1.jpg
    ├── resource2.jpg
    └── ...
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- [Cloudinary](https://cloudinary.com/) for their excellent API
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
- [requests](https://requests.readthedocs.io/) for HTTP handling
- [APScheduler](https://apscheduler.readthedocs.io/) for job scheduling

## Disclaimer
This tool is provided as-is. Please ensure you have the necessary permissions to download resources from your Cloudinary account. Be mindful of rate limits and storage quotas when using this tool.
