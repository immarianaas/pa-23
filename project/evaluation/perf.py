import sys
import os

import timeit
import statistics

this_path = os.path.dirname(os.path.abspath(__file__))
syntactic_path = os.path.join(this_path, "..", "syntactic-analysis")
sys.path.append(syntactic_path)

from main import main


main()

loops = 1
iterations = 100

# Measure execution times
execution_times = timeit.repeat("main()", repeat=iterations)

print(f"Execution times: {execution_times}")


std_deviation = statistics.stdev(execution_times)
average_time = statistics.mean(execution_times)


print(f"Standard Deviation: {std_deviation}")
print(f"Average Time: {average_time}")



print("-------------")
total_time = timeit.timeit("main()", number=iterations, globals=globals())
print("Total time:", total_time)
print("Average time:", total_time/iterations)
