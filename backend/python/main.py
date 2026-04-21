import os
import re
import sys
import subprocess
from pathlib import Path


def find_proto_files(root_dir: Path):
    """Рекурсивно находит все .proto файлы"""
    l = list(root_dir.rglob("*.proto"))
    l = [p for p in l if "googleapis" not in p.as_uri().split("/")]
    l = [p for p in l if "google" not in p.as_uri().split("/")]
    print(l)

    return l


def add_init_files(directory: Path):
    """Рекурсивно добавляет __init__.py во все поддиректории"""
    # Проходим по всем поддиректориям
    for subdir in sorted(directory.rglob("*")):
        if subdir.is_dir():
            init_file = subdir / "__init__.py"
            if not init_file.exists():
                # Создаем пустой __init__.py
                init_file.touch()
                print(f"   📄 Created {init_file.relative_to(directory.parent)}")

    # Также создаем __init__.py в корневой директории, если его нет
    root_init = directory / "__init__.py"
    if not root_init.exists():
        root_init.touch()
        print(f"   📄 Created {root_init.relative_to(directory.parent)}")


def main():

    proto_root = Path("../proto").resolve()

    output_dirs = [
        Path("proto-build/src/proto_build").resolve(),
    ]
    googleapis_path = proto_root / "googleapis"

    print(f"Proto source directory : {proto_root}")
    print(f"Output directory      : {output_dirs}\n")
    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)

    proto_files = find_proto_files(proto_root)

    if not proto_files:
        print(f"❌ No .proto files found in {proto_root}")
        return

    print(f"✅ Found {len(proto_files)} proto files:")
    for f in proto_files:
        print(f"   - {f.relative_to(proto_root)}")

    for output_dir in output_dirs:
        cmd = [
            "uv",
            "run",
            "python",
            "-m",
            "grpc_tools.protoc",
            f"-I{proto_root}",
            f"--python_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            f"--pyi_out={output_dir}",  # ← Дополнительные .pyi от protobuf
            *[str(f) for f in proto_files],
        ]

        print(f"\n🚀 Running command:")
        print(" ".join(cmd))
        print("-" * 80)

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)

            # Добавляем __init__.py файлы после успешной генерации
            print(f"\n📦 Adding __init__.py files to all subdirectories...")
            add_init_files(output_dir)

            print(
                f"\n✅ Successfully generated gRPC Python code with mypy types in:\n   {output_dir}"
            )
            print("   Generated files include .pyi stubs for better type hinting.")
            print(
                "   Added __init__.py files to all directories for proper Python packaging."
            )

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Generation failed with exit code {e.returncode}")
            if e.stdout:
                print("STDOUT:", e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            sys.exit(1)
        except FileNotFoundError as e:
            print(e)
            print("❌ Error: 'uv' command not found.")
            sys.exit(1)


if __name__ == "__main__":
    main()
