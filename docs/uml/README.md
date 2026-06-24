# UML diagrams

Диаграммы подготовлены в формате PlantUML (`.puml`) для включения в диплом и документацию проекта.

## Class diagrams

- `class_service_overview.puml` — обзор сервисов и внешних зависимостей без детализации доменных моделей.
- `class_auth_service.puml` — сервис авторизации, сессии и LoL verification challenge.
- `class_community_service.puml` — пользователи, друзья, клубы, команды и связанные игровые аккаунты.
- `class_search_service.puml` — cold/hot анкеты поиска напарников, роли и ранговые диапазоны.
- `class_tournament_service.puml` — турниры, участники, капитанский драфт игроков и сетка.
- `class_bracket_builders.puml` — builder-слой генерации турнирных сеток.
- `class_draft_service.puml` — игровой champion draft внутри игровой серии.
- `class_messenger_service.puml` — чаты, сообщения, реакции и история сообщений.
- `class_socket_gateway.puml` — WebSocket-соединения и доставка notification_stream.
- `class_gateway_service.puml` — REST gateway, gRPC stubs и публикация событий.
- `class_frontend_app.puml` — структура frontend-приложения: routes, components, contexts, API hooks и DTO.

## Sequence diagrams

- `seq_email_login.puml` — авторизация по email-коду и создание сессии.
- `seq_lol_account_verification.puml` — привязка и подтверждение League of Legends аккаунта.
- `seq_friend_request_realtime.puml` — заявка в друзья с доставкой уведомления через socket gateway.
- `seq_community_update_profile.puml` — обновление профиля пользователя и синхронизация Redis-сессии.
- `seq_community_list_users_profile_preview.puml` — поиск пользователей и открытие мини-превью профиля.
- `seq_community_friends_list.puml` — получение списка друзей с агрегацией профилей.
- `seq_community_club_team_flow.puml` — создание клуба/команды и добавление участника.
- `seq_chat_message_realtime.puml` — отправка сообщения и realtime-обновление чата.
- `seq_tournament_draft_flow.puml` — жизненный цикл DRAFT-турнира от регистрации до сетки.
- `seq_bracket_generation.puml` — генерация турнирной сетки для разных форматов.
- `seq_partner_search_swipe.puml` — просмотр cold deck и swipe-действие в поиске напарников.

Файлы можно открыть в любом PlantUML renderer, IntelliJ plugin, VS Code PlantUML extension или через `plantuml *.puml`.
