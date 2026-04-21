# justfile для управления микросервисами Akiora
# Установка: https://github.com/casey/just
# Использование: just <команда>
set shell := ["powershell.exe", "-c"]
# Переменные
project_root := source_dir()
python_root := project_root + "/backend/python"
proto_build_src := python_root + "/proto-build/src/proto_build"
python_cmd := "uv run python"

# Определяем разделитель в зависимости от ОС (для гибкости)
sep := if os() == "windows" { ";" } else { ":" }

# Экспортируем PYTHONPATH правильно
# Экспортируем PYTHONPATH для всех команд

set export

export PYTHONPATH := proto_build_src + sep + env_var_or_default("PYTHONPATH", "")
# ----------------------------------------------------------------------------
# Основные команды
# ----------------------------------------------------------------------------
# Показать все доступные команды
default:
    @echo "Just thinks PYTHONPATH is: {{PYTHONPATH}}"
    @echo "PowerShell sees PYTHONPATH as: $env:PYTHONPATH"
    @just --list

# Установка зависимостей для всех сервисов
install:
    @echo "🔧 Installing dependencies..."
    cd {{python_root}} && uv sync --all-packages
    @echo "✅ Dependencies installed"

# Обновление зависимостей
update:
    @echo "🔄 Updating dependencies..."
    cd {{python_root}} && uv sync --upgrade
    @echo "✅ Dependencies updated"

# Генерация proto файлов
generate-proto:
    @echo "📦 Generating protobuf files..."
    cd {{python_root}} && uv run python scripts/generate_proto.py
    @echo "✅ Proto files generated"
notification:
    @echo "🚀 Starting Notification Service..."
    cd {{python_root}}/notification ; {{python_cmd}} main.py

# Запустить game сервис
game:
    @echo "🎮 Starting Game Service..."
    cd {{python_root}}/game && {{python_cmd}} main.py

# Запустить user сервис
user:
    @echo "👤 Starting User Service..."
    cd {{python_root}}/user && {{python_cmd}} main.py

# Запустить messenger сервис
messenger:
    @echo "💬 Starting Messenger Service..."
    cd {{python_root}}/messenger && {{python_cmd}} main.py

# Запустить gateway сервис
gateway:
    @echo "🌐 Starting Gateway Service..."
    cd {{python_root}}/gateway && {{python_cmd}} main.py

# Запустить все сервисы (в фоне)
all:
    @echo "🚀 Starting all services..."
    @just --justfile {{justfile()}} notification &
    @just --justfile {{justfile()}} game &
    @just --justfile {{justfile()}} user &
    @just --justfile {{justfile()}} messenger &
    @just --justfile {{justfile()}} gateway &
    @echo "✅ All services started"

