package akiora.user.rest.model.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import akiora.user.rest.model.User;

@Getter
@Setter
@Builder
@AllArgsConstructor
public class UserResponse {

    private User user;
}


