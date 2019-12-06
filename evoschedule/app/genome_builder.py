class GenomeBuilder:

    def __init__(self, time_scale, time_per_task, min_task_time):
        """ A class used to generate a Genome object."""

        self.time_scale = time_scale
        self.total_minutes = self.get_total_minutes()

        if self.validate_minimum_task_time(min_task_time):
            self.min_task_time = min_task_time

        if self.validate_task_times(time_per_task):
            self.time_per_task = time_per_task
        
        self.tasks = list(self.time_per_task.keys())
        self.set_num_time_slots()
        self.set_genes_per_task()
        
    def get_total_minutes(self):
        """ Returns the number of minutes based on the time_scale."""

        if self.time_scale == "daily":
            minutes = 24 * 60 # minutes in a day

        elif self.time_scale == "weekly":
            minutes = 7 * 24 * 60
        
        elif self.time_scale == "biweekly":
            minutes = 14 * 24 * 60

        return minutes

    def validate_minimum_task_time(self, min_task_time):
        """ Returns true if the minimum task time is valid.
        
        A valid minimum task time evenly divides into a day's worth of minutes.
        Also a valid minimum task time shall not exceed one day. A minimum
        task time is the minimum amount of consecutive time we wish to spend
        on a task."""

        if min_task_time <= 24 * 60 and (24 * 60) % min_task_time == 0:
            return True
        else:
            msg = "min time task evenly divide 60 if less than or equal to 60 \
                or evenly divide (24*60) if less than 24*60"
            print(msg)
            return False

    def validate_task_times(self, task_times):
        """ Returns True if the task times are valid.
        
        A valid task time is one that is evenly divisible by the minimum task time. """

        total = 0
        for task in task_times:
            if task_times[task] % self.min_task_time != 0:
                msg = "min time task evenly divide 60 if less than or equal to 60 \
                    or evenly divide (24*60) if less than 24*60"
                print(msg)
                return False
            total += task_times[task]

        return total <= self.total_minutes

    def set_num_time_slots(self):
        """ Calculates and returns the number of time slots.

        The number of time slots is determined by the time_scale,
        which is daily, weekly, or biweekly. 
        In addition to the time_scale, the number of time slots is 
        also determined by the minimum_time_per_task, which is an 
        integer that represents the minimum number of minutes that 
        we are to schedule a task for.
        """

        self.n_alleles = self.total_minutes // self.min_task_time

    def set_genes_per_task(self):
        """ Converts time_per_task values which are in minutes, to # genes."""

        self.genes = {}
        for task in self.tasks:
            self.genes[task] = self.time_per_task[task] // self.min_task_time

    def get_genome(self):
        """ Uses the data collected to produce a Genome."""

        from .genome import Genome

        return Genome(self.time_scale, self.tasks, self.genes, self.n_alleles, self.min_task_time)