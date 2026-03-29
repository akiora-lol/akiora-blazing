// ─── Server ───────────────────────────────────────────────────────────────────
pub const REST_ADDR: &str = "0.0.0.0:8080";
pub const GRPC_ADDR: &str = "[::]:50051";

// ─── MongoDB ──────────────────────────────────────────────────────────────────
pub const MONGO_URL_DEFAULT: &str = "mongodb://admin:password123@localhost:27017";
pub const MONGO_DB_NAME_DEFAULT: &str = "community_db";
pub const MONGO_URL_ENV: &str = "MONGODB_URL";
pub const MONGO_DB_NAME_ENV: &str = "MONGODB_DB_NAME";

// ─── Collections ──────────────────────────────────────────────────────────────
pub const COLLECTION_USERS: &str = "users";

// ─── API routes ───────────────────────────────────────────────────────────────
pub const ROUTE_USERS: &str = "/api/users";
pub const ROUTE_USERS_BY_ID: &str = "/api/users/{id}";
pub const ROUTE_USERS_BY_EMAIL: &str = "/api/users/by-email/{email}";
