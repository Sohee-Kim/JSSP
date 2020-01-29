import fileinput
import random

class JobShop(object):
    def __init__(self):
        self.jobs = None

    def file_read(self, path=None):
        with fileinput.input(files=path) as f:
            next(f)
            jobs = [[(int(machine), int(time)) for machine, time in zip(*[iter(line.split())] * 2)]
                    for line in f if line.strip()]

        self.jobs = jobs

    def print_jobs(self, jobs):
        print(len(jobs), len(jobs[0]))
        for job in jobs:
            for machine, time in job:
                print(machine, time, end=" ")
            print()

    def print_schedule(self, jobs, schedule):
        def format_job(time, jobnr):
            if time == 1:
                return '#'
            if time == 2:
                return '[]'

            js = str(jobnr)

            if 2 + len(js) <= time:
                return ('[{:^' + str(time - 2) + '}]').format(jobnr)

            return '#' * time

        job_len = len(jobs)
        machine_len = len(jobs[0])

        tjob = [0] * job_len
        tmachine = [0] * machine_len

        ij = [0] * job_len

        output = [""] * machine_len

        for i in schedule:
            machine, time = jobs[i][ij[i]]
            ij[i] += 1
            start = max(tjob[i], tmachine[machine])
            space = start - tmachine[machine]
            end = start + time
            tjob[i] = end
            tmachine[machine] = end

            output[machine] += ' ' * space + format_job(time, i)

        print("")
        print("Optimal Schedule: ")
        [print("Machine ", idx, ":", machine_schedule) for idx, machine_schedule in enumerate(output)]
        print("")
        print("Optimal Schedule Length: ", max(tmachine))


class TimeExceed(Exception):
    pass
