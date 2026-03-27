mod user;

use mongodb::Client;
use user::{UserDomain, Gender, UserMapper, UserRepository};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    println!("=== User Mapper with MongoDB Example ===\n");

    // 1. Подключаемся к MongoDB
    let mongo_url = "mongodb://admin:password123@localhost:27017";
    let client = Client::with_uri_str(mongo_url).await?;
    let database = client.database("community_db");

    // 2. Создаем репозиторий
    let repository = UserRepository::new(&database).await;

    // 3. Создаем доменного пользователя
    let mut user_domain = UserDomain::new(
        String::from("alice@example.com"),
        String::from("Alice"),
        Gender::Female,
    );

    user_domain.add_social(String::from("https://twitter.com/alice"), false);
    user_domain.add_social(String::from("https://instagram.com/alice"), false);
    user_domain.add_social(String::from("https://facebook.com/alice"), true);

    println!("📦 Domain user created: {:?}\n", user_domain);

    // 4. Маппим в модель для БД (убрали mut)
    let user_model = UserMapper::domain_to_data(&user_domain);
    println!("🔄 Mapped to persistence model: {:?}\n", user_model);

    // 5. Сохраняем в MongoDB
    let insert_result = repository.save(user_model.clone()).await?;
    println!("💾 Saved to MongoDB with ID: {:?}\n", insert_result.inserted_id);

    // 6. Ищем по email
    let found = repository.find_by_email("alice@example.com").await?;
    if let Some(found_user) = found {
        println!("🔍 Found by email: {:?}\n", found_user);

        // 7. Обратный маппинг в домен
        let recovered_domain = UserMapper::data_to_domain(found_user);
        println!("🔄 Mapped back to domain: {:?}\n", recovered_domain);
    }

    // 8. Показываем всех пользователей
    let all_users = repository.find_all().await?;
    println!("📋 All users in database: {} total", all_users.len());
    for user in all_users {
        println!("   - {} ({})", user.name, user.email);
    }

    println!("\n✅ Success!");
    Ok(())
}