"""
# Resthru
## Restaurant QM Simulation

## Covers

- Waiting for other processes
- Resources: Resource

## Scenario

A drive-thru restaurant has a specific number of counters
and define a service processes that takes some (random) time.

Customer process arrive at the restaurant at a random time.
If the first counter is available, they start the service process
and wait to finish. If not, they wait until they can use one.
After finished, customer proceed to the next counter until
all counters are passed.

The complete service processes are:
- order
- pay
- take
"""

import os
import sys
import random
import datetime
import simpy

class Restaurante():
    STATE = 0
    TEMP = 0
    SUM_ALL = 0.00
    CALC = [0] * 500  # Input capacity
    RANDOM_SEED = 42  # Random helper

    # Simulation time in minutes
    HOUR_OPEN = 7  # Morning
    HOUR_CLOSE = 23  # Night
    START = HOUR_OPEN * 60
    SIM_TIME = HOUR_CLOSE * 60

    SIM_FACTOR = 1 / 60  # Simulation realtime factor
    PEAK_START = 11
    PEAK_END = 13
    PEAK_TIME = 60 * (PEAK_END - PEAK_START)  # Range of peak hours

    NUM_COUNTERS = 1  # Number of counters in the drive-thru
    # Minutes it takes in each counters
    TIME_COUNTER_A = 2
    TIME_COUNTER_B = 1
    TIME_COUNTER_C = 3

    # Create a customer every [min, max] minutes
    CUSTOMER_RANGE_NORM = [5, 10]  # in normal hours
    CUSTOMER_RANGE_PEAK = [1, 5]  # in peak hours
    """
    Define clear screen function
    """


    def clear(self):
        os.system(['clear', 'cls'][os.name == 'nt'])


    """
    Define exact clock format function
    """


    def toc(self, raw):
        clock = ('%02d:%02d' % (raw / 60, raw % 60))
        return clock


  

    """
    The customer process (each customer has a name)
    arrives at the drive-thru lane, counter, then serviced by the empoyee (ce).
    It then starts the service process for each counters then leaves.
    """
    """
    (Type 2) Define customer behavior at first counter
    """


    def customer2A(self, env, name, wl, ce12, ce3):

        with wl.lane.request() as request:

            if (env.now >= self.SIM_TIME):
                print("[!] Not enough time! %s cancelled" % name)
                env.exit()

            yield request
            yield env.process(wl.serve(name))
            print("[w] (%s) %s is in waiting lane" % (self.toc(env.now), name))

        # Start the actual drive-thru process
        print("[v] (%s) %s is in drive-thru counter" % (self.toc(env.now), name))

        with ce12.employee.request() as request:

            if (env.now + self.TIME_COUNTER_A + self.TIME_COUNTER_B >= self.SIM_TIME):
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            self.CALC[int(name[5:])] = env.now
            yield env.process(ce12.serve(name))
            print("[?] (%s) %s choose the order" % (self.toc(env.now), name))

            yield env.process(ce12.serve(name))
            print("[$] (%s) %s is paying and will take the order" %
                (self.toc(env.now), name))
            env.process(self.customer2B(env, name, ce12, ce3))


    """
    (Type 2) Define customer behavior at second counter
    """


    def customer2B(self, env, name, ce12, ce3):

        with ce3.employee.request() as request:

            if (env.now + self.TIME_COUNTER_C >= self.SIM_TIME):
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            yield env.process(ce3.serve(name))
            print("[^] (%s) %s leaves" % (self.toc(env.now), name))

            global TEMP
            TEMP = int(name[5:])
            self.CALC[int(name[5:])] = env.now - self.CALC[int(name[5:])]


    """
    (Type 3) Define customer behavior at first counter
    """


    def customer3A(self, env, name, wl, ce1, ce2, ce3):

        with wl.lane.request() as request:

            if (env.now >= self.SIM_TIME):
                print("[!] Not enough time! %s cancelled" % name)
                env.exit()

            yield request
            yield env.process(wl.serve(name))
            print("[w] (%s) %s is in waiting lane" % (self.toc(env.now), name))

        # Start the actual drive-thru process
        print("[v] (%s) %s is in drive-thru counter" % (self.toc(env.now), name))

        with ce1.employee.request() as request:

            if (env.now + self.TIME_COUNTER_A >= self.SIM_TIME):
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)

            yield request

            self.CALC[int(name[5:])] = env.now
            yield env.process(ce1.serve(name))
            print("[?] (%s) %s choose the order" % (self.toc(env.now), name))

            print("[2] (%s) %s will pay the order" % (self.toc(env.now), name))
            env.process(self.customer3B(env, name, ce1, ce2, ce3))


    """
    (Type 3) Define customer behavior at second counter
    """


    def customer3B(self, env, name, ce1, ce2, ce3):

        with ce2.employee.request() as request:

            if (env.now + self.TIME_COUNTER_B >= self.SIM_TIME):
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            yield env.process(ce2.serve(name))
            print("[$] (%s) %s is paying the order" % (self.toc(env.now), name))

            print("[3] (%s) %s will take the order" % (self.toc(env.now), name))
            env.process(self.customer3C(env, name, ce1, ce2, ce3))


    """
    (Type 3) Define customer behavior at third counter
    """


    def customer3C(self, env, name, ce1, ce2, ce3):

        with ce3.employee.request() as request:

            if (env.now + self.TIME_COUNTER_C >= self.SIM_TIME):
                print("[!] Not enough time! Assumed %s is quickly finished" % name)
                yield env.timeout(0.5)
                env.exit()

            yield request

            yield env.process(ce3.serve(name))
            print("[^] (%s) %s leaves" % (self.toc(env.now), name))

            global TEMP
            TEMP = int(name[5:])
            self.CALC[int(name[5:])] = env.now - self.CALC[int(name[5:])]


    """
    Define detail of 2 counters setup environment
    """


    def setup2(self, env, cr):
        # Create all counters
        wl = waitingLane(env)
        ce12 = counterFirstSecond(env)
        ce3 = counterThird(env)
        i = 0

        # Create more customers while the simulation is running
        while True:
            yield env.timeout(random.randint(*cr))
            i += 1
            env.process(self.customer2A(env, "Cust %d" % i, wl, ce12, ce3))


    """
    Define detail of 3 counters setup environment
    """


    def setup3(self, env, cr):
        # Create all counters
        wl = waitingLane(env)
        ce1 = counterFirst(env)
        ce2 = counterSecond(env)
        ce3 = counterThird(env)
        i = 0

        # Create more customers while the simulation is running
        while True:
            yield env.timeout(random.randint(*cr))
            i += 1
            env.process(self.customer3A(env, "Cust %d" % i, wl, ce1, ce2, ce3))


    """
    Run the main program, execute via editor or terminal.
    """
    def run (self):
        self.clear()
        print("""
            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            >> Restaurant Queuing Model Simulation
            >> Drive-Thru Fast Food Restaurant Design Model Evaluation
            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>""")
        self.RANDOM_SEED = int(input("Ingrese la semilla: "))

        self.HOUR_OPEN = int(input("Ingrese la hora de apertura: "))
        self.HOUR_CLOSE = int(input("Ingrese la hora de cerrar: "))
        # Simulation time in minutes
        self.START = self.HOUR_OPEN * 60
        self.SIM_TIME = self.HOUR_CLOSE * 60

        self.NUM_COUNTERS = int(input("Ingrese el numero de cajas: "))  # Number of counters in the drive-thru

        # # Create a customer every [min, max] minutes
        # CUSTOMER_RANGE_NORM = [5, 10]  # in normal hours
        # CUSTOMER_RANGE_PEAK = [1, 5]  # in peak hours
        
        
        # Check if the number of counters is specified
        if len(sys.argv) < 2:
            nc = 3
        else:
            nc = int(sys.argv[1])

        # random.seed(RANDOM_SEED) # Helps reproducing the results

        # Has the environment in realtime (wall clock)
        # env = simpy.RealtimeEnvironment(factor=SIM_FACTOR)

        # Has the environment in manual step through
        env = simpy.Environment(initial_time=self.START)
        print("Environment created at %d!" % env.now)

        # Decide the counter model setup
        if nc == 2:
            env.process(self.setup2(env, self.CUSTOMER_RANGE_NORM))
        elif nc == 3:
            env.process(self.setup3(env, self.CUSTOMER_RANGE_NORM))

        print("Setup initialized!")

        print("Start simulation!")
        env.run(until=self.SIM_TIME)
        
        for i in range(TEMP + 1):
            self.SUM_ALL += self.CALC[i]

        averageTimeService = self.SUM_ALL / (TEMP + 1)
        servicePerSecond = 1.00 / (averageTimeService * 60)
        servicePerMinute = servicePerSecond * 60

        print("The end!")
        print("[i] Model: %d counters" % nc)
        print("[i] Average time:       %.4f" % averageTimeService)
        print("[i] Service per minute: %f" % servicePerMinute)

        # print(self.CALC)

"""
Waiting lane class
"""

class waitingLane(object):

    def __init__(self, env):
        self.env = env
        self.lane = simpy.Resource(env, 3)

    def serve(self, cust):
        yield self.env.timeout(0)
        print("[w] (%s) %s entered the area" % (Restaurante().toc(self.env.now), cust))


"""
First counter class
"""


class counterFirst(object):

    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(
            random.randint(Restaurante.TIME_COUNTER_A - 1, Restaurante.TIME_COUNTER_A + 1))
        print("[?] (%s) %s ordered the menu" % (Restaurante().toc(self.env.now), cust))


"""
Second counter class
"""


class counterSecond(object):

    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(
            random.randint(Restaurante.TIME_COUNTER_B - 1, Restaurante.TIME_COUNTER_B + 1))
        print("[$] (%s) %s paid the order" % (Restaurante().toc(self.env.now), cust))


"""
First+Second counter class
"""


class counterFirstSecond(object):

    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(
            random.randint(Restaurante.TIME_COUNTER_A - 1, Restaurante.TIME_COUNTER_A + 1))
        print("[?] (%s) %s ordered the menu" % (Restaurante().toc(self.env.now), cust))

        yield self.env.timeout(
            random.randint(Restaurante.TIME_COUNTER_B - 1, Restaurante.TIME_COUNTER_B + 1))
        print("[$] (%s) %s paid the order" % (Restaurante().toc(self.env.now), cust))


"""
Third counter class
"""


class counterThird(object):

    def __init__(self, env):
        self.env = env
        self.employee = simpy.Resource(env, 1)

    def serve(self, cust):
        yield self.env.timeout(
            random.randint(Restaurante.TIME_COUNTER_C - 1, Restaurante.TIME_COUNTER_C + 1))
        print("[#] (%s) %s took the order" % (Restaurante().toc(self.env.now), cust))
