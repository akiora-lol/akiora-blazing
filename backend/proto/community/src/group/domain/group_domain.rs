#[derive(Debug, Clone)]
pub struct GroupDomain {
    pub id: Option<String>,
    pub owner_id: String,
    pub name: String,
    /// All members including the owner
    pub members: Vec<String>,
}

impl GroupDomain {
    pub fn new(owner_id: String, name: String) -> Self {
        Self {
            id: None,
            members: vec![owner_id.clone()],
            owner_id,
            name,
        }
    }
}
