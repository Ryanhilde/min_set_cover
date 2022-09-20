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
        if [j[0][i] for i in attribute] != [j[1][i] for i in attribute]:
            separated_pairs.append(j)
    return separated_pairs


def greedy_set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    universe = set(tuple(row) for row in universe)
    elements = set(e for s in subsets for e in s)
    subsets = [set(ele) for ele in subsets]

    # Check the subsets cover the universe

    covered = set()
    cover = []
    attributes = []

    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        attributes.append(subsets.index(subset))
        covered |= subset

    return attributes


def motwani_calculate_samples(dataset, k_samples):
    samples = []
    for i in range(k_samples):
        sample_1 = random.choice(dataset)
        sample_2 = random.choice(dataset)
        if sample_1 != sample_2:
            samples.append(tuple([sample_1, sample_2]))
    return samples


def motwani_alg(dataset, delta, eps):
    m = len(dataset[0])
    time_first = time.process_time()
    k = abs(round(math.log((math.pow(2, m) / delta), (1 / 1 - eps))))
    sampled_pairs = motwani_calculate_samples(dataset, k)

    values = [*range(0, len(dataset[0]), 1)]
    values_list = []
    for L in range(len(values)):
        for subset in itertools.combinations(values, L):
            values_list.append(subset)

    subsets = list(map(lambda x: separate_pairs(sampled_pairs, x), values_list))
    print(values_list[2071-1])
    greedy_set_cover(sampled_pairs, subsets)
    time_update = time.process_time()
    print(f"total time: {time_update - time_first}")


def run_motwani_adult_dataset():
    adult_df = pd.read_csv("adult.csv")
    adult_df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
                        'Protective-serv', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
                        'hours-per-week',
                        'native-country']
    adult_df = adult_df.drop(columns='fnlwgt')

    dataset_tuples = list(adult_df.itertuples(index=False))
    print("Running Motwani Brute Force Alg. on Adult dataset")
    motwani_alg(dataset_tuples, delta, eps)


def run_motwani_covtype_dataset():
    with open('covtype.csv', newline='') as f:
        reader = csv.reader(f)
        dataset_tuples = [tuple(row) for row in reader]
    print("Running Motwani Brute Force Alg. on Covtype dataset")
    motwani_alg(dataset_tuples, delta, eps)


# run_motwani_adult_dataset()
run_motwani_covtype_dataset()
