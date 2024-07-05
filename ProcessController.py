import multiprocessing
from collections import deque
import time



class ProcessController:
    def __init__(self):
        self.processes = []
        self.tasks_queue = deque()
        self.max_proc = None


    def set_max_proc(self, n):
        self.max_proc = n

    def start(self, tasks, max_exec_time):
        if self.max_proc is None:
            raise ValueError("Max Processes number not set, you can use the max_proc function")

        for task in tasks:
            self.tasks_queue.append(task)

        while self.tasks_queue and len(self.processes) < self.max_proc:
            self._start_new_task(max_exec_time)

    def _start_new_task(self, max_exec_time):
        if self.tasks_queue:
            task, args = self.tasks_queue.popleft()
            process = multiprocessing.Process(target=self._run_task, args=(task, args, max_exec_time))
            process.start()
            self.processes.append(process)

        self._cleanup_processes()

    def _run_task(self, task, args, max_exec_time):
        start_time = time.time()
        p = multiprocessing.Process(target=task, args=args)
        p.start()
        while p.is_alive():
            if time.time() - start_time > max_exec_time:
                p.terminate()
                break
            time.sleep(0.1)
        p.join()

    def _cleanup_processes(self):
        self.processes = [p for p in self.processes if p.is_alive()]

    def wait(self):
        for process in self.processes:
            process.join()

    def wait_count(self):
        return len(self.tasks_queue)

    def alive_count(self):
        self._cleanup_processes()
        return len(self.processes)

# Пример использования
def example(n):
    time.sleep(n)
    print(f"Task with sleep {n} seconds completed.")

if __name__ == "__main__":
    tasks = [
        (example, (2,)),
        (example, (3,)),
        (example, (4,)),
        (example, (5,)),
    ]

    controller = ProcessController()
    controller.set_max_proc(2)
    controller.start(tasks, max_exec_time=6)

    print(f"Number of tasks waiting: {controller.wait_count()}")
    print(f"Number of tasks alive: {controller.alive_count()}")

    controller.wait()
    print("All tasks are completed.")