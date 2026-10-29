# Лабораторная работа 1 - агенты JADE

Лабораторная №2 «Торговля книгами»: [инструкция и описание](LAB2.md). Запуск: `mvn -Plab2 compile exec:java`.

Проект запускает три агента на локальной платформе JADE:

- `agenta` (`A.AMain`) каждые 5 секунд отправляет `REQUEST` с содержимым `Ping` агентам `agentb` и `B`;
- `agentb` и `B` (оба `B.BClass`) отвечают на корректный запрос сообщением `INFORM` с содержимым `Pong`.

## Запуск

В терминале из папки проекта выполните:

```powershell
mvn compile exec:java
```

Откроется GUI JADE. В консоли ожидается последовательность сообщений вида:

```text
agenta sent Ping to agentb
agentb received Ping from agenta
agentb sent Pong to agenta
agenta received Pong from agentb
agenta sent Ping to B
B received Ping from agenta
B sent Pong to agenta
agenta received Pong from B
```

Строка агентов для запуска из IDE: `agenta:A.AMain;agentb:B.BClass;B:B.BClass`.

## Наблюдение в Sniffer

1. В окне RMA откройте меню `Tools` и запустите `Sniffer`.
2. В окне Sniffer добавьте в список агентов `agenta`, `agentb` и `B`.
3. Через несколько секунд на диаграмме появятся два запроса `Ping` и два ответа `Pong`.

Порядок стартовых сообщений может отличаться: JADE запускает агентов независимо. Для наблюдения обмена через интерфейс JADE запустите Sniffer и добавьте в него `agenta` и `agentb` до отправки следующего сообщения.
