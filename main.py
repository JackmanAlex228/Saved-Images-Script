from atproto import Client
from dotenv import load_dotenv 
from os import getenv, listdir
from loader import Loader
import requests
load_dotenv()

def main():

  # Load environment variables
  HANDLE = getenv('HANDLE')
  PASSWORD = getenv('PASSWORD')
  DOWNLOAD_PATH = getenv('DOWNLOAD_PATH')
  LIMIT = getenv('LIMIT')

  # Initialize client
  client = Client()
  client.login(HANDLE, PASSWORD)
  print(f'Logged in as {client.me.display_name}')

  # Initialize variables
  cursor = None
  all_likes = []
  duplicates = []
  num_fetched = 0

  # Fetch all likes, displaying a status bar in the console
  print(f"Fetching liked posts for {HANDLE}...")
  with Loader(f"Fetching liked posts..."):
    while True:
      resp = client.app.bsky.feed.get_actor_likes({'actor': HANDLE, 'cursor': cursor})
      all_likes.extend(resp.feed)
      if not resp.cursor:
        break
      cursor = resp.cursor
      if len(resp.feed) == 0:
        break
      num_fetched += len(resp.feed)
      print(f" ({num_fetched} liked posts so far)", end='')
    print(f"Total liked posts: {len(all_likes)}\n")

  # Download images
  print(f"Total liked posts: {len(all_likes)}\n")
  print(f"Now downloading {LIMIT} images")
  for item in all_likes[:int(LIMIT)]:
    try:
      if hasattr(item.post.embed, 'images'):
        image_link = item.post.embed.images[0].fullsize
      if hasattr(item.post.embed, 'media'):
        image_link = item.post.embed.media.images[0].fullsize
        image_link = item.post.embed.media.images[0].fullsize
    except (IndexError, AttributeError):
      print(f"No image found for post {item.post.uri}")
      continue
    img_data = requests.get(image_link).content
    filename = f'{item.post.uri.split("/")[-1]}.png'

    # If an image of the same filename is in the download path, skip it
    if filename in listdir(DOWNLOAD_PATH):
      print(f"Skipping {filename}, already downloaded")
      duplicates.append(filename)
      continue

    # Download the image
    with open(f'{DOWNLOAD_PATH}/{filename}', 'wb') as handler:
      handler.write(img_data)

  print(f"Finished!")

if __name__ == '__main__':
  main()