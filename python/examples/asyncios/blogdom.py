import asyncio
from keyword import kwlist
import socket


async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def main() -> None:
    domains = (f"{kw}.dev" for kw in kwlist)
    coros = [probe(domain) for domain in domains]
    for coro in asyncio.as_completed(coros):
        domain, isAvailable = await coro
        result = "+ " if isAvailable else ""
        print(f"{result} {domain}")


if __name__ == "__main__":
    asyncio.run(main())
