import os
import sys

import async_timeout
import asyncio
import aiohttp
import requests


class ImageDownloader:

    @staticmethod
    async def _download_coroutine(session, url, storage_folder, timeout):
        with async_timeout.timeout(timeout):
            async with session.get(url) as response:
                try:
                    if response.status == 200:
                        filename = os.path.join(storage_folder, os.path.basename(url))
                        with open(filename, 'wb') as f_handle:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f_handle.write(chunk)
                    return await response.release()
                finally:
                    if sys.exc_info()[0] is not None:
                        # on exceptions, close the connection altogether
                        response.close()
                    else:
                        return await response.release()

    @staticmethod
    async def _download(loop, urls, storage_folder, timeout):
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = [ImageDownloader._download_coroutine(session, url, storage_folder, timeout) for url in urls]
            await asyncio.gather(*tasks, return_exceptions=True)

    @staticmethod
    def download_from_urls(url, storage_path_folder, timeout):
        urls = [url] if not isinstance(url, list) else url
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ImageDownloader._download(loop, urls, storage_path_folder, timeout))
        loop.close()

    @staticmethod
    def download_from_url(url):
        return requests.get(url, timeout=3)


# file = "/home/rick/Projects/lun/floor_plan_project/floor_plan_project/floor_plans/services/image_urls/colorful_floor_plans.txt"
# urls = FileProcessor.extract_urls_from_file(file)
# print(len(urls))


# csv_file = "/home/rick/Projects/lun/image_urls.csv"
# urls = FileProcessor.extract_urls_from_csv(csv_file, 1, 7)
# print(len(urls))



