package akiora.user.persistence.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Getter
@Setter
@Document("users")
public class User {

    @Id
    private String id;
    @Indexed(unique = true)
    private String email;
    private String name;
    private String bio;
    private String birthday;
    private String gender;
    private List<Socials> socials;
    private List<String> games;
}

