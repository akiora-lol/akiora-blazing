use std::sync::Arc;

use tonic::{Request, Response, Status};

use proto_build::community::user_v1::{
    user_service_server::UserService as UserServiceGrpc,
    CreateUserRequest, Gender as ProtoGender, GetUserRequest, PatchUserRequest,
    Social as ProtoSocial, UserResponse,
};

use crate::user::domain::{Gender, SocialDomain, UserDomain};
use crate::user::domain::user_service::UserService;

pub struct UserGrpcService {
    service: Arc<UserService>,
}

impl UserGrpcService {
    pub fn new(service: Arc<UserService>) -> Self {
        Self { service }
    }
}

fn domain_gender_to_proto(g: &Gender) -> i32 {
    match g {
        Gender::Helicopter => ProtoGender::Helicopter as i32,
        Gender::Male => ProtoGender::Male as i32,
        Gender::Female => ProtoGender::Female as i32,
    }
}

fn proto_gender_to_domain(g: i32) -> Gender {
    match ProtoGender::try_from(g) {
        Ok(ProtoGender::Male) => Gender::Male,
        Ok(ProtoGender::Female) => Gender::Female,
        _ => Gender::Helicopter,
    }
}

fn domain_to_grpc_response(user: UserDomain, bio: String, birthday: String) -> UserResponse {
    UserResponse {
        id: user.id.unwrap_or_default(),
        email: user.email,
        name: user.name,
        bio,
        gender: domain_gender_to_proto(&user.gender),
        birthday,
        socials: user.social.into_iter().map(|s| ProtoSocial { link: s.link, hide: s.is_hide }).collect(),
    }
}

#[tonic::async_trait]
impl UserServiceGrpc for UserGrpcService {
    async fn create_user(
        &self,
        request: Request<CreateUserRequest>,
    ) -> Result<Response<UserResponse>, Status> {
        let req = request.into_inner();
        let user = self
            .service
            .create_user(req.email, req.name, Gender::Helicopter)
            .await
            .map_err(|e| Status::internal(e.to_string()))?;

        Ok(Response::new(domain_to_grpc_response(user, String::new(), String::new())))
    }

    async fn update_user(
        &self,
        request: Request<PatchUserRequest>,
    ) -> Result<Response<UserResponse>, Status> {
        let req = request.into_inner();

        let existing = self
            .service
            .get_user_by_email(&req.email)
            .await
            .map_err(|e| Status::internal(e.to_string()))?
            .ok_or_else(|| Status::not_found("user not found"))?;

        let updated_domain = UserDomain {
            id: existing.id,
            email: existing.email.clone(),
            name: if req.name.is_empty() { existing.name } else { req.name },
            gender: proto_gender_to_domain(req.gender),
            social: req
                .socials
                .into_iter()
                .map(|s| SocialDomain { link: s.link, is_hide: s.hide })
                .collect(),
        };

        let result = self
            .service
            .update_user(&req.email, updated_domain)
            .await
            .map_err(|e| Status::internal(e.to_string()))?
            .ok_or_else(|| Status::not_found("user not found"))?;

        Ok(Response::new(domain_to_grpc_response(result, req.bio, req.birthday)))
    }

    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<UserResponse>, Status> {
        let req = request.into_inner();

        let user = if !req.id.is_empty() {
            self.service.get_user_by_id(&req.id).await
        } else {
            self.service.get_user_by_email(&req.email).await
        }
        .map_err(|e| Status::internal(e.to_string()))?
        .ok_or_else(|| Status::not_found("user not found"))?;

        Ok(Response::new(domain_to_grpc_response(user, String::new(), String::new())))
    }
}
