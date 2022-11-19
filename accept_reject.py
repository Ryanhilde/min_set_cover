import csv
import itertools
import random
import pandas as pd
import math
import time

# Global variables
eps = 0.001
delta = 0.1


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

    # Check the subsets cover the universe
    for i in subsets:
        subset = set(i)
        universe = universe - subset

    if len(universe) == 0:
        return "pass"
    else:
        return "fail"


def motwani_calculate_samples(dataset, k_samples):
    samples = []
    for i in range(k_samples):
        sample_1 = random.choice(dataset)
        sample_2 = random.choice(dataset)
        if sample_1 != sample_2:
            samples.append(tuple([sample_1, sample_2]))
    return samples


def run_alg(dataset, total_time, tuning_variable):
    m = len(dataset[0])
    time_first = time.process_time()

    correct_counter = 0
    total_counter = 0
    values = []

    # stuff = list(range(0, len(dataset[0])))
    stuff = []
    for i in list(range(0, len(dataset[0]))):
        flip = random.randint(0, 150)
        if flip == 1:
            stuff.append(i)
    for L in range(len(stuff) + 1):
        for subset in itertools.combinations(stuff, L):
            values.append(subset)
    del values[0]

    motwani_k = round(m / eps)
    motwani_sampled_pairs = motwani_calculate_samples(dataset, motwani_k)

    for i in values:
        vu_k = round(tuning_variable * (m / math.sqrt(eps)))
        vu_sampled_pairs = motwani_calculate_samples(dataset, vu_k)

        motwani_subsets = list(map(lambda x: separate_pairs(motwani_sampled_pairs, x), list(i)))
        vu_subsets = list(map(lambda x: separate_pairs(vu_sampled_pairs, x), list(i)))

        motwani = greedy_set_cover(motwani_sampled_pairs, motwani_subsets)
        vu = greedy_set_cover(vu_sampled_pairs, vu_subsets)

        if motwani == vu:
            correct_counter += 1
        total_counter += 1

    print("percentage of correctly identified: " + str(correct_counter / total_counter))
    print("Sample size of Motwani: " + str(motwani_k))
    print("Sample size of Vu: " + str(vu_k))
    print("Size of tuple subsets: " + str(len(values)))
    print('\n')
    time_update = time.process_time()
    total_time.append(time_update - time_first)
    return correct_counter / total_counter


def run_alg_naive(dataset, attributes):
    m = len(dataset[0])
    motwani_k = round(m / eps)
    motwani_sampled_pairs = motwani_calculate_samples(dataset, motwani_k)

    vu_k = round(m / math.sqrt(eps))
    vu_sampled_pairs = motwani_calculate_samples(dataset, vu_k)

    motwani_subsets = list(map(lambda x: separate_pairs(motwani_sampled_pairs, x), attributes))
    vu_subsets = list(map(lambda x: separate_pairs(vu_sampled_pairs, x), attributes))

    motwani = greedy_set_cover(motwani_sampled_pairs, motwani_subsets)
    vu = greedy_set_cover(vu_sampled_pairs, vu_subsets)
    if motwani == vu:
        print("pass")
    else:
        print("fail")


def run_motwani_adult_dataset():
    adult_df = pd.read_csv("adult.csv")
    adult_df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
                        'Protective-serv', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
                        'hours-per-week',
                        'native-country']
    adult_df = adult_df.drop(columns={'fnlwgt', 'education-num'})

    dataset_tuples = list(adult_df.itertuples(index=False))
    total_time = []
    avg_acc = 0
    for i in range(10):
        avg_acc += run_alg(dataset_tuples, total_time, 1)

    print(str(avg_acc / 10))
    # print("total time: " + str(sum(total_time) / (len(total_time))))


def run_motwani_covtype_dataset():
    with open('covtype.csv', newline='') as f:
        reader = csv.reader(f)
        dataset_tuples = [tuple(row) for row in reader]

    total_time = []
    avg_acc = 0
    for i in range(10):
        avg_acc += run_alg(dataset_tuples, total_time, 1)

    print(str(avg_acc / 10))
    # print("total time: " + str(sum(total_time) / (len(total_time))))


def run_cps():
    with open('cps_2016-08.csv', newline='') as f:
        reader = csv.reader(f)
        dataset_tuples = [tuple(row) for row in reader]

    total_time = []
    avg_acc = 0
    for i in range(10):
        avg_acc += run_alg(dataset_tuples, total_time, 1)
    print(str(avg_acc / 10))


# run_motwani_adult_dataset()
# run_motwani_covtype_dataset()
run_cps()
