import random
import time
from time import sleep

import asyncio
from datetime import datetime, timedelta
import itertools
from kiwi import Kiwi
from kayak import Kayak
from scraper import DATE_FORMAT
from renew_ip import renew_ip_address

import os

CITIES = ['ROME', 'LONDON', 'PARIS']


def clean_dir(dir_name: str) -> None:
    for file in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file)
        if os.path.isfile(file_path):  # Only delete files
            os.remove(file_path)


def purge() -> None:
    clean_dir('cookies')
    clean_dir('sessions')
    renew_ip_address()


def tasks_params(source: str, destination: str) -> list[tuple[str, str, int, int]]:
    """
    Creates the task parameters for our scraping
    """


    # Create all task parameters
    return [
        (source, destination, ttt, los)
        for ttt in range(1, 31)  # TTT between 1 and 30
        for los in range(1, 6)  # LOS between 1 and 5
    ]


async def worker(worker_id: int, queue: asyncio.Queue, batch_counter: asyncio.Queue) -> None:
    """
    Worker function for running batched async scraping
    :param worker_id: id for the worker
    :param queue: the async.Queue to refer to
    :param batch_counter: queue to track completed tasks for batch processing
    """
    while not queue.empty():
        momondo_result, kayak_result, kiwi_result = False, False, False
        try:
            source, destination, ttt, los = await queue.get()

            # Get data without writing to file
            kiwi_result = await Kiwi(
                departure_date=(datetime.today() + timedelta(days=ttt)).strftime(DATE_FORMAT),
                return_date=(datetime.today() + timedelta(days=ttt + los)).strftime(DATE_FORMAT),
                origin_city=source,
                destination_city=destination
            ).write_data(ttt, los)

            kayak_result = await Kayak(
                departure_date=(datetime.today() + timedelta(days=ttt)).strftime(DATE_FORMAT),
                return_date=(datetime.today() + timedelta(days=ttt + los)).strftime(DATE_FORMAT),
                origin_city=source,
                destination_city=destination
            ).write_data(ttt, los)

            # momondo_result = await Momondo(
            #     departure_date=(datetime.today() + timedelta(days=ttt)).strftime(DATE_FORMAT),
            #     return_date=(datetime.today() + timedelta(days=ttt + los)).strftime(DATE_FORMAT),
            #     origin_city=source,
            #     destination_city=destination
            # ).write_data(ttt, los)

            print(
                f"Worker {worker_id} completed task: {kayak_result, kiwi_result, momondo_result if kayak_result and kiwi_result and momondo_result else None}")

        except Exception as e:
            print(
                f"Worker {worker_id} encountered error: {e}\n{kayak_result, kiwi_result if kayak_result and kiwi_result else None}")
        finally:
            queue.task_done()
            await batch_counter.put(1)  # Signal that a task is complete


async def batch_monitor(batch_counter: asyncio.Queue, batch_size: int = 5):
    """
    Monitors completed tasks and runs purge() after each batch
    :param batch_counter: queue to track completed tasks
    :param batch_size: number of tasks in a batch before purging
    """
    count = 0
    while True:
        await batch_counter.get()
        count += 1
        batch_counter.task_done()

        if count >= batch_size:
            print(f"Batch of {batch_size} tasks completed. Running purge()...")
            purge()
            count = 0


async def scrape_and_save(source: str, destination: str) -> None:
    """
    Main flow of the collecting process
    (create all possible combination params for scraper -> creates queue for all combinations -> batch-fire the async process of scraping)
    """
    task_queue = asyncio.Queue()
    batch_counter = asyncio.Queue()  # Queue to track task completion for batching
    scrape_params = tasks_params(source, destination)
    random.shuffle(scrape_params)
    for params in scrape_params:
        task_queue.put_nowait(params)

    print(f"Created queue with {task_queue.qsize()} tasks")

    # Create the batch monitor
    batch_monitor_task = asyncio.create_task(batch_monitor(batch_counter, 5))

    # Create worker tasks to process the queue concurrently
    workers = [asyncio.create_task(worker(i, task_queue, batch_counter)) for i in range(18)]

    # Wait until the main task queue is fully processed
    await task_queue.join()

    # Cancel our worker tasks
    for w in workers:
        w.cancel()

    # Cancel the batch monitor task
    batch_monitor_task.cancel()

    print("All tasks completed")

def get_data()-> None:
    """
    running the main flow of collecting all flights data
    :return: Flights.csv file
    """
    for _ in range(0,3):
        for trak in [(source, destination) for source, destination in itertools.product(CITIES, repeat=2) if source != destination]:
            asyncio.run(scrape_and_save(trak[0], trak[1]))
            purge()
            time.sleep(60*60) # Sleep for one hour
        sleep(60*60*24) # Wait for the next snapshot date
