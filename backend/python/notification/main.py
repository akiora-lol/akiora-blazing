import asyncio

from app import app
from ioc import container
from setup import setup


async def main():
    await setup()
    try:
        await app.run()
    finally:
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
