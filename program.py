# Computational Algorithm for Simulation and Data Analysis
# Lodinu Kalugalage

# used for random_sample
import random

import sys
import matplotlib.pyplot as plt

# these are used in part 3
NO_EXTERN = True
if not NO_EXTERN:
    import termcolor

# storing python's range so it isn't affected when range below shadows it
python_range = range


# we load this dynamically from github
HEIGHTS_FILE_NAME = 'heights.txt'
HEIGHTS_URL = "https://raw.githubusercontent.com/hexsocean/static/main/heights.txt"

# Utility functions for loading from path and urls


def load_from_path(fpath, line_mid):
    with open(fpath, 'r') as f:
        res = []
        for line in f:
            res += [float(x) for x in line_mid(line).split(',')]
        return res


def load_from_url(url, fpath, line_mid):
    import os.path as path
    if not path.exists(fpath):
        print(f"Downloading {fpath}...")
        from urllib import request
        request.urlretrieve(url, fpath)
    return load_from_path(fpath, line_mid)

# For loading in the sample dataset


def load_heights():
    return load_from_url(HEIGHTS_URL, HEIGHTS_FILE_NAME, lambda l: l.strip("ï»¿"))


# Part 1


def len(data: list):
    '''
    gets the length of a list

    Can't use the standard python len() because it
    is forbidden, so iterate through the list and
    count the elements
    '''

    n = 0
    for _ in data:
        n += 1
    return n


def minimum(data: list):
    '''
    gets the minimum value in a list
    '''
    min_val = data[0]
    for n in data:
        min_val = (n if n < min_val else min_val)
    return min_val


def maximum(data: list):
    '''
    gets the maximum value in a list
    '''
    max_val = data[0]
    for n in data:
        max_val = (n if n > max_val else max_val)
    return max_val


def range(data: list):
    '''
    gets the range of data in a list
    '''
    return maximum(data) - minimum(data)


def total(data: list):
    '''
    gets the total of items in a list
    '''
    total = 0
    for n in data:
        total += n
    return total


def mean(data: list):
    '''
    gets the mean of the items in a list
    '''
    return total(data) / len(data)


def mode(data: list):
    '''
    gets the mode of items in a list
    '''
    modes = []
    mode_count = 0
    # converted to a set to get unique values
    for n in set(data):
        x = data.count(n)
        if x > mode_count:
            modes = [n]
            mode_count = x
        if x == mode_count:
            modes.append(n)
    modes = list(set(modes))
    modes.sort()
    return modes


# The functions below may copy the data into a new list
# and sort it, so that the original data is not modified
# this is important as it maintains immutability
#
# ideally python's standard `sorted` could be
# used here, but it is forbidden


def ceil(n):
    # ceil works by using the truncating property of int()
    # so we negate it, truncate, and negate it again
    return int(-1 * n // 1 * -1)


def floor(n):
    return int(n // 1)


def lerp(a, b, t):
    return float(a) + (float(b) - float(a)) * t


def median(data):
    working_data = data.copy()
    working_data.sort()
    # median is the middle value
    pos = 0.5 * (len(working_data) + 1)
    midf = floor(pos) - 1
    midc = ceil(pos) - 1
    return lerp(working_data[midf], working_data[midc], 0.5)


def lower_quartile(data: list):
    working_data = data.copy()
    working_data.sort()
    pos = 0.25 * (len(working_data) + 1)
    midf = floor(pos) - 1
    midc = ceil(pos) - 1
    # we lerp between the two values upper and lowwer the pos
    # this is because the pos is not always an integer
    return lerp(working_data[midf], working_data[midc], pos - floor(pos))


def upper_quartile(data: list):
    working_data = data.copy()
    working_data.sort()
    pos = 0.75 * (len(working_data) + 1)
    midf = floor(pos) - 1
    midc = ceil(pos) - 1
    # unlike lower quartile, we slice from half to end
    # odd or even length does matter as we have to
    # account for the middle value
    return lerp(working_data[midf], working_data[midc], pos - floor(pos))


def five_number_summary(data: list):
    '''
    gets the five number summary of items in a list
    '''
    return [minimum(data), lower_quartile(data), median(data), upper_quartile(data), maximum(data)]


def interquartile_range(data: list):
    '''
    gets the iqr of items in a list
    '''
    return upper_quartile(data) - lower_quartile(data)


def variance(data: list):
    '''
    gets the variance of items in a list
    '''
    working_data = data.copy()
    working_data.sort()

    data_length = len(working_data)
    mean_val = mean(working_data)

    total = 0
    for n in working_data:
        total += (n - mean_val) ** 2

    return total / data_length


def standard_deviation(data: list):
    '''
    gets the standard deviation of items in a list
    '''
    return variance(data) ** 0.5


def random_sample(data: list, sample_size: int) -> list:
    '''
    gets a random sample of items in a list
    '''
    working_data = data.copy()
    working_data.sort()

    data_length = len(working_data)

    sample_range = data_length - 1

    sample = []
    for _ in python_range(sample_size):
        sample.append(working_data[random.randint(0, sample_range)])

    return sample


# Part 2

#  input get and validation functions


def err(msg):
    '''
    prints an error message
    '''
    fmsg = "ERROR: " + msg
    if NO_EXTERN:
        print(fmsg)
        return
    print(termcolor.colored(fmsg, "red"))


def input_validation_base(prompt: str, move, check, pass_err=False):
    '''
    this functionality is shared by add *_validated_input functions

    `move` and `check` aren't typed, as that would require importing the
    `typing` module (`typeing.Callable`), which is forbidden
    '''
    while True:
        try:
            value = move(input(prompt))
            if check(value) == True:
                return value
        except:
            if pass_err:
                return None
            err('Input parsing error.')
            pass


def integer_validated_input(prompt: str, check, nullable: bool = False):
    '''
    gets an integer input from the user and validates it
    '''

    def anon_check_fn(value: int) -> bool:
        if value == None and not nullable:
            err("Value must be a number")
            return False
        if nullable and value == None:
            return True
        if value >= check[0] and value <= check[1]:
            return True
        else:
            err("Value must be between {} and {}".format(check[0], check[1]))
            return False

    return input_validation_base(prompt, int, anon_check_fn, nullable)


def float_validated_input(prompt: str, check: tuple):
    '''
    gets a float input from the user and validates it
    '''

    def anon_check_fn(value: float) -> bool:
        if value == None:
            err("Value must be a number")
            return False
        if value >= check[0] and value <= check[1]:
            return True
        else:
            err("Value must be between {} and {}".format(check[0], check[1]))
            return False

    return input_validation_base(prompt, float, anon_check_fn)


def float_list_validation_middleware(value: list) -> bool:
    '''
    validates a list of floats
    '''
    if type(value) != list:
        err("Must be a list!")
        return False
    for n in value:
        if type(n) != float:
            err("List must only contain numbers!")
            return False
    return True


def get_top_level_input(nullable: bool = False):
    '''
    gets the top level input from the user
    '''
    option = integer_validated_input('''
What kind of data would like to analyse?
(1) A list of space-separated data
(2) Values and their frequencies
(3) Stem-and-leaf data
(4) Filepath (csv style)
(5) Sample (heights.txt)
Enter the number next to your choice: ''', (1, 5), True)
    return option


def accept_list_input() -> list:
    '''
    gets a list of space-separated data from the user
    '''

    data = input_validation_base('''
You have selected to enter space-separated data.
Enter or paste the list of data separated by spaces: 
''', lambda x: [float(y) for y in x.split(' ')], float_list_validation_middleware)
    return data


def accept_frequency_input() -> tuple:
    '''
    gets values and their frequencies from the user
    '''

    # this is done so we can reuse the same function instead of creating two
    # delegates
    first_pass_count = None

    def anon_check_fn(value: list) -> bool:
        if not float_list_validation_middleware(value):
            return False
        if first_pass_count:
            if len(value) == first_pass_count:
                return True
            else:
                err(
                    f"Frequencies must be the same length as the values.")
                return False
        return True

    values = input_validation_base('''
You have selected to enter VALUES and their FREQUENCIES.
First, enter or paste the VALUES, separated by spaces: ''', lambda x: [float(y) for y in x.split(' ')], anon_check_fn)
    first_pass_count = len(values)
    frequencies = input_validation_base('''
Now enter the corresponding FREQUENCIES separated by spaces: ''', lambda x: [float(y) for y in x.split(' ')],
                                        anon_check_fn)

    data = []
    for value, frequency in zip(values, frequencies):
        data += [value] * int(frequency)
    return data


def accept_input_with_stem_and_leaves() -> list:
    '''
    gets stem-and-leaf data from the user
    '''

    # we need this because a zero character string cannot get converted to
    # a float
    def anon_map_fn(x):
        res = []
        for n in x.split(' '):
            if len(n) != 0:
                res.append(float(n))

        return res

    stem_leaf_list = []
    print('''
    You have selected stem-and-leaf data.
    Enter data row by row, separated by spaces.
    Press enter without typing anything when done.
    ''')
    while True:
        data = input_validation_base(
            '''Enter row: ''', anon_map_fn, float_list_validation_middleware)
        if len(data) == 0:
            if len(stem_leaf_list) < 1:
                err("You must enter at least one row!")
                continue
            break
        if len(data) < 1:
            err("Each row must contain at least one number (stem)!")
            continue
        if len(data) < 2:
            err("This row will be ignored (no leaves)!")
            continue
        # check for negative numbers
        should_continue = False
        for n in data[1:]:
            if n < 0:
                err("Leaves cannot contain negative numbers!")
                should_continue = True
                continue
        if should_continue:
            continue
        stem_leaf_list += [data]
    res = []
    for stem_leaf in stem_leaf_list:
        stem = stem_leaf[0]
        leaves = stem_leaf[1:]
        for leaf in leaves:
            negative_stem = float(stem) < 0
            adapted_leaf = -leaf if negative_stem else leaf
            res.append(float(stem) * 10 + float(adapted_leaf))
    return res


def accept_analyse_mode():
    '''
    gets an analysation mode
    '''
    return integer_validated_input('''Choose an option for what you would like to calculate;
(1) Mean (2) Median
(3) Mode (4) Range
(5) Interquartile Range
(6) Standard Deviation
(7) Five-number summary
Enter the number next to your choice: ''', (1, 7))


def accept_end_prompt():
    '''
    gets a prompt to end the program
    '''
    return integer_validated_input('''
What would you like to do next?
(1) Perform additional statistical analysis on current data
(2) Enter new data of the same type as before
(3) Start over from the beginning
(4) Exit
''', (1, 4))


# helper tool thing that creates a binary version of a number and
# checks against another number (binary AND)
def enable_set(src, v):
    return 1 << (src - 1) & int(bin(v)[2:].zfill(3)[::-1], 2) != 0


def userland():
    '''
    userland data entry and validation
    '''
    option = None
    data = []
    analyse_mode = None
    end_prompt = 3
    while True:
        if enable_set(end_prompt, 0b001):
            option = get_top_level_input()
            if option is None:
                break
        # we need all data to be converted to a list
        if enable_set(end_prompt, 0b011):
            if option == 1:
                data = accept_list_input()
            elif option == 2:
                data = accept_frequency_input()
            elif option == 3:
                data = accept_input_with_stem_and_leaves()
            elif option == 4:
                import os.path as path
                fpath = input("filepath: ")
                while not path.exists(fpath):
                    err("Filepath doesn't exist.")
                    fpath = input("filepath: ")

                data = load_from_path(fpath, lambda x: x)
            elif option == 5:
                data = load_heights()

        analyse_mode = accept_analyse_mode()

        if analyse_mode == 1:
            print("Mean: {}".format(mean(data)))
        elif analyse_mode == 2:
            print("Median: {}".format(median(data)))
        elif analyse_mode == 3:
            mode_res = mode(data)
            # done so it is gramatically correct
            print("Mode{}: {}".format('s' if len(mode_res) else '', mode(data)))
        elif analyse_mode == 4:
            print("Range: {}".format(range(data)))
        elif analyse_mode == 5:
            print("Interquartile Range: {}".format(interquartile_range(data)))
        elif analyse_mode == 6:
            print("Standard Deviation: {}".format(standard_deviation(data)))
        elif analyse_mode == 7:
            d = five_number_summary(data)
            print(
                f'''Five-number summary:
minimum: {d[0]:.4f}
lower quartile: {d[1]:.4f}
median: {d[2]:.4f}
upper quartile: {d[3]:.4f}
maximum: {d[4]:.4f}''')
        end_prompt = accept_end_prompt()
        if end_prompt == 4:
            break


# part 3
# This part uses sns (seaborn), which is a wrapper around matplotlib
# to display data.


def part_three_simulate(data: list, sample_count: int, sample_size: int = 5):
    samples_mean = []
    for _ in python_range(sample_count):
        samples_mean += [mean(random_sample(data, sample_size))]

    # setting information
    plt.hist(samples_mean, density=True, bins=10, edgecolor='black')
    plt.title("Sampling Distribution of Means")
    plt.xlabel("Height (cm)")


def part_three_simulate_quad(data: list, sample_count: int):
    # four different iterations of what we did above
    sample_set = []
    for sample_size in [5, 10, 20, 40]:
        samples_mean = []
        sample_set += [samples_mean]
        for _ in python_range(sample_count):
            samples_mean += [mean(random_sample(data, sample_size))]

    # creating a figure with 2 rows and 2 columns
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].hist(sample_set[0], density=True, bins=10, edgecolor='black')
    axes[0, 1].hist(sample_set[1], density=True, bins=10, edgecolor='black')
    axes[1, 0].hist(sample_set[2], density=True, bins=10, edgecolor='black')
    axes[1, 1].hist(sample_set[3], density=True, bins=10, edgecolor='black')

    # setting information
    axes[0, 0].set_title("Sample Size = 5")
    axes[0, 0].set_xlabel("Height (cm)")
    axes[0, 1].set_title("Sample Size = 10")
    axes[0, 1].set_xlabel("Height (cm)")
    axes[1, 0].set_title("Sample Size = 20")
    axes[1, 0].set_xlabel("Height (cm)")
    axes[1, 1].set_title("Sample Size = 40")
    axes[1, 1].set_xlabel("Height (cm)")

    fig.suptitle("Simulated samples of different Sample Sizes")
    fig.tight_layout()


# userland


if __name__ == '__main__':
    # generating graphs
    if 'load' in sys.argv:
        heights = load_heights()
        if '1' in sys.argv:
            part_three_simulate(heights, 20)
        if '2' in sys.argv:
            part_three_simulate_quad(heights, 20)

        plt.savefig('graphs.png')
    else:
        userland()
