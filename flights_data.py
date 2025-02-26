import asyncio
from datetime import datetime, timedelta
import itertools
from kiwi import Kiwi
from kayak import Kayak
from momondo import Momondo
from scraper import DATE_FORMAT

def tasks_params()->list[tuple[str,str,int,int]]:
    """
    Creates the task parameters for our scraping
    """
    cities = ['ROME', 'LONDON', 'PARIS']

    # Using itertools.product to generate city combinations
    city_combinations = [(source, destination) for source, destination in itertools.product(cities, repeat=2) if
                         source != destination]

    # Create all task parameters
    return [
        (source, destination, ttt, los)
        for (source, destination) in city_combinations
        for ttt in range(1, 31)  # TTT between 1 and 30
        for los in range(1, 6)  # LOS between 1 and 5
    ]

async def worker(worker_id: int, queue: asyncio.Queue)-> None:
    """
    Worker function for running batched asyng scraping
    :param worker_id: id for the worker
    :param queue: the async.Queue to refer to
    """
    while not queue.empty():
        momondo_result, kayak_result, kiwi_result = False, False, False
        try:
            source, destination, ttt, los = await queue.get()

            # Get data without writing to file
            kayak_result = await Kayak(
                departure_date=(datetime.today() + timedelta(days=ttt)).strftime(DATE_FORMAT),
                return_date=(datetime.today() + timedelta(days=ttt + los)).strftime(DATE_FORMAT),
                origin_city=source,
                destination_city=destination
            ).write_data(ttt, los)

            kiwi_result = await Kiwi(
                departure_date=(datetime.today() + timedelta(days=ttt)).strftime(DATE_FORMAT),
                return_date=(datetime.today() + timedelta(days=ttt + los)).strftime(DATE_FORMAT),
                origin_city=source,
                destination_city=destination
            ).write_data(ttt, los)

            momondo_result = await Momondo(
                departure_date=(datetime.today() + timedelta(days=ttt)).strftime(DATE_FORMAT),
                return_date=(datetime.today() + timedelta(days=ttt + los)).strftime(DATE_FORMAT),
                origin_city=source,
                destination_city=destination
            ).write_data(ttt, los)

            print(f"Worker {worker_id} completed task: {kayak_result, kiwi_result, momondo_result if kayak_result and kiwi_result and momondo_result else None}")

        except Exception as e:
            print(f"Worker {worker_id} encountered error: {e}\n{kayak_result, kiwi_result if kayak_result and kiwi_result else None}")
        finally:
            queue.task_done()

async def scrape_and_save() -> None:
    """
    Main flow of the collecting process
    (create all possible combination params for scraper -> creates queue for all combinations -> batch-fire the async process of scraping)
    """
    queue = asyncio.Queue()
    for params in tasks_params():
        queue.put_nowait(params)

    print(f"Created queue with {queue.qsize()} tasks")

    # Create 5 worker tasks to process the queue concurrently
    workers = [asyncio.create_task(worker(i, queue)) for i in range(5)]

    # Wait until the queue is fully processed
    await queue.join()

    # Cancel our worker tasks
    for w in workers:
        w.cancel()

    print("All tasks completed")