package akiora.user.domain.model;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class User {

    private String id;
    private String email;
    private String name;
    private String bio;
    private String birthday;
    private Gender gender;
    private List<Socials> socials;
    private List<String> games;
}

