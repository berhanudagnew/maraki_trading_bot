import asyncio

async def featch_data():
    print("Running featch_data block 1")
    ...
    await asyncio.sleep(2)
    print('done featching .. ')
    # Release execution
    await asyncio.sleep(0)

    print("Running featch_data block 2")
    return 4
    ...

async def print_numbers():
    print("Running print_number block 1")
    ...
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)
    # Release execution
    await asyncio.sleep(0)

    print("Running print_number block 2")
    ...

async def main():
    task_1 = asyncio.create_task(featch_data())
    task_2 = asyncio.create_task(print_numbers())
    value = await task_1
    print(value * 4)
    # await task_1
    await task_2

if __name__ == "__main__":
    asyncio.run(main())