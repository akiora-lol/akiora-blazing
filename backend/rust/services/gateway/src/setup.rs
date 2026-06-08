use redis::Client;
use redis::aio::{ConnectionManager, ConnectionManagerConfig};
use std::error::Error;
use std::time::Duration;
pub async fn setup() -> Result<ConnectionManager, Box<dyn Error>> {
    let client = Client::open("redis://localhost:6379/0")?;

    let config = ConnectionManagerConfig::new()
        .set_min_delay(Duration::from_millis(100)) // минимальная задержка между попытками
        .set_max_delay(Duration::from_secs(5)) // максимальная задержка
        .set_number_of_retries(10) // количество попыток переподключения
        .set_response_timeout(Some(Duration::from_secs(30))) // таймаут ответа
        .set_connection_timeout(Some(Duration::from_secs(5))); // таймаут соединения

    let manager = ConnectionManager::new_with_config(client, config).await?;
    Ok(manager)
}
