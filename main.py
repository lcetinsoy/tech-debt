#!/usr/bin/python3

import argparse
import yaml

from techdebt.lib import *


parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="configuration")

parser.add_argument("--folder", help="the folder to analyse")
parser.add_argument("--extension", help="file extension")

args = parser.parse_args()


conf_file = args.conf
if os.path.isfile(conf_file):

    with open(conf_file) as f:
        options = yaml.load(f)

    folders = options['folder']

    excluded_folders = folders['excluded']
    included_folders = folders['included']

    extensions = options['extensions']
    scores = options['scores']

    debtps = analyse_debt(included_folders, extensions, excluded_folders)


    debpt_statistics = debt_statistics(debtps, scores)



print(debpt_statistics)

