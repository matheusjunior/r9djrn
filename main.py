server_list = []

class Task:
    _duration = 0

    def __init__(self, start_time, duration):
        self.start_time = start_time
        self.end_time = start_time + duration
        self.run_time = 0
        Task._duration = duration

    def update(self):
        self.run_time += 1

    def has_completed(self):
        return self.run_time == Task._duration

# TODO: need to update server stats
class Server:
    _umax = 0

    def __init__(self, capacity):
        self.task_list = []
        self.tick_available = 0
        Server._umax = capacity
    
    def is_full(self):
        return len(self.task_list) == Server._umax

    def get_tick_available(self):
        return self.tick_available

    def add_task(self, task):
        if self.is_full():
            return False
        self.task_list.append(task)
        # calculate score
        self.tick_available = task.end_time

    def update(self):
        tasks_to_delete = []
        for task in self.task_list:
            task.update()
            if (task.has_completed()):
                tasks_to_delete.append(task)
        self.task_list = [t for t in self.task_list if t not in tasks_to_delete]

def update_running_stats(now):
    servers_running = []
    for server in server_list:
        server.update()
        if len(server.task_list) > 0:
            servers_running.append(server)
    
    return servers_running

# just find if there is any available server
# finding the best one is left for another function
def has_sever_available():
    if not len(server_list):
        return False
    else:
        for server in server_list:
            if server.is_full():
                continue
            else:
                return True

def allocate(now, duration):
    max_tick_available = 0
    for server in server_list:
        if server.tick_available > max_tick_available and not server.is_full():
            max_tick_available = server.tick_available
            pair = {max_tick_available: server}
    
    task = Task(now, duration)
    pair[max_tick_available].add_task(task)

def create_server(capacity, now, duration):
    server = Server(capacity)
    task = Task(now, duration)
    server.add_task(task)
    server_list.append(server)

def dump():
    if len(server_list) == 1:
        print(len(server_list[0].task_list))
    else:
        s = ""
        for server in server_list:
            s += '{},'.format(len(server.task_list))
        print(s)

with open('input', 'r') as input:
    ttask = int(input.readline())
    umax = int(input.readline())
    
    tick = 1
    for line in input:
        ntasks = int(line)
        # print('ntasks {}', ntasks)
        if not ntasks:
            dump()
            server_list = update_running_stats(tick)
            tick += 1
            continue

        for i in range(1, ntasks + 1):
            # print(i)
            if has_sever_available():
                allocate(tick, ttask)
            else:
                create_server(umax, tick, ttask)

        dump()
        server_list = update_running_stats(tick)
        tick += 1
    
    while True:
        if len(server_list) == 0:
            break

        dump()
        server_list = update_running_stats(tick)
        tick += 1
    print('0')