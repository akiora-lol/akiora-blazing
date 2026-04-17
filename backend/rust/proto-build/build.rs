const PROTO_FILES: &[&str] = &[
    "D:/Dev/akiora-blazing/backend/proto/game/v1/tournament_service.proto",
    "D:/Dev/akiora-blazing/backend/proto/game/v1/gameseries_service.proto",
];

const PROTO_INCLUDES: &[&str] = &[
    "D:/Dev/akiora-blazing/backend/proto",
    "D:/Dev/akiora-blazing/backend/proto/googleapis",
];

fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_prost_build::configure()
        .build_client(true)
        .build_server(false)
        .type_attribute(".", "#[derive(serde::Serialize, serde::Deserialize)] #[serde(rename_all = \"camelCase\")]")
        .compile_protos(PROTO_FILES, PROTO_INCLUDES)?;
    Ok(())
}
