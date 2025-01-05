import json
import httpx
import csv

USERNAME_LIST = ['cristiano', 'whoop', 'globesoccer', 'saudi2034', 'mrbeast', 'leomessi',  'adidasfootball', 'fortnite',
                  'stanley_brand', 'neymarjr', 'kyliecosmetics', 'kyliejenner', 'khy', 'therock', 'target', 'kimkardashian',
                  'selenagomez', 'arianagrande', 'wmag', 'variety', 'taylorswift', 'voguemexico', 'beyonce', 'justinbieber',
                  'zoesugg', 'kourtneykardash', 'khloekardashian', 'emmachamberlain', 'itsmarziapie', 'pewdiepie',
                  'nikkietutorials', 'nimya', 'jeffreestar', 'jeffreestarcosmetics', 'jamescharles', 'dantdm', 'youtooz',
                  'loganpaul', 'lunchly', 'fcbarcelona', 'juventus', 'drinkprime', 'jakepaul', 'mostvaluablepromotions',
                  'netflix', 'miketyson', 'kevikodra', 'juttaleerdam', 'bretmanrock', 'lelepons', 'hudabeauty', 'zachking',
                  'willsmith', 'observatorynorthpark', 'spotifypodcasts', 'primevideo', 'youtube', 'cloakbrand',
                  'milliebobbybrown', 'apocalypto_12', 'markiplier', 'lizakoshy', 'aboutyou', 'toryburch', 'ddlovato',
                  'graziausa_', 'snoopdogg', 'forstonerzonlyradio', 'harpersbazaarus', 'mileycyrus', 'tanamongeau',
                  'jeff', 'caseyneistat', 'andrewschulz','jessicaalba', 'chrishemsworth', 'wildstateprod', 'elcorteingles',
                  'gigihadid', 'katyperry', 'itv', 'tomholland2013', 'berobrewing', 'foodandwine', 'officialtommyfleetwood',
                  'shawnmendes', 'interviewmag', 'johnlegend', 'yutsai88', 'billboard', 'qvc', 'nbcthevoice', 'kismet',
                  'abc', 'jenniferhudsonshow', 'davetozer', 'ladygaga', 'khloekardashian', 'bustle', 'aliciakeys',
                  'kingjames', 'lakers', 'nike', 'uninterrupted', 'ohiostatefb', 'kevinhart4real', 'usainbolt', 'eurosport',
                  'digiceljamaica', 'manchesterunited', 'britishgq', 'worldathletics', 'highperformance', 'serenawilliams',
                  'essence', 'barackobama', 'thepivot', 'vicblends', 'kamalaharris']


client = httpx.Client(
    headers = {
        "x-ig-app-id": "936619743392459",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)


def write_csv_user(user):
    with open('insta_userdata.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'username', 'fullname', 'biography', 'followerCount', 'category', 'isVerified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(user)


def scrape_user(username: str):
    result = client.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
    )

    if result.status_code != 200:
        raise ValueError(f"Error: Received status code {result.status_code}. Response: {result.text}")

    data = json.loads(result.content)
    data = data["data"]["user"]
    clean_user_data = [{
         'id': data['id'],
         'username': data['username'],
         'fullname': data['full_name'],
         'biography': data['biography'],
         'followerCount': data['edge_followed_by']['count'],
         'category': data['category_enum'],
         'isVerified': data['is_verified']
    }]
    return clean_user_data


if __name__ == "__main__":
    all_users = []
    for user_name in USERNAME_LIST:
        user = list(scrape_user(user_name))
        all_users.extend(user)
    write_csv_user(all_users)
