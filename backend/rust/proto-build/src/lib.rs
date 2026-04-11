pub mod common {
    tonic::include_proto!("akiora.common");
}

pub mod game {
    pub mod tournament {

        tonic::include_proto!("akiora.game.tournament");
    }
}
