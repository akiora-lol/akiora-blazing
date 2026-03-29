pub mod domain;
pub mod grpc;
pub mod mapper;
pub mod persistence;
pub mod rest;

pub use domain::GroupDomain;
pub use persistence::repo::MongoGroupRepository;
