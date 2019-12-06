def daily_test_data():
    """ Provides test data for the full system test when using "daily" time_scale."""
    time_scale = "daily"
    time_per_task = {
        "Free" : 480,
        "Work" : 480,
        "Sleep" : 480
    }
    min_task_time = 5

    preferences = {
        "Free" : {
            "avoid" : ["09:00AM-05:00PM"],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" : ["08:00PM-10:00PM"],
            "preferred" : ["05:00PM-06:00PM"],
            "required" : []
        },
        "Work" : {
            "avoid" : [],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" : [],
            "preferred" : [],
            "required" : ["09:00AM-05:00PM"]
        },
        "Sleep" : {
            "avoid" : ["09:00AM-05:00PM"],
            "inconvenient" : ["06:00PM-08:00PM"],
            "neutral" : [],
            "convenient" : ["08:00PM-10:00PM"],
            "preferred" : ["10:00PM-07:00AM"],
            "required" : []
        }
    }
    return time_scale, time_per_task, min_task_time, preferences

def weekly_test_data():
    """ Provides test data for the full system test when using "weekly" time_scale."""
    time_scale = "weekly"
    time_per_task = {
        "Free" : 480 * 9,
        "Work" : 480 * 5,
        "Sleep" : 480 * 7
    }
    min_task_time = 60
    preferences = {
        "Free" : {
            "avoid" : [ "Monday,09:00AM-Monday,05:00PM", 
                        "Tuesday,09:00AM-Tuesday,05:00PM", 
                        "Wednesday,09:00AM-Wednesday,05:00PM", 
                        "Thursday,09:00AM-Thursday,05:00PM", 
                        "Friday,09:00AM-Friday,05:00PM"],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" :[ "Monday,06:00PM-Monday,08:00PM", 
                            "Tuesday,06:00PM-Tuesday,08:00PM", 
                            "Wednesday,06:00PM-Wednesday,08:00PM", 
                            "Thursday,06:00PM-Thursday,08:00PM", 
                            "Friday,06:00PM-Friday,08:00PM"],
            "preferred" : [],
            "required" : []
        },
        "Work" : {
            "avoid" : [],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" : [],
            "preferred" : [],
            "required" : [ "Monday,09:00AM-Monday,05:00PM", 
                        "Tuesday,09:00AM-Tuesday,05:00PM", 
                        "Wednesday,09:00AM-Wednesday,05:00PM", 
                        "Thursday,09:00AM-Thursday,05:00PM", 
                        "Friday,09:00AM-Friday,05:00PM"],
        },
        "Sleep" : {
            "avoid" : [ "Monday,09:00AM-Monday,05:00PM", 
                        "Tuesday,09:00AM-Tuesday,05:00PM", 
                        "Wednesday,09:00AM-Wednesday,05:00PM", 
                        "Thursday,09:00AM-Thursday,05:00PM", 
                        "Friday,09:00AM-Friday,05:00PM"],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" : [],
            "preferred" : [ "Monday,10:00PM-Tuesday,06:00AM",
                            "Tuesday,10:00PM-Wednesday,06:00AM",
                            "Wednesday,10:00PM-Thursday,06:00AM",
                            "Thursday,10:00PM-Friday,06:00AM",
                            "Friday,10:00PM-Saturday,06:00AM",
                            "Saturday,10:00PM-Sunday,06:00AM",
                            "Sunday,10:00PM-Monday,06:00AM"],
            "required" : []
        }
    }
    return time_scale, time_per_task, min_task_time, preferences 

def biweekly_test_data():
    """ Provides test data for the full system test when using "biweekly" time_scale."""
    time_scale = "biweekly"
    time_per_task = {
        "Free" : 480 * 9 * 2,
        "Work" : 480 * 5 * 2,
        "Sleep" : 480 * 7 * 2
    }
    min_task_time = 60
    preferences = {
        "Free" : {
            "avoid" : [ "Monday1,09:00AM-Monday1,05:00PM", 
                        "Tuesday1,09:00AM-Tuesday1,05:00PM", 
                        "Wednesday1,09:00AM-Wednesday1,05:00PM", 
                        "Thursday1,09:00AM-Thursday1,05:00PM", 
                        "Friday1,09:00AM-Friday1,05:00PM",
                        "Monday2,09:00AM-Monday2,05:00PM", 
                        "Tuesday2,09:00AM-Tuesday2,05:00PM", 
                        "Wednesday2,09:00AM-Wednesday2,05:00PM", 
                        "Thursday2,09:00AM-Thursday2,05:00PM", 
                        "Friday2,09:00AM-Friday2,05:00PM"],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" :[ "Monday1,06:00PM-Monday1,08:00PM",
                            "Tuesday1,06:00PM-Tuesday1,08:00PM", 
                            "Wednesday1,06:00PM-Wednesday1,08:00PM", 
                            "Thursday1,06:00PM-Thursday1,08:00PM", 
                            "Friday1,06:00PM-Friday1,08:00PM",
                            "Monday2,06:00PM-Monday2,08:00PM", 
                            "Tuesday2,06:00PM-Tuesday2,08:00PM", 
                            "Wednesday2,06:00PM-Wednesday2,08:00PM", 
                            "Thursday2,06:00PM-Thursday2,08:00PM", 
                            "Friday2,06:00PM-Friday2,08:00PM"],
            "preferred" : [],
            "required" : []
        },
        "Work" : {
            "avoid" : [],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" : [],
            "preferred" : [],
            "required" : [ "Monday1,09:00AM-Monday1,05:00PM", 
                        "Tuesday1,09:00AM-Tuesday1,05:00PM", 
                        "Wednesday1,09:00AM-Wednesday1,05:00PM", 
                        "Thursday1,09:00AM-Thursday1,05:00PM", 
                        "Friday1,09:00AM-Friday1,05:00PM",
                        "Monday2,09:00AM-Monday2,05:00PM", 
                        "Tuesday2,09:00AM-Tuesday2,05:00PM", 
                        "Wednesday2,09:00AM-Wednesday2,05:00PM", 
                        "Thursday2,09:00AM-Thursday2,05:00PM", 
                        "Friday2,09:00AM-Friday2,05:00PM"],
        },
        "Sleep" : {
            "avoid" : [ "Monday1,09:00AM-Monday1,05:00PM", 
                        "Tuesday1,09:00AM-Tuesday1,05:00PM", 
                        "Wednesday1,09:00AM-Wednesday1,05:00PM", 
                        "Thursday1,09:00AM-Thursday1,05:00PM", 
                        "Friday1,09:00AM-Friday1,05:00PM",
                        "Monday2,09:00AM-Monday2,05:00PM", 
                        "Tuesday2,09:00AM-Tuesday2,05:00PM", 
                        "Wednesday2,09:00AM-Wednesday2,05:00PM", 
                        "Thursday2,09:00AM-Thursday2,05:00PM", 
                        "Friday2,09:00AM-Friday2,05:00PM"],
            "inconvenient" : [],
            "neutral" : [],
            "convenient" : [],
            "preferred" : [ "Monday1,10:00PM-Tuesday1,06:00AM",
                            "Tuesday1,10:00PM-Wednesday1,06:00AM",
                            "Wednesday1,10:00PM-Thursday1,06:00AM",
                            "Thursday1,10:00PM-Friday1,06:00AM",
                            "Friday1,10:00PM-Saturday1,06:00AM",
                            "Saturday1,10:00PM-Sunday1,06:00AM",
                            "Sunday1,10:00PM-Monday2,06:00AM",
                            "Monday2,10:00PM-Tuesday2,06:00AM",
                            "Tuesday2,10:00PM-Wednesday2,06:00AM",
                            "Wednesday2,10:00PM-Thursday2,06:00AM",
                            "Thursday2,10:00PM-Friday2,06:00AM",
                            "Friday2,10:00PM-Saturday2,06:00AM",
                            "Saturday2,10:00PM-Sunday2,06:00AM",
                            "Sunday2,10:00PM-Monday1,06:00AM"],
            "required" : []
        }
    }
    return time_scale, time_per_task, min_task_time, preferences


def full_system_test(args):
    """ Tests out the entire system. The following things are tested: 
    
    * Creating a GenomeBuilder object
    * Creating a Genome object
    * Creating a HeuristicBuilder object
    * Creating a Heuristic object
    * Creating an EvolutionSimulator object
    * Running the EvolutionSimulator object
    * Creating a GoogleCalendar object
    * Adding events to GoogleCalendar
    * Displaying the evolution graph""" 

    from app.genome_builder import GenomeBuilder
    from app.heuristic_builder import HeuristicBuilder
    from app.evolution_simulator import EvolutionSimulator
    from app.google_calendar import GoogleCalendar
    
    # Unpack the input
    time_scale, time_per_task, min_task_time, preferences = args
    
    # Create the genome
    gb = GenomeBuilder(time_scale, time_per_task, min_task_time)
    genome = gb.get_genome()

    # Create the heuristic
    hb = HeuristicBuilder(genome, preferences)
    heuristic = hb.get_heuristic()

    # Create the evolution simulator
    evolution = EvolutionSimulator( genome, 
                                    heuristic,
                                    n_generations = 500,
                                    seqs_per_gen = 200,
                                    breed_rate = .05,
                                    max_mutation_rate = 0.01)

    best_sequence = evolution.run()
    print(best_sequence.get_schedule())
    print("fitness:", best_sequence.fitness)
    gc = GoogleCalendar(time_scale, schedule=best_sequence.schedule())

    gc.add_events()
    evolution.show_evolution_graph()

def daily_test():
    """ Run a full system test using the daily test data."""
    full_system_test(daily_test_data())

def weekly_test():
    """ Run a full system test using the weekly test data."""
    full_system_test(weekly_test_data())

def biweekly_test():
    """ Run a full system test using the biweekly test data."""
    full_system_test(biweekly_test_data())