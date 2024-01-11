import sys
import os

import timeit
import statistics

import math

this_path = os.path.dirname(os.path.abspath(__file__))
syntactic_path = os.path.join(this_path, "..", "abstract_interpreter")
sys.path.append(syntactic_path)

from testDemo import main_func

#main()


def repeat():
    number = 50
    iterations = 100

    # Measure execution times
    execution_times = timeit.repeat("main_func()", repeat=iterations, number=number, globals=globals())
    print(f"SEM - Execution times: {execution_times}")

    std_deviation = statistics.stdev(execution_times)
    average_time = statistics.mean(execution_times)

    print(f"Standard Deviation: {std_deviation}")
    print(f"Average Time: {average_time}")


def time():

    num_repeat = 10
    num_loops = 1
    times = []
    for _ in range(num_repeat):
        total_time = timeit.timeit("main_func()", number=num_loops, globals=globals())
        print("Total time:", total_time)
        print("Average time:", total_time/iterations)


# repeat()

##########
# OUTPUT - repeat()
##########
number = 50
iterations = 100

execution_times = [0.4224700570339337, 0.4429233630653471, 0.48365686694160104, 0.42008877999614924, 0.4280100769829005, 0.4310735099716112, 0.4483656770316884, 0.5107808189932257, 0.47375317302066833, 0.4826447010273114, 0.44064520101528615, 0.4464295220095664, 0.43463950091972947, 0.46645470301155, 0.4206692830193788, 0.4217665670439601, 0.43256654299329966, 0.42809528508223593, 0.43140057707205415, 0.43195390910841525, 0.43110341008286923, 0.4368094059173018, 0.48292803403455764, 0.46879525494296104, 0.5258987070992589, 0.4338182550854981, 0.4434471180429682, 0.4304013450164348, 0.41782033105846494, 0.42505624995101243, 0.46126557898242027, 0.4294114770600572, 0.4543775279307738, 0.4248010660521686, 0.4307817999506369, 0.43935879203490913, 0.4580675259931013, 0.42723094299435616, 0.4243295129854232, 0.43130045488942415, 0.422370569081977, 0.42983240203466266, 0.4279357569757849, 0.42476703599095345, 0.4301783130504191, 0.42987963499035686, 0.4257496959762648, 0.4780045719817281, 0.43050524801947176, 0.4197985539212823, 0.4245604849420488, 0.42809644306544214, 0.41911432705819607, 0.4300056319916621, 0.4233494020299986, 0.43203828495461494, 0.4284167280420661, 0.4263456939952448, 0.4271808339981362, 0.4740102030336857, 0.42922289902344346, 0.42902844899799675, 0.425481186946854, 0.4158881549956277, 0.4209257160546258, 0.42617042805068195, 0.4250099640339613, 0.41964310593903065, 0.42085595696698874, 0.43514260405208915, 0.4642369020730257, 0.44912013702560216, 0.43459546798840165, 0.43727834802120924, 0.4400444140192121, 0.4288014490157366, 0.4757018000818789, 0.4312319819582626, 0.43961599899921566, 0.42599153600167483, 0.43851495697163045, 0.4315929199801758, 0.47942855302244425, 0.4437070160638541, 0.43721077195368707, 0.45005030801985413, 0.439203510992229, 0.4410807240055874, 0.4316282869549468, 0.4351480600889772, 0.4299679429968819, 0.43007113004568964, 0.43955574289429933, 0.48185901704709977, 0.44151825690642, 0.42747455707285553, 0.4273472250206396, 0.43869176192674786, 0.42946300003677607, 0.4328272429993376]
# len(execution_times) = iterations

# log of the execution times in MILLISSECONDS
times = [ math.log(elem*1000/iterations) for elem in execution_times]
times = [ elem*1000/number for elem in execution_times]

print(times)

mean = statistics.mean(times)
std = statistics.stdev(times)

print("mean:", mean)
print("std:", std)