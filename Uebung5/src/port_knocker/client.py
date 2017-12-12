import argparse

parser = argparse.ArgumentParser(description='monitor')
parser.add_argument('--shared-key', metavar='INT', type=int, required=True)
parser.add_argument('--num-knocks', metavar='INT', type=int, required=True)
parser.add_argument('IP/DOMAIN', type=str)
parser.add_argument('PORT', type=int)
args = parser.parse_args()
