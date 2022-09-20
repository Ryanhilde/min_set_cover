import csv
import itertools
import random
import pandas as pd
import math
import time

# Global variables
eps = 0.001
delta = 0.01


# Functions
def separate_pairs(pairs, attribute):
    """Create subsets of separated pairs"""
    separated_pairs = []
    for j in pairs:
        if j[0][attribute] != j[1][attribute]:
            separated_pairs.append(j)
    return separated_pairs


def greedy_set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    universe = set(tuple(row) for row in universe)
    elements = set(e for s in subsets for e in s)
    subsets = [set(ele) for ele in subsets]

    covered = set()
    cover = []
    attributes = []

    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        attributes.append(subsets.index(subset))
        covered |= subset

    return attributes


def vu_calculate_samples(dataset, k_samples):
    samples = []
    for i in range(k_samples):
        samples.append(random.choice(dataset))
    return samples


def vu_alg(dataset, delta, eps):
    m = len(dataset[0])
    time_first = time.process_time()
    k = abs(round(math.log(1/0.01) * math.sqrt(m/eps)))

    sampled_pairs = vu_calculate_samples(dataset, k)
    create_combinations = list(itertools.combinations(sampled_pairs, 2))

    print(len(sampled_pairs))
    print(len(create_combinations))

    subsets = list(map(lambda x: separate_pairs(create_combinations, x), range(m)))
    print(greedy_set_cover(create_combinations, subsets))
    time_update = time.process_time()
    print(f"total time: {time_update - time_first}")


def run_vu_adult_dataset():
    adult_df = pd.read_csv("adult.csv")
    adult_df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
                        'Protective-serv', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
                        'hours-per-week',
                        'native-country']
    adult_df = adult_df.drop(columns='fnlwgt')

    dataset_tuples = list(adult_df.itertuples(index=False))
    print("Running Vu Approx. Alg. on Adult dataset")
    vu_alg(dataset_tuples, delta, eps)


def run_vu_covtype_dataset():
    with open('covtype.csv', newline='') as f:
        reader = csv.reader(f)
        dataset_tuples = [tuple(row) for row in reader]
    print("Running Vu Approx. Alg. on Covtype dataset")
    vu_alg(dataset_tuples, delta, eps)


run_vu_adult_dataset()
# run_vu_covtype_dataset()
