use crate::domain::models::Game;
use shared::MongoRepository;

pub type GameRepo = MongoRepository<Game>;
