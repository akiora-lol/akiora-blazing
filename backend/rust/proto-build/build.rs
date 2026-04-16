use protox::prost::Message;
use std::{env, fs, path::PathBuf};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proto_root = "../../proto";

    // Явно указываем файлы для компиляции
    let proto_files = vec![
        format!("{}/common/types.proto", proto_root),
        format!("{}/common/game_actors.proto", proto_root),
        format!("{}/common/game_settings.proto", proto_root),
        format!("{}/common/game_draft.proto", proto_root),
        format!("{}/game/v1/tournament_service.proto", proto_root),
        format!("{}/game/v1/gameseries_service.proto", proto_root),
    ];

    // Директории, где могут находиться импортируемые файлы
    let proto_dirs = vec![
        proto_root.to_string(),
        format!("{}/game/v1", proto_root),
        format!("{}/common", proto_root),
    ];

    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());

    // Проверяем, что все указанные файлы существуют
    for file in &proto_files {
        if !fs::metadata(file).is_ok() {
            eprintln!("Warning: proto file not found: {}", file);
        }
    }

    let file_descriptors = protox::compile(&proto_files, &proto_dirs)?;
    let fds_path = out_dir.join("file_descriptor_set.bin");
    fs::write(&fds_path, file_descriptors.encode_to_vec())?;

    tonic_prost_build::configure()
        .file_descriptor_set_path(&fds_path)
        .skip_protoc_run()
        .compile_protos(&proto_files, &proto_dirs)?;

    println!("cargo:rerun-if-changed={}", proto_root);
    Ok(())
}
