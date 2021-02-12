import asyncio
import random
import time

MENU = {
    "beef": 5,
    "paste": 3,
    "fish and chips": 2,
    "roast": 6,
    "pizza": 1
}

class Order:
    def __init__(self, meal, name):
        self.meal = meal
        self.name = name

def now_time():
    sec = int(time.time() - start_time)
    return f"{sec//60:0>2}:{sec%60:0>2}"

async def cook(name: int, requests : asyncio.Queue):
    while True:
        order = await requests.get()
        meal = order.meal
        custumer = order.name
        need_time = MENU.get(meal)
        print(f"[{now_time()}] cooker {name} start cooking {meal} for {custumer} in {need_time} minutes")
        await asyncio.sleep(need_time)
        print(f"[{now_time()}] cooker {name} finish cooking {meal} for {custumer}")
        requests.task_done()

async def costume(name: int, q : asyncio.Queue):
    sl = random.randint(0, 120)
    # print(f"[{now_time()}] costumer {name} come after {sl} minutes")
    await asyncio.sleep(sl)

    meal_num = random.randint(1, 4)
    menu = list(MENU.keys())
    meals = [random.choice(menu) for _ in range(meal_num)]
    print(f"[{now_time()}] costumer {name} come and make order: {', '.join(meals)}")
    for meal in meals:
        await q.put(Order(meal, name))


async def main(ncost: int, ncook: int):
    q = asyncio.Queue()
    costumers = [asyncio.create_task(costume(i, q)) for i in range(ncost)]
    cookers = [asyncio.create_task(cook(i, q)) for i in range(ncook)]
    await asyncio.wait(costumers)
    await q.join()
    for c in cookers:
        c.cancel()

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main(120, 10))