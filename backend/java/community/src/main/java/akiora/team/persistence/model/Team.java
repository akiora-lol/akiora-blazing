package akiora.team.persistence.model;

import lombok.Getter;
import lombok.Setter;
import akiora.user.persistence.model.User;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Getter
@Setter
@Document("teams")
public class Team {

    private List<User> users;
}
