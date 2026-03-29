pub mod common {
    tonic::include_proto!("akiora.common");
}
pub mod game {
    pub mod gameseries {
        tonic::include_proto!("akiora.game.gameseries");
    }

    pub mod game {
        tonic::include_proto!("akiora.game.game");
    }

    pub mod tournament {
        tonic::include_proto!("akiora.game.tournament");
    }
}
