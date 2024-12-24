# Python Scraper API

This project provides a Flask API to scrape search results from Google and Bing.


## **Disclaimer**

**This project is for educational purposes only.**

- **Google and Bing's Terms of Service prohibit scraping** their search results. If you wish to use their services in a legitimate and compliant manner, please use their official APIs instead.
- **Scraping at scale can result in your IP being banned**. Please use this project responsibly and limit the frequency of requests. If scraping in production, consider using **rotating IPs** or a **proxy service**.
- **I am not responsible for any consequences**, such as IP bans or legal actions, arising from the use of this scraper.


## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/python-scraper-api.git
    cd python-scraper-api
    ```

2. Create a `.env` file by copying the `.env.example` file and updating the values:
    ```sh
    cp .env.example .env
    ```

3. Build the Docker image:
    ```sh
    docker build -t python-scraper-api .
    ```

4. Run the Docker container:
    ```sh
    docker run -p 5000:5000 --env-file .env python-scraper-api
    ```

## API Endpoints

### Google Search

- **URL:** `/api/google_search`
- **Method:** `POST`
- **Headers:**
    - `x-api-key: your_api_key_here`
- **Body:**
    ```json
    {
        "query": "your search query"
    }
    ```

### Bing Search

- **URL:** `/api/bing_search`
- **Method:** `POST`
- **Headers:**
    - `x-api-key: your_api_key_here`
- **Body:**
    ```json
    {
        "query": "your search query"
    }
    ```

## Example Request

```sh
curl -X POST http://localhost:5000/api/google_search \
    -H "Content-Type: application/json" \
    -H "x-api-key: your_api_key_here" \
    -d '{"query": "example search"}'
```

