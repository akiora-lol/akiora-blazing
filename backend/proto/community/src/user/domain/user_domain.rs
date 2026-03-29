#[derive(Debug, Clone)]
pub struct UserDomain {
    pub id: Option<String>,
    pub email: String,
    pub name: String,
    pub gender: Gender,
    pub social: Vec<SocialDomain>,
}

#[derive(Debug, Clone, Copy)]
pub enum Gender {
    Male,
    Female,
    Helicopter,
}

#[derive(Debug, Clone)]
pub struct SocialDomain {
    pub link: String,
    pub is_hide: bool,
}

impl UserDomain {
    pub fn new(email: String, name: String, gender: Gender) -> Self {
        Self {
            id: None,
            email,
            name,
            gender,
            social: Vec::new(),
        }
    }

    pub fn add_social(&mut self, link: String, is_hide: bool) {
        self.social.push(SocialDomain { link, is_hide });
    }
}

impl SocialDomain {
    pub fn new(link: String, is_hide: bool) -> Self {
        Self { link, is_hide }
    }
}