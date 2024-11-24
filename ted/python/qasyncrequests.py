# This is a sample Python script.

import asyncio
import aiohttp

# Constants
URL = "[sURL]"  # Replace with the target URL
CONCURRENT_REQUESTS = 10        # Number of concurrent requests per batch
TOTAL_BATCHES = 10              # Number of batches

async def send_request(session, request_id):
    
    """Send a single HTTP GET request."""
    try:
        async with session.get(URL) as response:
            status = response.status
            print(f"Request {request_id}: {status}")
    except Exception as e:
        print(f"Request {request_id} failed: {e}")

async def send_requests_batch(batch_id):
    """Send one batch of requests concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [
            send_request(session, request_id=(batch_id * CONCURRENT_REQUESTS) + i + 1)
            for i in range(CONCURRENT_REQUESTS)
        ]
        await asyncio.gather(*tasks)

async def main():

    """Main function to orchestrate the batches."""
    for batch_id in range(TOTAL_BATCHES):
        print(f"Starting batch {batch_id + 1}...")
        await send_requests_batch(batch_id)
        print(f"Batch {batch_id + 1} completed.")
        # await asyncio.sleep(1)  # Optional delay between batches

if __name__ == "__main__":
    asyncio.run(main())

