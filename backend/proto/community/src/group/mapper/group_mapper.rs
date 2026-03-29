use crate::group::domain::GroupDomain;
use crate::group::persistence::Group;

pub struct GroupMapper;

impl GroupMapper {
    pub fn domain_to_data(domain: &GroupDomain) -> Group {
        Group {
            id: domain
                .id
                .as_deref()
                .and_then(|s| bson::oid::ObjectId::parse_str(s).ok()),
            owner_id: domain.owner_id.clone(),
            name: domain.name.clone(),
            members: domain.members.clone(),
        }
    }

    pub fn data_to_domain(model: Group) -> GroupDomain {
        GroupDomain {
            id: model.id.map(|oid| oid.to_hex()),
            owner_id: model.owner_id,
            name: model.name,
            members: model.members,
        }
    }
}
