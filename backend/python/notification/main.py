# test_imports.py
import sys

# Проверяем protobuf
try:
    import google.protobuf

    print(f"✅ protobuf version: {google.protobuf.__version__}")
except ImportError:
    print("❌ protobuf not installed")
    sys.exit(1)


# Проверяем ваши сгенерированные файлы
try:
    from game.v1.gameseries_service_pb2 import (
        ChampLockRequest as ChampLockRequest,
        DESCRIPTOR as DESCRIPTOR,
        DraftActionRequest as DraftActionRequest,
        ToggleReadyRequest as ToggleReadyRequest,
    )

    print("✅ Generated protobuf imports work!")
except ImportError as e:
    print(f"❌ Generated imports failed: {e}")
