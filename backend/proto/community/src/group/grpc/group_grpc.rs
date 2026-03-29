use std::sync::Arc;

use tonic::{Request, Response, Status};

use proto_build::community::group_v1::{
    group_service_server::GroupService as GroupServiceGrpc,
    CreateGroupRequest, GetGroupRequest, GroupResponse, PatchGroupRequest,
};

use crate::group::domain::group_domain::GroupDomain;
use crate::group::domain::group_service::GroupService;

pub struct GroupGrpcService {
    service: Arc<GroupService>,
}

impl GroupGrpcService {
    pub fn new(service: Arc<GroupService>) -> Self {
        Self { service }
    }
}

fn to_grpc_response(g: GroupDomain) -> GroupResponse {
    GroupResponse {
        id: g.id.unwrap_or_default(),
        owner_id: g.owner_id,
        name: g.name,
        users: g.members,
    }
}

#[tonic::async_trait]
impl GroupServiceGrpc for GroupGrpcService {
    async fn create_group(
        &self,
        request: Request<CreateGroupRequest>,
    ) -> Result<Response<GroupResponse>, Status> {
        let req = request.into_inner();
        let group = self
            .service
            .create_group(req.owner_id, req.name)
            .await
            .map_err(|e| Status::invalid_argument(e.to_string()))?;
        Ok(Response::new(to_grpc_response(group)))
    }

    /// PatchGroupRequest identifies the group by the current `owner_id`.
    async fn update_group(
        &self,
        request: Request<PatchGroupRequest>,
    ) -> Result<Response<GroupResponse>, Status> {
        let req = request.into_inner();
        let new_name = if req.name.is_empty() { None } else { Some(req.name) };
        let group = self
            .service
            .update_group_by_owner(&req.owner_id, new_name, req.add_users, req.delete_users)
            .await
            .map_err(|e| Status::invalid_argument(e.to_string()))?
            .ok_or_else(|| Status::not_found("group not found"))?;
        Ok(Response::new(to_grpc_response(group)))
    }

    async fn get_group(
        &self,
        request: Request<GetGroupRequest>,
    ) -> Result<Response<GroupResponse>, Status> {
        let req = request.into_inner();
        let group = self
            .service
            .get_group(&req.id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?
            .ok_or_else(|| Status::not_found("group not found"))?;
        Ok(Response::new(to_grpc_response(group)))
    }
}
