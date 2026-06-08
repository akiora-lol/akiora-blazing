# Akiora Backend Architecture

Многосервисная архитектура на Python с gRPC для межсервисной коммуникации и FastAPI для REST API.

## Структура проекта

```
backend/python/
├── proto-build/          # Сгенерированные Python файлы из .proto
├── stubs/                # Клиентские стабы для взаимодействия с сервисами
├── shared/               # Общие контракты и утилиты (Pydantic модели)
├── gateway/              # API Gateway (FastAPI) - точка входа
├── auth/                 # Сервис аутентификации
├── community/            # Сервис сообщества (users, clubs, teams, groups)
├── messenger/            # Сервис сообщений и чатов
├── game/                 # Сервис игр (tournaments, game series)
├── draft/                # Сервис драфта
├── search/               # Сервис поиска
├── notification/         # Сервис уведомлений
└── main.py               # Скрипт генерации gRPC кода
```

## Сервисы

### Gateway (REST API)
- **Порт**: 8000
- **Технология**: FastAPI + Granian
- **Назначение**: Точка входа для всех REST запросов
- **Маршруты**:
  - `/users/*` - пользователи (Community service)
  - `/clubs/*` - клубы (Community service)
  - `/teams/*` - команды (Community service)
  - `/groups/*` - группы (Community service)
  - `/chats/*`, `/messages/*` - мессенджер (Messenger service)
  - `/tournaments/*`, `/gameseries/*` - игры (Game service)

**IoC контейнер**: Dishka для управления зависимостями

### Community Service
- **Ответственность**: Управление пользователями, клубами, командами, группами
- **БД**: MongoDB (Beanie ORM)
- **Структура**:
  ```
  domain/
  ├── entities/       # Beanie модели (User, Club, Team, Group)
  └── services/       # Бизнес-логика (UserService, ClubService, etc.)
  ```
- **Стаб**: `stubs/club_stub.py`, `stubs/team_stub.py`, `stubs/group_stub.py`, `stubs/user_stub.py`

### Messenger Service
- **Ответственность**: Чаты, сообщения, реакции, уведомления о прочтении
- **БД**: Redis (для кеша сообщений и статусов)
- **Структура**:
  ```
  domain/
  ├── entities/       # Chat, Message модели
  └── services/       # ChatService, MessageService
  ```
- **Стаб**: `stubs/messenger_stub.py`
- **IoC**: Использует RedisManager для управления подключениями

### Game Service
- **Ответственность**: Турниры, игровые серии, драфты
- **БД**: MongoDB
- **Структура**:
  ```
  domain/
  ├── entities/       # Tournament, GameSeries сущности
  ├── services/       # Бизнес-логика
  └── value_objects/  # Значимые объекты
  community/          # Взаимодействие с Community service
  ```
- **Стабы**: `stubs/tournament_stub.py`, `stubs/gameseries_stub.py`

### Auth Service
- **Ответственность**: OAuth, сессии
- **Структура**:
  ```
  domain/
  ├── auth_service.py      # Логика аутентификации
  ├── session_service.py   # Управление сессиями
  └── session_repo.py      # Репозиторий сессий
  ```

### Search Service
- **Статус**: Заготовка (domain структура создана)

### Draft Service
- **Структура**: Простая архитектура с моделями и сервисом
- **Файлы**: `draft_model.py`, `draft_service.py`, `draft_schemas.py`

### Notification Service
- **Статус**: Заготовка

## Proto файлы (../proto)

Protobuf файлы определяют gRPC сервисы и сообщения:

### Community сервис
- `community/user/v1/user_service.proto`
- `community/club/v1/club_service.proto`
- `community/team/v1/team_service.proto`
- `community/group/v1/group_service.proto`

### Game сервис
- `game/v1/tournament_service.proto`
- `game/v1/gameseries_service.proto`
- `common/game_actors.proto` - типы участников игры
- `common/game_draft.proto` - драфт правила
- `common/game_settings.proto` - настройки игры
- `common/types.proto` - общие типы

### Messenger сервис
- `messenger/v1/messenger_service.proto`

### Генерация кода
**Скрипт**: `main.py`
```bash
uv run python main.py
```

**Процесс**:
1. Находит все `.proto` файлы в `../proto` (исключает googleapis)
2. Генерирует Python код с помощью `grpc_tools.protoc`:
   - `*_pb2.py` - сообщения
   - `*_pb2_grpc.py` - сервисные классы
   - `*.pyi` - type hints для mypy
3. Добавляет `__init__.py` во все директории
4. Выходная папка: `proto-build/src/proto_build/`

## Shared - Общие контракты

**Назначение**: Pydantic модели для взаимодействия между сервисами

**Структура**: `shared/src/shared/contracts/`
- `messenger.py` - Пydantic модели для Messenger (ChatResponse, MessageResponse и т.д.)
- `club.py` - Модели Club сервиса
- `team.py` - Модели Team сервиса
- `group.py` - Модели Group сервиса
- `tournament.py` - Модели Game сервиса (Tournament)
- `gameseries.py` - Модели GameSeries
- `auth.py` - Auth модели
- `draft/` - Draft модели

## Стабы (Stubs)

**Назначение**: Клиентские оберки для вызова сервисов через gRPC

**Архитектура каждого стаба**:
1. **Mapper класс** - преобразует между Pydantic моделями и protobuf сообщениями
   ```python
   class MessengerMapper:
       # Словари маппингов enum значений
       CHAT_OWNER_TYPE_MAP = {0: ChatOwnerType.OWNER_UNSPECIFIED, ...}
       CHAT_OWNER_TYPE_TO_PROTO = {v: k for k, v in CHAT_OWNER_TYPE_MAP.items()}
       
       @classmethod
       def to_pydantic_chat_response(cls, grpc_response) -> ChatResponse:
           # Преобразует protobuf -> Pydantic
   ```

2. **Service stub класс** - выполняет RPC вызовы
   ```python
   class MessengerStub:
       def __init__(self, channel: grpc.aio.Channel):
           self.stub = pb2_grpc_module.MessengerServiceStub(channel)
       
       async def create_chat(self, request: CreateChatRequest) -> ChatResponse:
           # Маппирует Pydantic -> protobuf
           # Выполняет RPC вызов
           # Маппирует обратно protobuf -> Pydantic
   ```

**Примеры**:
- `stubs/messenger_stub.py` - самый полный пример (~200+ строк)
- `stubs/club_stub.py` - Community stub
- `stubs/user_stub.py` - User stub
- `stubs/team_stub.py` - Team stub
- `stubs/tournament_stub.py` - Tournament stub
- `stubs/gameseries_stub.py` - GameSeries stub
- `stubs/group_stub.py` - Group stub

**Важные нюансы**:
1. **Mappers хранят двусторонние маппинги**:
   - `*_MAP` (int -> enum) для десериализации protobuf → Pydantic
   - `*_TO_PROTO` (enum -> int) для сериализации Pydantic → protobuf
   
2. **Обработка nested структур**:
   ```python
   # Пример из messenger_stub.py
   allowed_users=list(grpc_response.allowed_users),  # list() конвертирует protobuf repeated
   ```

3. **UUID обработка**:
   ```python
   id=UUID(grpc_response.id)  # String из protobuf → UUID объект
   ```

4. **Default значения**:
   ```python
   cls.*_MAP.get(grpc_response.field, DefaultValue.UNSPECIFIED)
   ```

5. **Асинхронные вызовы**:
   ```python
   response = await self.stub.CreateChat(pb_request)  # await для async gRPC
   ```

## IoC контейнеры (Dishka)

**Структура**: Каждый сервис имеет свой `ioc.py`

**Типичная структура**:
```python
class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(self) -> UserService:
        return UserService()

container = make_async_container(ConfigProvider(), DomainProvider())
```

**Scopes**:
- `Scope.APP` - синглтон на весь жизненный цикл приложения (Settings, Redis connections)
- `Scope.REQUEST` - создается для каждого запроса

**Примеры из сервисов**:
- `community/ioc.py` - Settings, UserService, ClubService, TeamService
- `messenger/ioc.py` - ConfigProvider, InfraProvider (Redis), DomainProvider
- `auth/ioc.py` - AuthService, SessionService

## Особенности интеграции

### Gateway ↔ Сервисы
1. **gRPC каналы**: Создаются в dependencies.py Gateway
2. **Стабы**: Используются в route handlers для вызова сервисов
3. **Преобразование**: Pydantic контракты ↔ gRPC ↔ Pydantic

### Пример потока данных:
```
REST запрос (Pydantic)
    ↓
Gateway route handler
    ↓
Стаб (Pydantic → protobuf)
    ↓
gRPC вызов
    ↓
Community service
    ↓
Beanie сущность ↔ MongoDB
    ↓
Результат (protobuf)
    ↓
Стаб (protobuf → Pydantic)
    ↓
REST ответ (Pydantic)
```

## Зависимости (pyproject.toml)

- **FastAPI/Granian** - REST API
- **gRPC** - межсервисная коммуникация
- **Beanie** - ODM для MongoDB
- **Pydantic** - валидация и сериализация данных
- **Dishka** - IoC контейнер
- **Redis** - кеширование (messenger service)
- **FastStream** - async stream processing
- **Loguru** - логирование

## Рабочий процесс разработки

1. **Изменения в proto файлах**:
   - Редактировать файл в `../proto/`
   - Запустить `python main.py` для регенерации кода
   - Обновить Mapper и Stub классы в `stubs/`

2. **Добавление нового сервиса**:
   - Создать папку сервиса
   - Добавить `domain/` структуру
   - Написать `ioc.py` для DI
   - Создать `main.py` entry point
   - Создать стаб в `stubs/`
   - Обновить `shared/contracts/` если нужны новые контракты

3. **Добавление endpoints в Gateway**:
   - Создать `routes/<entity>.py`
   - Использовать соответствующий стаб для вызова сервиса
   - Добавить router в `gateway/main.py`
