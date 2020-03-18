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
    
    def is_at_load_limit(self):
        return len(self.task_list) == Server._capacity

    def get_available_at_tick(self):
        return self.available_at_tick

    def add_task(self, task):
        if self.is_at_load_limit():
            return False
        
        self.task_list.append(task)
        self.available_at_tick = task.end_time

    def update_tasks(self):
        tasks = []
        for task in self.task_list:
            task.update()
            if (task.has_completed()):
                tasks.append(task)

        self._cleanup_tasks(tasks)

    def _cleanup_tasks(self, tasks):
        self.task_list = [t for t in self.task_list if t not in tasks]

class ServerManager:
    _server_list = []

    def is_empty(self):
        return not len(self._server_list)

    def update_servers(self):
        servers = []
        for server in self._server_list:
            server.update_tasks()
            if not len(server.task_list):
                servers.append(server)

        self._shutdown_unloaded_servers(servers)

    def allocate_task(self, now):
        if not self._has_server_available():
            self._create_and_boot_server(now)
        else:
            max_tick = 0
            if len(self._server_list) <= 0:
                return

            pair = {max_tick: self._server_list[0]}
            for server in self._server_list:
                if server.available_at_tick > max_tick and not server.is_at_load_limit():
                    max_tick = server.available_at_tick
                    pair = {max_tick: server}

            task = Task(now)
            pair[max_tick].add_task(task)

    def _shutdown_unloaded_servers(self, servers):
        self._server_list = [s for s in self._server_list if s not in servers]

    def _create_and_boot_server(self, now):
        server = Server()
        task = Task(now)
        server.add_task(task)
        self._server_list.append(server)

    def _has_server_available(self):
        if not len(self._server_list):
            return False
        else:
            for server in self._server_list:
                if server.is_at_load_limit():
                    continue
                else:
                    return True

    def dump(self):
        if len(self._server_list) == 1:
            print(len(self._server_list[0].task_list))
        else:
            s = ""
            for server in self._server_list:
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
        if not ntasks:
            manager.dump()
            manager.update_servers()
            tick += 1
            continue

        for i in range(1, ntasks + 1):
            manager.allocate_task(tick)

        manager.dump()
        manager.update_servers()
        tick += 1
    
    while True:
        if manager.is_empty():
            break

        manager.dump()
        manager.update_servers()
        tick += 1
    print('0')