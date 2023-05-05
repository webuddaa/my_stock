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
    df = ak.futures_zh_spot(symbol='V2309,P2309,V2307', market="CF", adjust='0')
