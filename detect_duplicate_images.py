from pathlib import Path
import difPy
import logging
import yaml
import os

def compare_files(PATHS):

  # Starting logger
  logging.basicConfig(
    filename='compare.log',
    level=logging.INFO,
    filemode="w"
  )
  logger = logging.getLogger(__name__)
  logger.info('Started')

  # Load config variables from yaml
  try:
    with open('config.yaml', 'r') as file:
      env_vars = yaml.safe_load(file)
      PROCESS_PATHS = env_vars['process_paths']
  except FileNotFoundError:
    print("The config.yaml file was not found")
    logger.info("The config.yaml file was not found.")
  except yaml.YAMLError as exc:
    print("There was an error loading the YAML file:", exc)
    logger.info("There was an error loading the YAML file:", exc)

  # Process paths for recursively
  for PATH in PATHS:
    if PATH.endswith('\*'):
      # Expand child directories recursively
      base = Path(PATH[:-2])
      for subdir in base.iterdir():
        if subdir.is_dir():
          # Look for the file recursively inside each subdir
          PATHS.append(os.path.normpath(subdir))
    # Check whether the path exists. If it does, add it to the search
    if not os.path.exists(PATH):
      print(f"Error: Directory {PATH} not found")
    else:
      dif = difPy.build(PATHS)
      search = difPy.search(dif)
      print(f"Duplicates found:\n {search.result}")
      logger.info("Duplicates found:\n", search.result)