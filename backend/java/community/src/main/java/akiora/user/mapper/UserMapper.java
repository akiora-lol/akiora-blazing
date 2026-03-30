package akiora.user.mapper;

import akiora.user.persistence.model.User;
import akiora.config.MapStructConfig;
import org.mapstruct.Mapper;

@Mapper(config = MapStructConfig.class, uses = SocialsMapper.class)
public interface UserMapper {

    akiora.user.domain.model.User dataToDomain(User user);

    User domainToData(akiora.user.domain.model.User user);

    akiora.user.domain.model.User restToDomain(akiora.user.rest.model.User user);

    akiora.user.rest.model.User domainToRest(akiora.user.domain.model.User user);
}
