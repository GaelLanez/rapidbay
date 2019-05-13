import aiohttp
import settings
from bs4 import BeautifulSoup


async def search(searchterm):
    magnet_links = []
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{settings.PIRATEBAY_HOST}/search/{searchterm}/1/7/0"
        ) as resp:
            data = await resp.text()
    try:
        soup = BeautifulSoup(data, "html.parser")
        trs = soup.find(id="searchResult").find_all("tr")
        for tr in trs:
            try:
                td = tr.find_all("td")[1]
                seeds = int(tr.find_all("td")[2].contents[0])
                a = td.find_all("a")
                title = str(a[0].contents[0])
                magnet_link = a[1]["href"]
                if seeds:
                    magnet_links.append(
                        dict(title=title, magnet=magnet_link, seeds=seeds)
                    )
            except Exception:
                pass
    except Exception:
        pass
    return magnet_links
