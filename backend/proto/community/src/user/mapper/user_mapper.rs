use crate::user::domain::{UserDomain, Gender, SocialDomain};
use crate::user::persistence::{User, Social as PersistenceSocial};

pub struct UserMapper;

impl UserMapper {
    pub fn domain_to_data(domain: &UserDomain) -> User {
        User {
            id: None,
            email: domain.email.clone(),
            name: domain.name.clone(),
            gender: match domain.gender {
                Gender::Male => "male".to_string(),
                Gender::Female => "female".to_string(),
                Gender::Helicopter => "helicopter".to_string(),
            },
            social: domain.social.iter().map(|s| PersistenceSocial {
                link: s.link.clone(),
                is_hide: s.is_hide,
            }).collect(),
        }
    }

    pub fn data_to_domain(model: User) -> UserDomain {
        UserDomain {
            email: model.email,
            name: model.name,
            gender: match model.gender.as_str() {
                "male" => Gender::Male,
                "female" => Gender::Female,
                "helicopter" => Gender::Helicopter,
                _ => panic!("Invalid gender"),
            },
            social: model.social.into_iter().map(|s| SocialDomain {
                link: s.link,
                is_hide: s.is_hide,
            }).collect(),
        }
    }
}