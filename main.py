from atproto import Client
from os import getenv
import requests

def main():
  HANDLE = getenv('HANDLE')
  PASSWORD = getenv('PASSWORD')
  DOWNLOAD_PATH = getenv('DOWNLOAD_PATH')
  LIMIT = getenv('LIMIT')

  client = Client()
  client.login(HANDLE, PASSWORD)
  print(f'Logged in as {client.me.display_name}')

  cursor = None
  all_likes = []

  while True:
    resp = client.app.bsky.feed.get_actor_likes({'actor': HANDLE, 'cursor': cursor})
    all_likes.extend(resp.feed)
    if not resp.cursor:
      break
    cursor = resp.cursor
    print(f"Fetched {len(resp.feed)} likes, total so far: {len(all_likes)}")
    if len(resp.feed) == 0:
      print("No more likes to fetch.")
      break

  print(f"Total liked posts: {len(all_likes)}\n")
  print(f"Now downloading {LIMIT} images")
  for item in all_likes[:LIMIT]:
    try:
      if hasattr(item.post.embed, 'images'):
        image_link = item.post.embed.images[0].fullsize
      if hasattr(item.post.embed, 'media'):
        image_link = item.post.embed.media.images[0].fullsize
    except (IndexError, AttributeError):
      print(f"No image found for post {item.post.uri}")
      continue
    print(f'{image_link}\n')
    img_data = requests.get(image_link).content
    with open(f'{DOWNLOAD_PATH}/{item.post.uri.split("/")[-1]}.png', 'wb') as handler:
      handler.write(img_data)

if __name__ == '__main__':
  main()