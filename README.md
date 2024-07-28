# Professor Ratings
A web scraping tool using Python and the Pyppeteer WebDriver to extract student reviews of specific professor from Rate My Professors to create one comprehensive review list with pros, cons, ratings, and etc.

## Features

- **Asynchronous Web Scraping**: Utilizes `pyppeteer` for efficient data extraction from dynamically loaded web pages.
- **Dynamic URL Building**: Builds URLs based on user input to scrape specific professor reviews.
- **Real-time Data Extraction**: Handles user sessions and data retrieval with `asyncio`.
- **Comprehensive Summaries**: Uses Google Generative AI to generate detailed summaries, including pros, cons, and ratings.

## Prerequisites

- `Python 3.x`
- `pyppeteer`
- `google-generativeai`
- `fake_useragent`
- `asyncio`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/rahulkodali/profRatings.git
    cd profRatings
    ```

2. Install the required Python packages:

    ```sh
    pip install -q -U google-generativeai
    pip install pyppeteer
    pip install asyncio
    pip install idk what else
    ```

3. Set up the API key in the config file:

    ```plaintext
    //set up key in google aistudio
    
    //in config file
    API_KEY=your_api_key_here
    ```


## Usage

1. Run the script:

    ```sh
    python rating.py
    ```

2. Enter the name of the professor when prompted.

3. The script will scrape reviews from Rate My Professors and generate a comprehensive summary.
