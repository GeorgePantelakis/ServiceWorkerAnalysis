import os
import multiprocessing as mp
import sys

from docker_config import *
from docker_monitor import *

if __name__== "__main__":
	remove_containers()
