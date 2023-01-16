import pandas as pd
import csv
import random

def create_workout(muscle):
    # Initialize empty lists to store workout information
    strength_exercises = []
    core_exercises = []
    cardio_exercises = []
    
    # Read from the CSV file
    with open('workouts.csv', 'r') as f:
        print("opened successfully")
        reader = csv.reader(f)
        next(reader) # Skip the header row
        for row in reader:
            muscle_group, workout, reps, link = row
            if muscle in muscle_group:
                strength_exercises.append((workout, reps, link))
            elif "Core" in muscle_group:
                core_exercises.append((workout, reps, link))
            elif "Cardio" in muscle_group:
                cardio_exercises.append((workout, reps, link))
    
    # Choose 3 random strength exercises
    strength_workout = random.sample(strength_exercises, 1)
    # Choose 2 random core exercises
    core_workout = random.sample(core_exercises, 1)
    # Choose 2 random cardio
    cardio_workout = random.sample(cardio_exercises, 1)

    workout = strength_workout + core_workout + cardio_workout

    list_of_exercizes =[]
    #Print the workout
    for exercise in workout:
        list_of_exercizes.append(exercise[0] + " - " + exercise[1])
    return str(list_of_exercizes)
    #return workout
