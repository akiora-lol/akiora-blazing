package akiora.user.rest.model.request;

import com.fasterxml.jackson.annotation.JsonAlias;
import lombok.Getter;
import lombok.Setter;
import akiora.user.rest.model.User;

@Getter
@Setter
public class UserRequest {

    @JsonAlias("UserRequest")
    private User user;
}
