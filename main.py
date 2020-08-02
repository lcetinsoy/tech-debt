import argparse
from techdebt.lib import *


parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="the folder to analyse")
parser.add_argument("--extension", help="file extension")

args = parser.parse_args()

folder = args.folder
ext = args.extension

debtps = get_all_debt_annotations(folder, ext)
debpt_statistics = debt_statistics(debtps)

print(debpt_statistics)

