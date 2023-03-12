import pandas as pd
import time
from datetime import datetime
import requests
import json
from loguru import logger
import argparse
import akshare as ak


if __name__ == '__main__':
    futures_rule_df = ak.futures_rule(date="20230310")
