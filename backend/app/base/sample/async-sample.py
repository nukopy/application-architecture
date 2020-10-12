import asyncio


# not async
async def print_sync():
    print("===== sync =====")
    print("hoge1")
    print("hoge2")
    print("hoge3")
    print("hoge4")
    print("hoge5")
    print("hoge6")
    print("hoge7")
    print("hoge8")
    print("hoge9")
    print("hoge10")

    return "hoge11"


async def print_async():
    hoge11 = await print_sync()
    print(hoge11)
    nums = [i for i in range(50)]

    async for i in nums:
        print(f"hoge{i}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_async())
