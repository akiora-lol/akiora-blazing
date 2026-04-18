import asyncio

from app.app import serve


def main():
    asyncio.run(serve())


if __name__ == "__main__":
    main()
