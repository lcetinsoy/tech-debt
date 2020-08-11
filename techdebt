#!/usr/bin/python3

import argparse
import yaml

from techdebt.lib import *


parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="configuration", default="techdebt.yml")

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
    debt_statistics = compute_debt_statistics(debtps, scores)

    plot_debt(debt_statistics)
    print(debt_statistics)


else:
    print('configuration file {} not found'.format(conf_file))
