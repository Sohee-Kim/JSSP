from .helper import *

import math
import random
import time


class SimulatedAnnealing(object):
    def __init__(self):
        pass

    def __random_schedule(self, job_len, machine_len):
        schedule = [i for i in list(range(job_len)) for _ in range(machine_len)]
        random.shuffle(schedule)

        return schedule

    def __cost(self, jobs, schedule):
        job_len = len(jobs)
        machine_len = len(jobs[0])

        tjob = [0]*job_len
        tmachine = [0]*machine_len

        ij = [0]*job_len

        for i in schedule:
            machine, time = jobs[i][ij[i]]
            ij[i] += 1

            start = max(tjob[i], tmachine[machine])
            end = start + time
            tjob[i] = end
            tmachine[machine] = end

        return max(tmachine)

    def __cost_partial(self, jobs, partial_schedule):
        return self.__cost(jobs, self.__normalize_schedule(partial_schedule))

    def __normalize_schedule(self, jobs, partial_schedule):
        job_len = len(jobs)
        machine_len = len(jobs[0])

        occurences = [0] * job_len
        normalized_schedule = []

        for t in partial_schedule:
            if occurences[t] < machine_len:
                normalized_schedule.append(t)
                occurences[t] += 1
            else:
                pass

        for t, count in enumerate(occurences):
            if count < machine_len:
                normalized_schedule.extend([t] * (machine_len - count))

        return normalized_schedule

    def __lowerBound(self, jobs):
        def lower0():
            return max(sum(time for _, time in job) for job in jobs)

        def lower1():
            mtimes = [0] * self.__num_machines(jobs)

            for job in jobs:
                for machine, time in job:
                    mtimes[machine] += time

            return max(mtimes)

        return max(lower0(), lower1())

    def __num_machines(self, jobs):
        return len(jobs[0])

    def __num_jobs(self, jobs):
        return len(jobs)

    def __shuffle(self, x, start=0, stop=None):
        if stop is None or stop > len(x):
            stop = len(x)

        for i in reversed(range(start + 1, stop)):
            job_len = random.randint(start, i)
            x[i], x[job_len] = x[job_len], x[i]

    def __get_neigbors(self, state, mode="normal"):
        neighbors = []

        for i in range(len(state)-1):
            n = state[:]
            if mode == "normal":
                swap_index = i + 1
            elif mode == "random":
                swap_index = random.randrange(len(state))

            n[i], n[swap_index] = n[swap_index], n[i]
            neighbors.append(n)

        return neighbors

    def __simulated_annealing(self, jobs, T, termination, halting, mode, decrease):
        total_jobs = len(jobs)
        total_machines = len(jobs[0])

        state = self.__random_schedule(total_jobs, total_machines)

        for i in range(halting):
            T = decrease * float(T)

            for k in range(termination):
                actual_cost = self.__cost(jobs, state)

                for n in self.__get_neigbors(state, mode):
                    n_cost = self.__cost(jobs, n)
                    if n_cost < actual_cost:
                        state = n
                        actual_cost = n_cost
                    else:
                        probability = math.exp(-n_cost/T)
                        if random.random() < probability:
                            state = n
                            actual_cost = n_cost

        return actual_cost, state

    def simulated_annealing_search(self, jobs, max_time=None, T=200, termination=10, halting=10, mode="random", decrease=0.8):
        num_experiments = 1

        solutions = []
        best = 10000000

        t0 = time.time()
        total_experiments = 0

        job_len = len(jobs)
        machine_len = len(jobs[0])
        rs = self.__random_schedule(job_len, machine_len)

        while True:
            try:
                start = time.time()

                for i in range(num_experiments):
                    cost, schedule = self.__simulated_annealing(jobs, T=T, termination=termination, halting=halting, mode=mode, decrease=decrease)

                    if cost < best:
                        best = cost
                        solutions.append((cost, schedule))

                total_experiments += num_experiments

                if max_time and time.time() - t0 > max_time:
                    raise TimeExceed("Time is over")

                t = time.time() - start
                if t > 0:
                    print("Best:", best, "({:.1f} Experiments/s, {:.1f} s)".format(
                            num_experiments/t, time.time() - t0))

                if t > 4:
                    num_experiments //= 2
                    num_experiments = max(num_experiments, 1)
                elif t < 1.5:
                    num_experiments *= 2

            except (KeyboardInterrupt, TimeExceed) as e:
                print()
                print("================================================")
                print("Best solution:")
                print(solutions[-1][1])
                print("Found in {:} experiments in {:.1f}s".format(total_experiments, time.time() - t0))

                return solutions[-1]

