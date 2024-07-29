import json
import math
import os
import time
import datetime
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from pytube import YouTube


now = datetime.datetime.now()

#formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
#filename = f"youtubedata_{formatted_datetime}.json"
app = Flask(__name__)
CORS(app)

API_key = "AIzaSyC83Ao_dUHSygFDzjVEoPWsK5aGfeUraoc"
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.start()



def download_data(API_KEY: str, ChannelID: str, filename: str):
  news_data=[]
  nextpagetoken=""
  record_count = 0
  while True:
      if nextpagetoken:
          news_url1 = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={ChannelID}&part=snippet,id&order=date&pageToken={nextpagetoken}&maxResults=50"
      else:
          news_url1 = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={ChannelID}&part=snippet,id&order=date&maxResults=50"

      try:
        print(filename)
        news_response_all = requests.get(news_url1).json()
        news_data=news_data+news_response_all.get("items",[])
        if news_response_all.get("nextPageToken",""):
            nextpagetoken = news_response_all.get("nextPageToken","")
        else:
            break
      except Exception as e:
        print(f"Error: {e}")
        break

      # Emergency Break
      try:
        record_count = record_count + news_response_all.get("pageInfo", {}).get("resultsPerPage", 0)
        total_records = news_response_all.get("pageInfo", {}).get("totalResults", 0)
        if total_records == record_count:
          break
      except Exception as e:
        print(f"Error: {e}")
      break


  checked_items=[]
  news_items=[]
  for item in news_data:
        item_id=item.get("id",{}).get("videoId",None)
      #if item_id not in checked_items:
        video_url= f"https://www.youtube.com/watch?v={item_id}"

        try:
          yt = YouTube(video_url)
          checked_items.append(item_id)
          if yt.length > 60:
              news_items.append(item)
        except Exception as e:
          print(f"Error: {e}")
  print(news_items)

  filename = str(os.path.join(filename))
  if news_items:
    with open(filename, "w") as f:
        json.dump(news_items, f, indent=4)


  # if checked_items:
  #   temp_dirname = os.path.dirname(filename)
  #   temp_filename = os.path.basename(filename)
  #   temp_filename = temp_filename.replace(".json", "_bck.json")
  #
  #   checked_filename_path = str(os.path.join(temp_dirname, temp_filename))
  #
  #   with open(checked_filename_path, "w") as f:
  #       json.dump(checked_items, f, indent=4)
  print("completed")
  return True

def fetch_data1():
    entertainmentChannelID = "UChVmpG7svTIbwlA1Ie4BfKA"
    newsroomChannelID = "UCCxo9eb6HtHdxm4AWw1-kYg"
    lifestyleChannelID = "UC_b8pP0DSHzofuJxtp5PAKg"

    # download_data(API_key, newsroomChannelID,"news.json")
    # download_data(API_key, entertainmentChannelID, "entertainment.json")
    download_data(API_key, lifestyleChannelID, "lifestyle.json")

#fetch_data1()





#     try:
#         url = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={entertainmentChannelID}&part=snippet,id&order=date&maxResults=1"
#
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         maxresult = data["pageInfo"]["totalResults"]
#
#         url1 = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={entertainmentChannelID}&part=snippet,id&order=date&maxResults={maxresult}"
#         maxresult_response = requests.get(url1)
#
#
#
#         with open("entertainment.json", "w") as f:
#             json.dump(maxresult_response.json(), f, indent=4)
#         #
#         # news_url = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={newsroomChannelID}&part=snippet,id&order=date&maxResults=1"
#         #
#         #news_response = requests.get(news_url)
#         # news_response.raise_for_status()
#
#         # data = news_response.json()
#         # news_maxresult=data["nextPageToken"]
#
#         news_data=[]
#         nextpagetoken=""
#         while True:
#             if nextpagetoken !="":
#                 news_url1 = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={newsroomChannelID}&part=snippet,id&order=date&pageToken={nextpagetoken}"
#                 news_response_all = requests.get(news_url1).json()
#                 news_data.append(news_response_all["items"])
#                 if news_response_all.get("nextPageToken",False):
#                    nextpagetoken = news_response_all["nextPageToken"]
#                 else:
#                     break
#             else:
#                 news_url1 = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={newsroomChannelID}&part=snippet,id&order=date"
#                 news_response_all = requests.get(news_url1).json()
#                 news_data.append(news_response_all["items"])
#
#                 if news_response_all.get("nextPageToken",False):
#                    nextpagetoken = news_response_all["nextPageToken"]
#                 else:
#                     break
#
#
#         news_data = news_response_all.json()
#         news_items=[]
#         for item in news_data["items"]:
#             video_duration = f"https://www.youtube.com/watch?v={item['id'].get('videoId', ' ')}"
#             yt = YouTube(video_duration)
#             video_length = yt.length
#             if video_length > 60:
#                 news_items.append(item)
#         with open("news.json", "w") as f:
#             json.dump(news_items, f, indent=4)
#
#         with open("news.json", "w") as f:
#             json.dump(news_response_all.json(), f, indent=4)
#
#         lifestyle_url = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={lifestyleChannelID}&part=snippet,id&order=date&maxResults=1"
#
#         lifestyle_response = requests.get(lifestyle_url)
#         lifestyle_response.raise_for_status()
#         data = lifestyle_response.json()
#         lifestyle_maxresult = data["pageInfo"]["totalResults"]
#         lifestyle_url1 = f"https://www.googleapis.com/youtube/v3/search?key={API_key}&channelId={newsroomChannelID}&part=snippet,id&order=date&maxResults={lifestyle_maxresult}"
#         lifestyle_response_all = requests.get(lifestyle_url1)
#
#         with open("lifestyle.json", "w") as f:
#             json.dump(lifestyle_response_all.json(), f, indent=4)
#     except Exception as e:
#         print(e)
#
#     print("saved data sucessfully")

#fetch_data1()

scheduler.add_job(fetch_data1, 'interval',  hours=4, id='fetch_data1', replace_existing=True)
@app.route('/connectOriginals', methods=['GET'])
def fetch_data():
    with open("entertainment.json", "r") as f:
        entertainment = json.load(f)
    with open("news.json", "r") as f:
        news = json.load(f)
    with open("lifestyle.json", "r") as f:
        lifestyle = json.load(f)

    # Debugging: print the news data to ensure it's being read correctly
    print(news)

    formatted_data = {}

    entertainment_data = []
    for item in entertainment:
        print(item)
        print()
    # return jsonify(entertainment)
        video_id = item["id"]["videoId"]
        resp = {
            "video_id": video_id,
            "id": video_id,
            "title": item["snippet"].get("title", ""),
            "description": item["snippet"].get("description", ""),
            "image": item["snippet"]["thumbnails"].get("high", {}).get("url", ""),
            "postDate": item["snippet"].get("publishedAt", ""),
            "youtubeLink": f"https://www.youtube.com/watch?v={video_id}",
            "soundcloudLink": None,
            "duration": None,
            "language": "English",
            "file": None,
            "slug": item["snippet"].get("title", ""),
        }
        entertainment_data.append(resp)

    # Process News Data
    news_data = []
    for item in news:
        print(item)
        video_id = item["id"]["videoId"]
        resp = {
            "video_id": video_id,
            "id": video_id,
            "title": item["snippet"].get("title", ""),
            "description": item["snippet"].get("description", ""),
            "image": item["snippet"]["thumbnails"].get("high", {}).get("url", ""),
            "postDate": item["snippet"].get("publishedAt", ""),
            "youtubeLink": f"https://www.youtube.com/watch?v={video_id}",
            "soundcloudLink": None,
            "duration": None,
            "language": "English",
            "file": None,
            "slug": item["snippet"].get("title", ""),
        }
        news_data.append(resp)


    # Process Lifestyle Data
    lifestyle_data = []
    for item in lifestyle:
        print(item)
        video_id = item["id"]["videoId"]
        resp = {
            "video_id": video_id,
            "id": video_id,
            "title": item["snippet"].get("title", ""),
            "description": item["snippet"].get("description", ""),
            "image": item["snippet"]["thumbnails"].get("high", {}).get("url", ""),
            "postDate": item["snippet"].get("publishedAt", ""),
            "youtubeLink": f"https://www.youtube.com/watch?v={video_id}",
            "soundcloudLink": None,
            "duration": None,
            "language": "English",
            "file": None,
            "slug": item["snippet"].get("title", ""),
        }
        lifestyle_data.append(resp)
    lifestyle_data= list({v['youtubeLink']: v for v in lifestyle_data}.values())
    entertainment_data=list({v['youtubeLink']: v for v in entertainment_data}.values())
    news_data=list({v['youtubeLink']: v for v in news_data}.values())

    formatted_data = {
        "connect-artist-interview": [],
        "connect-dil-se": [],
        "connect-sheesha": [],
        "entertainment": entertainment_data[:10],
        "explainers": [],
        "lifestyle": lifestyle_data[:10],
        "news-room": news_data[:10],
        "shows": [],
        "meta": {
            "title": "Connect Originals",
            "showAll": "true",
            "heading": None,
            "subHeading": None,
            "backgroundHeading": None,
            "backgroundImage": None,
            "itemsTitle": None,
            "items": [],
            "types": [
                {
                    "id": 343521,
                    "slug": "news-room",
                    "title": "News Room"
                },
                {
                    "id": 344304,
                    "slug": "entertainment",
                    "title": "Connect Cine"
                },
                {
                    "id": 344305,
                    "slug": "lifestyle",
                    "title": "Lifestyle"
                }
            ]
        }
    }

    return jsonify(formatted_data)



@app.route('/connectOriginals/news-room', methods=['GET'])
def fetch_news():
    records_per_page = 5
    page = int(request.args.get('page', 1))

    start_index = (page - 1) * records_per_page
    end_index = page * records_per_page

    try:
        with open("news.json", "r") as f:
            data = json.loads(f.read())


        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format"}), 500

        total_videos = len(data)
        total_pages = math.ceil(total_videos / records_per_page)

        resp_data = []
        for item in data:

            resp = {
                "video_id": item["id"].get("videoId", " "),
                "id": item["id"].get("videoId", " "),
                "title": item["snippet"].get("title", " "),
                "description": item["snippet"].get("description", " "),
                "image": item["snippet"]["thumbnails"].get("high", {}).get("url", " "),
                "postDate": item["snippet"].get("publishedAt", " "),
                "youtubeLink": f"https://www.youtube.com/watch?v={item['id'].get('videoId', ' ')}",
                "soundcloudLink": None,
                "duration": None,
                "language": "English",
                "file": None,
                "slug": item["snippet"].get("title", " "),
            }
            resp_data.append(resp)

        # Paginate data
        #paginated_data = resp_data[start_index:end_index]
        formatted_data = {
            "data": resp_data,
            "meta": {
                "title": "Connect Originals",
                "heading": None,
                "subHeading": None,
                "backgroundHeading": None,
                "backgroundImage": None,
                "itemsTitle": None,
                "items": [],
                "pagination": {
                    "total": total_videos,
                    "count": len(resp_data),
                    "per_page": records_per_page,
                    "current_page": page,
                    "total_pages": total_pages,
                    "links": {

                    }
                }
            }
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(formatted_data)


@app.route('/connectOriginals/entertainment', methods=['GET'])
def fetch_entertainment():
    records_per_page = 5
    page = int(request.args.get('page', 1))

    start_index = (page - 1) * records_per_page
    end_index = page * records_per_page

    try:
        with open("entertainment.json", "r") as f:
            data = json.loads(f.read())

        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format"}), 500

        total_videos = len(data)
        total_pages = math.ceil(total_videos / records_per_page)

        resp_data = []
        for item in data:
            resp = {
                "video_id": item["id"].get("videoId", " "),
                "id": item["id"].get("videoId", " "),
                "title": item["snippet"].get("title", " "),
                "description": item["snippet"].get("description", " "),
                "image": item["snippet"]["thumbnails"].get("high", {}).get("url", " "),
                "postDate": item["snippet"].get("publishedAt", " "),
                "youtubeLink": f"https://www.youtube.com/watch?v={item['id'].get('videoId', ' ')}",
                "soundcloudLink": None,
                "duration": None,
                "language": "English",
                "file": None,
                "slug": item["snippet"].get("title", " "),
            }
            resp_data.append(resp)

        # Paginate data
        # paginated_data = resp_data[start_index:end_index]
        formatted_data = {
            "data": resp_data,
            "meta": {
                "title": "Connect Originals",
                "heading": None,
                "subHeading": None,
                "backgroundHeading": None,
                "backgroundImage": None,
                "itemsTitle": None,
                "items": [],
                "pagination": {
                    "total": total_videos,
                    "count": len(resp_data),
                    "per_page": records_per_page,
                    "current_page": page,
                    "total_pages": total_pages,
                    "links": {

                    }
                }
            }
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(formatted_data)


@app.route('/connectOriginals/lifestyle', methods=['GET'])
def fetch_lifestyle():
    records_per_page = 5
    page = int(request.args.get('page', 1))

    start_index = (page - 1) * records_per_page
    end_index = page * records_per_page

    try:
        with open("lifestyle.json", "r") as f:
            data = json.loads(f.read())

        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format"}), 500

        total_videos = len(data)
        total_pages = math.ceil(total_videos / records_per_page)

        resp_data = []
        for item in data:
            resp = {
                "video_id": item["id"].get("videoId", " "),
                "id": item["id"].get("videoId", " "),
                "title": item["snippet"].get("title", " "),
                "description": item["snippet"].get("description", " "),
                "image": item["snippet"]["thumbnails"].get("high", {}).get("url", " "),
                "postDate": item["snippet"].get("publishedAt", " "),
                "youtubeLink": f"https://www.youtube.com/watch?v={item['id'].get('videoId', ' ')}",
                "soundcloudLink": None,
                "duration": None,
                "language": "English",
                "file": None,
                "slug": item["snippet"].get("title", " "),
            }
            resp_data.append(resp)

        # Paginate data
        # paginated_data = resp_data[start_index:end_index]
        formatted_data = {
            "data": resp_data,
            "meta": {
                "title": "Connect Originals",
                "heading": None,
                "subHeading": None,
                "backgroundHeading": None,
                "backgroundImage": None,
                "itemsTitle": None,
                "items": [],
                "pagination": {
                    "total": total_videos,
                    "count": len(resp_data),
                    "per_page": records_per_page,
                    "current_page": page,
                    "total_pages": total_pages,
                    "links": {

                    }
                }
            }
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
