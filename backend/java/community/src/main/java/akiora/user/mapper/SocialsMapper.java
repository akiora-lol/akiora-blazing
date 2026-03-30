package akiora.user.mapper;

import akiora.user.persistence.model.Socials;
import akiora.config.MapStructConfig;
import org.mapstruct.Mapper;

@Mapper(config = MapStructConfig.class)
public interface SocialsMapper {

    Socials dataToDomain(Socials socials);

    Socials domainToData(Socials socials);

    Socials restToDomain(akiora.user.rest.model.Socials socials);

    akiora.user.rest.model.Socials domainToRest(Socials socials);
}
