from queue import Queue
from typing import Generator, Any, Optional
from abc import ABC, abstractmethod


class SystemCall(ABC):
    """Abstract base class for system calls."""

    @abstractmethod
    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        """Method to handle the system call in the context of the scheduler and task."""


Coroutine = Generator[SystemCall | None, Any, None]


class Task:
    """Represents a single task in the scheduler."""

    def __init__(self, task_id: int, target: Coroutine) -> None:
        self.task_id = task_id
        self.target = target
        self.syscall_result = None

    def set_syscall_result(self, result: Any) -> None:
        """Sets the result of the last system call."""
        self.syscall_result = result

    def step(self) -> Optional[SystemCall]:
        """Executes one step of the coroutine."""
        try:
            result = self.target.send(self.syscall_result)
            self.syscall_result = None
            return result
        except StopIteration:
            return None


class Scheduler:
    """Scheduler to handle multiple tasks using cooperative multitasking."""

    def __init__(self) -> None:
        self.task_id = 0
        self.task_queue: Queue[Task] = Queue()
        self.task_map: dict[int, Task] = {}
        self.wait_map: dict[int, list[Task]] = {}

    def _schedule_task(self, task: Task) -> None:
        """Schedules a task by adding it to the queue."""
        self.task_queue.put(task)

    def new(self, target: Coroutine) -> int:
        """Creates a new task and schedules it."""
        self.task_id += 1
        task = Task(self.task_id, target)
        self.task_map[self.task_id] = task
        self._schedule_task(task)
        return self.task_id

    def exit_task(self, task_id: int) -> bool:
        """Exits the task and reschedules any waiting tasks."""
        task = self.task_map.pop(task_id, None)
        if task is None:
            return False

        if task_id in self.wait_map:
            for waiting_task in self.wait_map.pop(task_id):
                self._schedule_task(waiting_task)
        return True

    def wait_task(self, task_id: int, wait_id: int) -> bool:
        """Waits for another task to complete."""
        if wait_id not in self.task_map or task_id not in self.task_map:
            return False

        if wait_id not in self.wait_map:
            self.wait_map[wait_id] = []
        self.wait_map[wait_id].append(self.task_map[task_id])
        return True

    def run(self, ticks: Optional[int] = None) -> None:
        """Runs tasks for a specified number of ticks."""
        count = 0
        while not self.empty() and (ticks is None or count < ticks):
            if not self.task_queue.empty():
                task = self.task_queue.get()
                syscall = task.step()

                if syscall is not None:
                    should_reschedule = syscall.handle(self, task)
                    if should_reschedule:
                        self._schedule_task(task)
                elif task.task_id in self.task_map:
                    self.exit_task(task.task_id)

            count += 1

    def empty(self) -> bool:
        """Checks if there are any scheduled tasks."""
        return not bool(self.task_map)


class PrintMessage(SystemCall):
    """System call to print a message."""

    def __init__(self, message: str) -> None:
        self.message = message

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        print(self.message)  # Print the message when this syscall is handled
        return True


class GetTid(SystemCall):
    """System call to get the current task ID."""

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task.set_syscall_result(task.task_id)
        return True


class NewTask(SystemCall):
    """System call to create a new task."""

    def __init__(self, target: Coroutine) -> None:
        self.target = target

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task_id = scheduler.new(self.target)
        task.set_syscall_result(task_id)
        return True


class KillTask(SystemCall):
    """System call to kill a specific task."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        result = scheduler.exit_task(self.task_id)
        task.set_syscall_result(result)
        return True


class WaitTask(SystemCall):
    """System call to wait for a specific task to complete."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        if scheduler.wait_task(task.task_id, self.task_id):
            return False  # Do not reschedule while waiting
        else:
            task.set_syscall_result(False)
            return True


# Infinite ping coroutine
def infinite_ping() -> Coroutine:
    """Infinite coroutine that prints 'ping!'"""
    while True:
        yield PrintMessage("ping!")  # System call to print 'ping!'
        yield  # Allow context switching


# Infinite pong coroutine
def infinite_pong() -> Coroutine:
    """Infinite coroutine that prints 'pong!'"""
    while True:
        yield PrintMessage("pong!")  # System call to print 'pong!'
        yield  # Allow context switching


# Finite counter coroutine
def finite_counter() -> Coroutine:
    """Coroutine that counts from 0 to 4."""
    for i in range(5):
        yield PrintMessage(str(i))  # System call to print the number
        yield  # Allow context switching


# Testing code
import pytest
from _pytest.capture import CaptureFixture

def test_single_task_running(capsys: CaptureFixture[str]) -> None:
    t1 = Task(task_id=1, target=finite_counter())
    t1.step()
    stdout = capsys.readouterr().out
    assert stdout.strip() == '0'


def test_schedule_infinite_tasks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(infinite_ping())
    sched.new(infinite_pong())
    sched.run(ticks=1)

    stdout = capsys.readouterr().out
    assert stdout.strip() == 'ping!'

    sched.run(ticks=1)

    stdout = capsys.readouterr().out
    assert stdout.strip() == 'pong!'

    sched.run(ticks=2)

    stdout = capsys.readouterr().out
    assert stdout.split() == ['ping!', 'pong!']


def test_schedule_for_zero_ticks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(infinite_ping())
    sched.run(ticks=0)

    stdout = capsys.readouterr().out
    assert stdout == ''


def test_schedule_single_finite_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(finite_counter())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.split() == [str(i) for i in range(5)]

    assert sched.empty()


def finite_constant() -> Coroutine:
    for _ in range(3):
        yield PrintMessage("42")
        yield None


def test_schedule_finite_tasks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(finite_counter())
    sched.new(finite_constant())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.split() == ['0', '42', '1', '42', '2', '42', '3', '4']

    assert sched.empty()


def finite_greedy_task(message: str) -> Coroutine:
    for _ in range(3):
        print(message)
    yield None  # task without yield is not a coroutine


def test_schedule_non_cooperative_tasks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(finite_greedy_task('ping'))
    sched.new(finite_greedy_task('pong'))
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.split() == ['ping', 'ping', 'ping', 'pong', 'pong', 'pong']

    assert sched.empty()


def ping_with_tid() -> Coroutine:
    tid = yield GetTid()
    for i in range(5):
        yield PrintMessage(f'ping from {tid}')  # System call to print the message
        yield None


def pong_with_tid() -> Coroutine:
    tid = yield GetTid()
    for i in range(3):
        yield PrintMessage(f'pong from {tid}')  # System call to print the message
        yield None


def test_schedule_tasks_with_tid(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(ping_with_tid())
    sched.new(pong_with_tid())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'ping from 1',
        'pong from 2',
        'ping from 1',
        'ping from 1',
        'pong from 2',
        'ping from 1',
        'ping from 1',
    ]


# Uncomment the following line to run tests using pytest
# pytest.main()
