use std::{env, fs, path::PathBuf};

use protox::prost::Message;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proto_dir = "../../proto";
    let proto_file = format!("{}/community/user/v1/user_service.proto", proto_dir);

    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());

    let file_descriptors = protox::compile([&proto_file], [proto_dir])?;
    let fds_path = out_dir.join("file_descriptor_set.bin");
    fs::write(&fds_path, file_descriptors.encode_to_vec())?;

    tonic_prost_build::configure()
        .file_descriptor_set_path(&fds_path)
        .skip_protoc_run()
        .compile_protos(&[&proto_file], &[&proto_dir.to_string()])?;

    println!("cargo:rerun-if-changed={}", proto_dir);
    Ok(())
}
