from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

class Loader:
  def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
    """
    A loader-like context manager

    Args:
      desc (str, optional): The loader's description. Defaults to "Loading..."
      end (str, optional): Message to display when loading is complete
      timeout (float, optional): Time to wait between loading updates
    """
    self.desc = desc
    self.end = end
    self.timeout = timeout

    self.__thread = Thread(target=self._animate, daemon=True)
    self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
    self.done = False
  
  def start(self):
    self.__thread.start()
    return self
  
  def _animate(self):
    for c in cycle(self.steps):
      if self.done:
        break
      print(f"\r{self.desc} {c}", flush=True, end="")
      sleep(self.timeout)

  def __enter__(self):
    self.start()
    return self

  def stop(self):
    self.done = True
    cols = get_terminal_size((80, 20)).columns
    print("\r" + " " * cols, end="", flush=True)
    print(f"\r{self.end}", flush=True)

  def __exit__(self, exc_type, exc_value, tb):
    self.stop()