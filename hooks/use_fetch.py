from reactpy import hooks

def use_fetch(url):
    data, set_data = hooks.use_state(None)
    loading, set_loading = hooks.use_state(True)
    error, set_error = hooks.use_state("")

    async def fetch_data():
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    set_data(await resp.json())
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)

    hooks.use_effect(lambda: fetch_data(), [url])
    return data, loading, error
