class Task:
    _duration = 0

    def __init__(self, start_time):
        self.start_time = start_time
        self.end_time = start_time + Task._duration
        self.run_time = 0

    def update(self):
        self.run_time += 1

    def has_completed(self):
        return self.run_time == Task._duration

class Server:
    _capacity = 0

    def __init__(self):
        self.task_list = []
        self.available_at_tick = 0
    
    def is_full(self):
        return len(self.task_list) == Server._capacity

    def get_available_at_tick(self):
        return self.available_at_tick

    def add_task(self, task):
        if self.is_full():
            return False
        
        self.task_list.append(task)
        self.available_at_tick = task.end_time

    def update(self):
        tasks_to_delete = []
        for task in self.task_list:
            task.update()
            if (task.has_completed()):
                tasks_to_delete.append(task)
        self.task_list = [t for t in self.task_list if t not in tasks_to_delete]

class ServerManager:
    server_list = []

    def update_running_stats(self, now):
        servers_running = []
        for server in ServerManager.server_list:
            server.update()
            if len(server.task_list) > 0:
                servers_running.append(server)
        
        return servers_running

    def has_sever_available(self):
        if not len(ServerManager.server_list):
            return False
        else:
            for server in ServerManager.server_list:
                if server.is_full():
                    continue
                else:
                    return True

    def allocate(self, now, duration):
        max_available_at_tick = 0
        if len(ServerManager.server_list) <= 0:
            return 
        
        pair = {max_available_at_tick: ServerManager.server_list[0]}
        for server in ServerManager.server_list:
            if server.available_at_tick > max_available_at_tick and not server.is_full():
                max_available_at_tick = server.available_at_tick
                pair = {max_available_at_tick: server}
                # s = server
        
        task = Task(now)
        pair[max_available_at_tick].add_task(task)

    def create_server(self, capacity, now, duration):
        server = Server()
        task = Task(now)
        server.add_task(task)
        ServerManager.server_list.append(server)

    def dump(self):
        # print("dumping")
        if len(ServerManager.server_list) == 1:
            print(len(ServerManager.server_list[0].task_list))
        else:
            s = ""
            for server in ServerManager.server_list:
                s += '{},'.format(len(server.task_list))
            print(s)

with open('input', 'r') as input:
    ttask = int(input.readline())
    umax = int(input.readline())

    Task._duration = ttask
    Server._capacity = umax
    manager = ServerManager()
    
    tick = 1
    for line in input:
        ntasks = int(line)
        # print('ntasks {}', ntasks)
        if not ntasks:
            manager.dump()
            ServerManager.server_list = manager.update_running_stats(tick)
            tick += 1
            continue

        for i in range(1, ntasks + 1):
            # print(i)
            if manager.has_sever_available():
                manager.allocate(tick, ttask)
            else:
                manager.create_server(umax, tick, ttask)

        manager.dump()
        ServerManager.server_list = manager.update_running_stats(tick)
        tick += 1
    
    while True:
        if len(ServerManager.server_list) == 0:
            break

        manager.dump()
        ServerManager.server_list = manager.update_running_stats(tick)
        tick += 1
    print('0')