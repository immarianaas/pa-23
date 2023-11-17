from collections import defaultdict 
from timeit import timeit

def get_num_entries(data):
    counter = 0
    for [method1, method2list] in data.items():
        counter += len(method2list)
    return counter            


def get_num_true_positives(truth, testing):
    counter = 0
    for [method1, method2list] in testing.items():
        for method2 in method2list:
            if method2 in truth[method1]:
                counter += 1

    return counter

def get_num_false_positives(truth, testing):
    # it's FP if it is on testing but not on truth
    counter = 0

    for [method1, method2list] in testing.items():
        if method1 not in truth:
            counter += len(method2list)

        for method2 in method2list:
            if method2 not in truth[method1]:
                counter += 1

    return counter

def get_num_false_negatives(truth, testing):
    # its FN if it is truth but not on testing
    counter = 0

    for [method1, method2list] in truth.items():
        if method1 not in testing:
            counter += len(method2list)

        for method2 in method2list:
            if method2 not in testing[method1]:
                counter += 1
    
    return counter



def precision(truth, testing):
    TP = get_num_true_positives(truth, testing)
    FP = get_num_false_positives(truth, testing)

    return TP / (TP+FP)

def recall(truth, testing):
    TP = get_num_true_positives(truth, testing)
    FN = get_num_false_negatives(truth, testing)
    return TP / (TP+FN)

def f1score(truth, testing):
    precision_ = precision(truth, testing)
    recall_ = recall(truth, testing)
    return 2*precision_*recall_/(precision_+recall_)



def main(output = False):
    truth_dict = defaultdict(list)
    syn_dict = defaultdict(list)

    # first let's read the truth, main function:
    with open("truth-main.txt", "r") as truth:
        for line in truth:
            meth1, meth2 = line[1:-2].split(", ")

            truth_dict[meth1].append( meth2 )


    # then let's read the syn, main function:
    with open("syn-main.txt", "r") as truth:
        for line in truth:
            meth1, meth2 = line[1:-2].split(", ")

            syn_dict[meth1].append( meth2 )

    if output:
        print("total entries truth:", get_num_entries(truth_dict))
        print("total entries syn:", get_num_entries(syn_dict))
        print("number of true positives:", get_num_true_positives(truth_dict, syn_dict ))

        print("Precision:", precision(truth_dict, syn_dict))
        print("F1-score:", f1score(truth_dict, syn_dict))



    # false negatives: all in truth  that syn    didn't understand
    # false positives: all in syn    that truth  didn't understand
    # true negatives...... cant getit but also not necessary


main(output= True)

iterations = 1000
total_time = timeit("main()", number=iterations, globals=globals())
print("Total time:", total_time)
print("Average time:", total_time/iterations)
