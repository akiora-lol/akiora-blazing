pub mod community {
    pub mod user_v1 {
        tonic::include_proto!("akiora.community.user");
    }
    pub mod club_v1 {
        tonic::include_proto!("akiora.community.club");
    }
    pub mod group_v1 {
        tonic::include_proto!("akiora.community.group");
    }
}
