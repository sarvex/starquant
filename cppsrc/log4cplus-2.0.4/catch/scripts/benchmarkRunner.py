#!/usr/bin/env python3

import subprocess, os, sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from statistics import median, stdev
from datetime import datetime

def get_commit_hash():
    res = subprocess.run('git rev-parse HEAD'.split(), check=True, stdout=subprocess.PIPE, universal_newlines=True)
    return res.stdout.strip()

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} benchmark-binary')
    exit(1)


num_runs = 10
data = defaultdict(list)


def parse_file(file):

    def recursive_search(node):
        if node.tag == 'TestCase':
            results = node.find('OverallResult')
            time = results.get('durationInSeconds')
            data[node.get('name')].append(float(time))
        elif node.tag in ('Group', 'Catch'):
            for child in node:
                recursive_search(child)

    tree = ET.parse(file)
    recursive_search(tree.getroot())

def run_benchmarks(binary):
    call = [binary] + '-d yes -r xml -o'.split()
    for i in range(num_runs):
        file = f'temp{i}.xml'
        print(f'Run number {i}')
        subprocess.run(call + [file])
        parse_file(file)
        # Remove file right after parsing, because benchmark output can be big
        os.remove(file)


# Run benchmarks
run_benchmarks(sys.argv[1])

result_file = '{:%Y-%m-%dT%H-%M-%S}-{}.result'.format(datetime.now(), get_commit_hash())


print(f'Writing results to {result_file}')
with open(result_file, 'w') as file:
    for k in sorted(data):
        file.write(
            f'{k}: median: {median(data[k])} (s), stddev: {stdev(data[k])} (s)\n'
        )
