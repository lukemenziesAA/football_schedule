    for person in players:
        for role in roles:
            for day in range(days):
                obj += assignments[slot, person, role, day]
problem += lpSum(obj), 'Sum_of_everything'


# Add constraints
for day in range(days):
    for slot in range(slots):
        for role in roles:
            # In every time slot, each role is assigned to exactly one person
            problem += lpSum(assignments[slot, person, role, day]
                             for person in players) == 1, \
                'one person for {} in slot {} day {}'.format(role, slot, day)


for day in range(days):
    for slot in range(slots):
        for person in players:
            # In every time slot, each player is assigned to exactly one role
            problem += lpSum(assignments[slot, person, role, day]
                             for role in roles) <= 1, \
                'one role for person {} in slot {} for day {}'.format(person,
                                                                      slot,
                                                                      day)

for day in range(days):
    for person in players:
        # Nobody plays too many slots, restrict to a maximum of 3 slots
        problem += lpSum(assignments[slot, person, role, day]
                         for slot in range(slots) for role in roles) <= \
            max_assignments_per_person, \
            'limit plays for person {} for day {}'.format(person, day)

for day in range(days):
    for person in players:
        # Nobody plays too little, ensure minimum slots played in 2*10minutes
        problem += lpSum(assignments[slot, person, role, day]
                         for slot in range(slots)
                         for role in roles) >= min_slots_per_person, \
            'min plays for person {} for day {}'.format(person, day)


for day in range(days):
    for person in players:
        for role in roles:
            # Players don't play more than once in a position per day
            problem += lpSum(assignments[slot, person, role, day]
                             for slot in range(slots)) <= 1, \
                'person {} doesnt play position {} more than once on day {}'\
                .format(person, role, day)


for person in players:
    for role in roles:
        # Players get to try every position at least once
        problem += lpSum(assignments[slot, person, role, day]
                         for slot in range(slots)
                         for day in range(days)) >= 1, \
            'player {} plays position {} at least once'.format(person, role)

if days > 3:
    for person in range(players_len-1):
        # Players have an equal number of plays
        problem += lpSum(assignments[slot, players[person], role, day]
                         for slot in range(slots)
                         for day in range(days)
                         for role in roles) \
            == (assignments[slot, players[person+1], role, day]
                for slot in range(slots)
                for day in range(days)
                for role in roles)


problem.writeLP('rota_generator_problem.txt')

problem.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[problem.status])


vertical = ['slot_{}_day_{}'.format(slot + 1, day + 1)
            for day in range(days) for slot in range(slots)]

# Dataframe containing results
results = DataFrame(get_persons(slots, players, roles, days, assignments),
                    index=players, columns=vertical).T
