package akiora.user.domain.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Socials {

    private String link;
    @JsonProperty("isHide")
    private boolean isHide;
}
