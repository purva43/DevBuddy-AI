import time
import asyncio

# --- Synchronous version ---
def slow_task_sync(name, seconds):
    print(f"Starting {name}...")
    time.sleep(seconds)
    print(f"Finished {name}")

def run_sync():
    start = time.time()
    slow_task_sync("Task A", 2)
    slow_task_sync("Task B", 2)
    slow_task_sync("Task C", 2)
    print(f"Sync total time: {time.time() - start:.1f}s\n")

# --- Async version ---
async def slow_task_async(name, seconds):
    print(f"Starting {name}...")
    await asyncio.sleep(seconds)
    print(f"Finished {name}")

async def run_async():
    start = time.time()
    await asyncio.gather(
        slow_task_async("Task A", 2),
        slow_task_async("Task B", 2),
        slow_task_async("Task C", 2),
    )
    print(f"Async total time: {time.time() - start:.1f}s")

run_sync()
asyncio.run(run_async())