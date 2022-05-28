import random
import re
import time
from urllib.parse import urljoin
from xmlrpc.client import ServerProxy

from dateutil import parser
import requests
from tqdm import tqdm


def get_distributions_list(base_url):
    client = ServerProxy(base_url)
    distributions = client.list_packages()
    return distributions


def get_names_stats(
    all_names,
    possible_chars,
    required_chars=set(),
    round_decimals=5,
    sample_size=3,
    random_state=42
):
    all_names_count = len(all_names)
    names = [name for name in all_names if required_chars <= set(name) <= possible_chars]
    names_count = len(names)
    names_prop = round(names_count / all_names_count, round_decimals)

    print(f'Possible chars: {"".join(sorted(possible_chars))}')
    print(f'Required chars: {"".join(sorted(required_chars))}')
    print(f'Names count: {names_count}')
    print(f'Names proportion: {names_prop:.{round_decimals}f}')

    if names:
        random.seed(random_state)
        names_sample = random.sample(names, k=min(sample_size, len(names)))
        print(f'Examples: {names_sample}')

    print()

    return names


def get_distribution_info(base_url, distribution_name):
    distribution_info_url = urljoin(base_url, '/pypi/{distribution_name}/json')
    response = requests.get(distribution_info_url.format(distribution_name=distribution_name))
    response.raise_for_status()
    distribution_info = response.json()
    return distribution_info


def get_distribution_update_stats(base_url, distributions, delay=0.1):
    update_stats = {}
    incorrect_distributions = {}

    for distribution_name in tqdm(distributions):
        try:
            distribution_info = get_distribution_info(base_url, distribution_name)
            last_updated = distribution_info['urls'][-1]['upload_time_iso_8601']
            update_stats[distribution_name] = parser.parse(last_updated)
        except Exception as e:
            incorrect_distributions[distribution_name] = e

        time.sleep(delay)

    return update_stats, incorrect_distributions


def check_alternative_urls(distribution_name, delay=0.1):
    pattern = r'[.\-_]'
    project_url = 'https://pypi.python.org/project/{project_name}'
    punctuation = set('.-_')

    for match in re.finditer(pattern, distribution_name):
        char_idx = match.start()
        char = distribution_name[char_idx]

        for replace_char in sorted(punctuation - set(char)):
            alt_distribution_name = list(distribution_name)
            alt_distribution_name[char_idx] = replace_char
            alt_distribution_name = ''.join(alt_distribution_name)
            alt_distribution_url = project_url.format(project_name=alt_distribution_name)

            response = requests.get(alt_distribution_url)
            response.raise_for_status()
            redirected_url = response.url
            print(f'{alt_distribution_url} -> {redirected_url}')
            time.sleep(delay)
