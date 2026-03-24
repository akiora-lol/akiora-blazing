use protox::prost::Message;
use std::{env, fs, path::PathBuf};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proto_root = "../../proto";

    let proto_files = find_proto_files(proto_root)?;
    let proto_dirs = find_proto_directories(proto_root)?;

    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());

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

fn find_proto_files(dir: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let mut files = Vec::new();
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_dir() {
            files.extend(find_proto_files(path.to_str().unwrap())?);
        } else if path.extension().and_then(|e| e.to_str()) == Some("proto") {
            files.push(path.to_str().unwrap().to_string());
        }
    }
    Ok(files)
}

fn find_proto_directories(root: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let mut dirs = std::collections::HashSet::new();
    let proto_files = find_proto_files(root)?;

    for file in proto_files {
        if let Some(parent) = PathBuf::from(file).parent() {
            dirs.insert(parent.to_str().unwrap().to_string());
        }
    }

    dirs.insert(root.to_string());

    Ok(dirs.into_iter().collect())
}
