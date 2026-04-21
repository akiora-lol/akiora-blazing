import grpc
from settings import Settings

settings = Settings()

_channels: dict[str, grpc.aio.Channel] = {}


def get_community_channel() -> grpc.aio.Channel:
    if "community" not in _channels:
        _channels["community"] = grpc.aio.insecure_channel(settings.community_service_address)
    return _channels["community"]


def get_messenger_channel() -> grpc.aio.Channel:
    if "messenger" not in _channels:
        _channels["messenger"] = grpc.aio.insecure_channel(settings.messenger_service_address)
    return _channels["messenger"]


def get_game_channel() -> grpc.aio.Channel:
    if "game" not in _channels:
        _channels["game"] = grpc.aio.insecure_channel(settings.game_service_address)
    return _channels["game"]


async def close_all_channels():
    for channel in _channels.values():
        await channel.close()
    _channels.clear()
