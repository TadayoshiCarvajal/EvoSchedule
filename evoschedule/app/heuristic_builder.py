class HeuristicBuilder:
    
    def __init__(self, genome, preferences):
        """ It is the job of this class to construct a Heuristic using the user
        preferences. It is assumed the user preferences do not contradict themselves.
        It will be the job of the UI in future version releases of this software to 
        ensure that is the case."""

        valid = self.validate_genome_with_preferences(genome, preferences)
        self.label_values  = {  "avoid":0, 
                                "inconvenient":1, 
                                "neutral":5, 
                                "convenient":10, 
                                "preferred":25, 
                                "required":100}
        if valid:
            self.genome = genome
            self.time_scale = genome.time_scale
            self.preferences = preferences
            self.tasks = genome.tasks
            self.labels  = {"avoid", "inconvenient", "neutral", "convenient", "preferred", "required"}
        else:
            message = "The genome is incompatible with the preferences."
            raise ValueError(message)

        # For weekly and biweekly time_scales
        self.weekday_to_num = {
            'Monday' : 0,
            'Tuesday' : 1,
            'Wednesday' : 2,
            'Thursday' : 3,
            'Friday' : 4,
            'Saturday' : 5,
            'Sunday' : 6,
            'Monday1' : 0,
            'Tuesday1' : 1,
            'Wednesday1' : 2,
            'Thursday1' : 3,
            'Friday1' : 4,
            'Saturday1' : 5,
            'Sunday1' : 6,
            'Monday2' : 7,
            'Tuesday2' : 8,
            'Wednesday2' : 9,
            'Thursday2' : 10,
            'Friday2' : 11,
            'Saturday2' : 12,
            'Sunday2' : 13
        }

        # Convert day of week number to day string for weekly time_scale
        self.num_to_weekday_weekly = {
            0 : 'Monday',
            1 : 'Tuesday',
            2 : 'Wednesday',
            3 : 'Thursday',
            4 : 'Friday',
            5 : 'Saturday',
            6 : 'Sunday'
        }
        # Convert day of week number to day string for biweekly time_scale
        self.num_to_weekday_biweekly = {
            0 : 'Monday1',
            1 : 'Tuesday1',
            2 : 'Wednesday1',
            3 : 'Thursday1',
            4 : 'Friday1',
            5 : 'Saturday1',
            6 : 'Sunday1',
            7 : 'Monday2',
            8 : 'Tuesday2',
            9 : 'Wednesday2',
            10 : 'Thursday2',
            11 : 'Friday2',
            12 : 'Saturday2',
            13 : 'Sunday2',
        }

        self.process_preferences() # build time_fitness dictionary

        self.H = self.preferences_to_heuristic() # build H from time_fitness
        self.time_windows = self.get_time_windows() 

    def validate_genome_with_preferences(self, genome, preferences):
        """ Returns if the genome and the preferences have the same set of tasks."""

        genome_tasks = sorted(genome.tasks)
        pref_tasks = sorted(list(preferences.keys()))
        return genome_tasks == pref_tasks

    def minute_time_to_time(self, minute_time):
        """ Converts number of minutes to a time.
        
        If the time_scale is weekly or biweekly, we use the dictionaries
        num_to_weekday_weekly and num_to_weekday_biweekly to obtain the 
        day of the week."""
        minutes_per_day = 24 * 60
        day_num = minute_time // minutes_per_day
        minute_time = minute_time % minutes_per_day

        if self.time_scale == "daily":
            day = ""
        elif self.time_scale == 'weekly':
            day = self.num_to_weekday_weekly[day_num] + ','
        else:
            day = self.num_to_weekday_biweekly[day_num] + ','
        
        hours = minute_time // 60
        minutes = minute_time % 60

        if hours == 12:
            label = 'PM'
        elif hours > 12:
            label = 'PM'
            hours -= 12
        elif hours == 0:
            hours = 12
            label = 'AM'
        else:
            label = 'AM'

        hours = f"{hours:02d}"
        minutes = f"{minutes:02d}"

        return day + hours + ':' + minutes + label


    def minute_time(self, time):
        """ Converts a time in the form of HH:MM AM/PM to it's number of minutes representation."""

        if self.time_scale != 'daily':
            weekday, time = time.split(',')
            day_num = self.weekday_to_num[weekday]
        else:
            day_num = 0

        time_label = time[-2:]
        time = time[:-2] # strip AM or PM
        time_hr, time_min = time.split(":")
        time_hr, time_min = int(time_hr), int(time_min)
        if time_label == "PM" and time_hr != 12:
            time_hr += 12
        
        time_day_in_minutes = 24 * 60 * day_num
        time_hr_in_minutes = 60 * time_hr
        return time_day_in_minutes + time_hr_in_minutes + time_min

    def time_to_minute_range(self, time_range):
        """" Converts a time range in the form of HH:MM_AM/PM-HH:MM_AM/PM to (X, Y) 
        where X and Y are the minute range representations."""

        # Parses and converts the time
        start, end = time_range.split("-")
        start = self.minute_time(start)
        end = self.minute_time(end)
        if end < start:
            # split into two ranges
            if self.time_scale == 'daily':
                max_num_minutes = 1440
            elif self.time_scale == 'weekly':
                max_num_minutes = 10080
            else: # biweekly
                max_num_minutes = 20160

            r1 = (start, max_num_minutes)
            r2 = (0, end)
            return [r1, r2]
        return (start, end)

    def process_preferences(self):
        """ Constructs the time_fitness dictionary.
        
        The time_fitness dictionary is a nested dictionary. The keys are tasks.
        Each task has it's own inner dictionary for a value. The keys of the inner 
        dictionary are time ranges in the form of minute ranges. Each has as its 
        value a number which corresponds to the fitness of the task being 
        performed during that minute range."""

        self.time_fitness = {task:{} for task in self.tasks}
        for task in self.tasks:
            for label in self.labels:
                label_list = self.preferences[task][label]
                for i in range(len(label_list)):
                    minute_range = self.time_to_minute_range(label_list[i])
                    # this is a tuple if one contiguous range.
                    # this is a list if it was split into two ranges due to overflow.
                    if type(minute_range) == tuple:
                        self.time_fitness[task][minute_range] = self.label_values[label]
                    elif type(minute_range) == list:
                        r1, r2 = minute_range
                        self.time_fitness[task][r1] = self.label_values[label]
                        self.time_fitness[task][r2] = self.label_values[label]

    def time_in_range(self, time, range):
        """ Returns true if a given time lies in the half closed interval of range.
        
        It is closed on the start side (left) and open on the side (right) of the 
        interval. i.e. [start, end). """

        start, end = range
        return time >= start and time < end

    def get_time_slot_value(self, task, time_slot_start_minute):
        """ Returns the fitness of a specified task being performed at a specified time."""

        range_fitness = self.time_fitness[task]
        for minute_range in range_fitness:
            if self.time_in_range(time_slot_start_minute, minute_range):
                return range_fitness[minute_range]
        return self.label_values["neutral"]

    def _show_times(self):
        """ Helper function for showing the times associated with each task in time_fitness."""
        for task in self.time_fitness:
            print(task)
            for rng in self.time_fitness[task]:
                print(rng, self.time_fitness[task][rng])

    def _show_H(self):
        """ Helper function for showing the matrix H."""
        n_time_slots = self.n_time_slots
        time_slot_size = self.time_slot_size
        s = " "
        print(f"{s:^5s}", end=" ")
        for i in range(n_time_slots):
            print(f"{(i*time_slot_size):^4d}", end=" ")
        print()
        H = self.H
        for task in H:
            print(f"{task:^5s}", end = " ")
            for i in range(len(H[task])):
                print(f'{H[task][i]:^4d}', end= " ")
            print()

    def get_time_windows(self):
        """ Gets a list containing the time windows"""
        time_windows = []
        if self.time_scale == 'daily':
            max_minutes = 24 * 60
        elif self.time_scale == 'weekly':
            max_minutes = 24 * 60 * 7
        else:
            max_minutes = 24 * 60 * 7 * 2

        for i in range(self.n_time_slots):
            time_slot_start_minute = (i*self.time_slot_size) % max_minutes
            time_slot_end_minute = ((i+1) * self.time_slot_size) % max_minutes

            start_minute_as_time = self.minute_time_to_time(time_slot_start_minute)
            end_minute_as_time = self.minute_time_to_time(time_slot_end_minute)

            time_window = (start_minute_as_time, end_minute_as_time)
            time_windows.append(time_window)
        return time_windows
        

    def preferences_to_heuristic(self):
        """ Builds the heuristic dictionary H."""
        self.n_time_slots = self.genome.n_alleles
        self.time_slot_size = self.genome.allele_size

        H = {task:[4]*self.n_time_slots for task in self.genome.tasks}
        self.time_windows = []

        for task in self.tasks:
            for i in range(self.n_time_slots):
                time_slot_start_minute = i*self.time_slot_size
                value = self.get_time_slot_value(task, time_slot_start_minute)
                H[task][i] = value

        return H

    def get_heuristic(self):
        """ Returns the Heuristic object."""
        from .heuristic import Heuristic
        return Heuristic(self.H, self.genome, self.time_windows)