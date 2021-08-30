import processscheduler as ps

n_workers = 2
n_locations = 1
n_tasks = 2
# ----------->T: 0  1
task_duration = [1, 1]
task_location = [0, 0]

pb = ps.SchedulingProblem("LimitNumberWorkersLocations", horizon=2)

workers = [ps.Worker("Worker_%i" % i) for i in range(n_workers)]

tasks = [
    ps.FixedDurationTask("Task_%i" % i, duration=task_duration[i])
    for i in range(n_tasks)
]

locations = [
    ps.NonConcurrentBuffer(
        "Location_%i" % i, initial_state=2, lower_bound=0, upper_bound=2
    )
    for i in range(n_locations)
]


# assign resources
for i, t in enumerate(tasks):
    # each task needs exactly one worker
    t.add_required_resource(ps.SelectWorkers(workers))
    # each tasks reduce by one the occupation index of the corresponding location/buffer when it starts...
    ps.TaskUnloadBuffer(t, locations[task_location[i]], quantity=1)
    # pb.add_constraint(begin)
    # ...and adds one to the occupation index when it ends
    ps.TaskLoadBuffer(t, locations[task_location[i]], quantity=1)
    # pb.add_constraint(end)

pb.add_objective_flowtime()

solver = ps.SchedulingSolver(
    pb, max_time=60, parallel=True
)  # , debug=True,  verbosity=1,)
# solver.export_to_smt2(smt_filename="exported_smt")
solution = solver.solve()
# with open("solution.json", "w") as f:
#     f.write(solution.to_json_string())
if solution:
    solution.render_gantt_matplotlib(
        render_mode="Resource",
        fig_filename="test_out_with_buffer.png",
        show_indicators=False,
    )
else:
    print("No solution found")
