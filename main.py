from JobShopScheduling import *


if __name__ == '__main__':
    job_ob = JobShop()
    jobs = job_ob.file_read('examples/15x15')

    machine_len = len(job_ob.jobs[0])
    job_len = len(job_ob.jobs)
    print("Chosen file:", 'examples/15x15')
    print("Number of machines:", machine_len)
    print("Number of jobs:", job_len)
    job_ob.print_jobs(job_ob.jobs)

    sa_ob = SimulatedAnnealing()
    cost, solution = sa_ob.simulated_annealing_search(job_ob.jobs, max_time=20, T=int(200), termination=int(10), halting=int(10), mode='random', decrease=float(0.8))

    job_ob.print_schedule(job_ob.jobs, solution)
