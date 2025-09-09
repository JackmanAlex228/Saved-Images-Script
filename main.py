from atproto import Client
from loader import Loader
from pathlib import Path
import requests
import logging
import glob
import yaml

# Finds files of duplicate names withing given directories
def file_exists_in_paths(filename: str, process_paths: list[str]) -> str | bool:
  for path in process_paths:
    if path.endswith('/*'):
      # Expand child directories recursively
      base = Path(path[:-2]) # remove /*
      for subdir in base.iterdir():
        if subdir.is_dir():
          # Look for the file recursively inside each subdir
          if any(subdir.rglob(filename)):
            return subdir
    else:
      dir_path = Path(path)
      if (dir_path / filename).exists():
        return dir_path
  return None


def main():

  # Starting logger
  logging.basicConfig(
    filename='downloader.log', 
    level=logging.INFO,
    filemode="w"
  )
  logger = logging.getLogger(__name__)
  logger.info('Started')

  # Load config variables from yaml
  try:
    with open('config.yaml', 'r') as file:
      env_vars = yaml.safe_load(file)
      HANDLE = env_vars['handle']
      PASSWORD = env_vars['password']
      DOWNLOAD_PATH = env_vars['download_path']
      LIMIT = env_vars['limit']
      PROCESS_PATHS = env_vars['process_paths']
  except FileNotFoundError:
      print("The config.yaml file was not found.")
      logger.info("The config.yaml file was not found.")
  except yaml.YAMLError as exc:
      print("There was an error loading the YAML file:", exc)
      logger.info("There was an error loading the YAML file:", exc)

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
  logger.info('Fetching liked posts...')
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
      logger.info(f"({num_fetched} liked posts so far)")
      print(f"({num_fetched} liked posts so far)", end='')
    logger.info(f"Total liked posts: {len(all_likes)}\n")
    print(f"Total liked posts: {len(all_likes)}\n")

  # Download images
  logger.info(f"Total liked posts: {len(all_likes)}\n")
  print(f"Total liked posts: {len(all_likes)}\n")
  with Loader(f"Downloading media files..."):
    for item in all_likes[:int(LIMIT)]:
      try:
        if hasattr(item.post.embed, 'images'):
          image_link = item.post.embed.images[0].fullsize
        if hasattr(item.post.embed, 'media'):
          image_link = item.post.embed.media.images[0].fullsize
      except (IndexError, AttributeError):
        logger.info(f"No image found or post {item.post.uri}")
        continue
      img_data = requests.get(image_link).content
      filename = f'{item.post.uri.split("/")[-1]}.png'

      # If an image of the same filename is in the process path(s), skip it
      path_of_dupe = file_exists_in_paths(filename, PROCESS_PATHS)
      if path_of_dupe:
        logger.info(f'File {filename} already exists in path {path_of_dupe}')
        duplicates.append(filename)
        continue

      # Download the image
      with open(f'{DOWNLOAD_PATH}/{filename}', 'wb') as handler:
        handler.write(img_data)

  logger.info('Finished!')
  print(f"Finished!")
  print(f"There are {len(duplicates)} duplicate files in the download path.")

if __name__ == '__main__':
  main()