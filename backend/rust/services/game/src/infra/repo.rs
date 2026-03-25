use crate::domain::game::Game;
use shared::MongoRepository;

pub type GameRepo = MongoRepository<Game>;
