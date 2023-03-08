import asyncio
import aiohttp

async def fetch_file(file_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://server-a-ip:port/get_file/", data={"file_name": file_name}) as response:
            return await response.json()

async def main():
    file_contents = await fetch_file("example.txt")
    if file_contents["file"]:
        with open("example.txt", "wb") as f:
            f.write(file_contents["file"])
            print("File saved.")
    else:
        print("File not found.")

asyncio.run(main())
