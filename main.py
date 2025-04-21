"""
     @Author: Ece Akinci
     @Date: 05/01/2025
"""

import json
import httpx
import csv
from urllib.parse import quote

BASE_URL = "https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables="

with open('userid.json', 'r') as f:
    USER_IDS = json.load(f)


# Writes a list of Instagram post data to a CSV file.
# Args: post (list): List of dictionaries containing Instagram post details.
def write_csv_post(post):
    with open('instagram_records.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['postid', 'userid', 'username', 'src', 'views', 'likes', 'type', 'tagged_users', 'captions', 'comments_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerows(post)


# Retrieves specific data from a nested dictionary structure in an Instagram post.
# Returns: Any: Extracted data or None if not available.
def get_edge(obj, val1, val2, val3):
    tagged_users = None
    tagged_user_data = obj.get(val1, {})
    edges = tagged_user_data.get('edges', [])

    if isinstance(edges, list) and len(edges) > 0:
        first_edge = edges[0]  # Safely access the first edge
        tagged_users = first_edge.get('node', {}).get(val2)
        if val3 != '':
            tagged_users = tagged_users.get(val3)

    return tagged_users


# Cleans and transforms raw Instagram post data into a structured format.
def cleaned_object(post):
    post = post['node']

    cleaned_post = {'postid': post['id'], 'userid': post['owner']['id'], 'username': post['owner']['username'],
                    'src': post['display_url'],
                    'views': post['video_view_count'] if 'video_view_count' in post else 0,
                    'likes': post['edge_media_preview_like']['count'],
                    'type': post['__typename'],
                    'tagged_users': get_edge(post, 'edge_media_to_tagged_user', 'user', 'username'),
                    'captions': get_edge(post, 'edge_media_to_caption', 'text', ''),
                    'comments_count': post['edge_media_to_comment']['count'],
                    }
    return cleaned_post


# Scrapes posts of a given Instagram user using Instagram's GraphQL API.
def scrape_user_posts(user_id: str, session: httpx.Client, page_size=12, max_pages: int = None):
    base_url = BASE_URL
    variables = {"id": user_id, "first": page_size, "after": None}
    _page_number = 1
    new_posts = []

    while True:
        resp = session.get(base_url + quote(json.dumps(variables)))
        data = resp.json()

        if resp.status_code == 200:
            posts = data["data"]["user"]["edge_owner_to_timeline_media"]
        else:
            print(resp.status_code, resp.text)
            break
        for post in posts["edges"]:
            new_posts.append(cleaned_object(post))  # Add cleaned post to the list
        page_info = posts["page_info"]
        if _page_number == 1:
            print(f"scraping total {posts['count']} posts of {user_id}")
        else:
            print(f"scraping page {_page_number}")
        if not page_info["has_next_page"]:
            break
        if variables["after"] == page_info["end_cursor"]:
            break
        variables["after"] = page_info["end_cursor"]
        _page_number += 1
        if max_pages and _page_number > max_pages:
            break
    return new_posts


if __name__ == "__main__":
    all_posts = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }

    with httpx.Client(headers=headers, timeout=httpx.Timeout(40.0)) as session:
        for userid in USER_IDS:
            posts = list(scrape_user_posts(userid, session, max_pages=4))
            all_posts.extend(posts)
    write_csv_post(all_posts)
