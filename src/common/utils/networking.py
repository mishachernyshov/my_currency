import aiohttp

session: aiohttp.ClientSession | None = None


async def get_session():
    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession()
    return session
