pub mod community {
    pub mod user_v1 {

        tonic::include_proto!("akiora.community.user");
    }
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
