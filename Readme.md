# Instagram Data Scraper

This project is a Python-based solution for scraping and organizing data from Instagram using its GraphQL API.

The main goal was to collect user profile data and detailed post information from a list of selected public Instagram accounts.

---

##  Features

- Retrieves user profile information (e.g., follower count, biography, etc.)
- Extracts post-level data (e.g., like count, caption, timestamp)
- Handles Instagram API limitations with alternative methods
- Saves outputs into two clean CSV files for further analysis

---

##  Output Files

- `instagram_userdata.csv`: Contains cleaned user profile information.
- `instagram_records.csv`: Contains structured post-level data from each user.

---

##  Project Structure

```
.
├── main.py               # Main script to scrape user post data
├── scrape_user.py        # Script to scrape user profile data
├── instagram_records.csv # Output: post data
├── instagram_userdata.csv# Output: user data
├── README.md             # Project documentation
```

---

##  Overview of Scripts

### `main.py`
- Uses a predefined list of Instagram usernames.
- Extracts `user_id` from page source (`profile_id`) to send GraphQL requests.
- **Functions:**
    - `scrape_user_posts`: Fetches post data using Instagram's GraphQL API.
    - `cleaned_object`: Filters and structures the relevant fields from the response.
    - `write_csv_post`: Saves structured post data to `instagram_records.csv`.

### `scrape_user.py`
- Retrieves and processes public profile info.
- **Functions:**
    - `scrape_user`: Fetches raw user data from the API.
    - `write_csv_user`: Saves structured profile data to `instagram_userdata.csv`.

---

##  Challenges Faced

- **API Restrictions:** Instagram restricts direct access to some data (e.g., status code 302). This was overcome by inspecting webpage source code to manually extract user IDs.
- **Data Cleaning:** The API responses are verbose and noisy. Custom cleaning functions were developed to extract only relevant data for both posts and user profiles.

---

## Requirements

- Python 3.x

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/instagram-scraper.git
cd instagram-scraper
```

2. Modify the user list in `main.py` or `scrape_user.py` as needed.
3. Run the scripts:

```bash
python scrape_user.py
python main.py
```

---

## Disclaimer

This project is for **educational purposes only**. Be aware of Instagram’s [terms of use](https://help.instagram.com/581066165581870) when using scraping tools. Respect privacy and legality when accessing user data.

---

##  Author

**Ece**  
MSc in Artificial Intelligence  
Feel free to reach out for collaboration or feedback!

---

## Acknowledgements

- Inspired by public data projects and research in social media analysis
- API insights based on the open structure of Instagram’s web GraphQL
