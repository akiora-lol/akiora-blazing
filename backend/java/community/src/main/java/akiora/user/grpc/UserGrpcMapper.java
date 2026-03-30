package akiora.user.grpc;

import akiora.user.grpc.proto.Gender;
import akiora.user.grpc.proto.Social;
import akiora.user.grpc.proto.UserRequest;
import akiora.user.grpc.proto.UserResponse;
import akiora.user.rest.model.Socials;
import akiora.user.rest.model.User;
import org.springframework.stereotype.Component;

@Component
public class UserGrpcMapper {

    public User toRestUser(UserRequest req) {
        return User.builder()
                .id(req.getId())
                .email(req.getEmail())
                .name(req.getName())
                .bio(req.getBio())
                .birthday(req.getBirthday())
                .gender(req.getGender() != Gender.HELICOPTER ? toRestGender(req.getGender()) : null)
                .socials(req.getSocialsList().isEmpty() ? null : req.getSocialsList().stream().map(s -> {
                    var social = new Socials();
                    social.setLink(s.getLink());
                    social.setHide(s.getHide());
                    return social;
                }).toList())
                .build();
    }

    public UserResponse toProtoResponse(User u) {
        var builder = UserResponse.newBuilder()
                .setId(nvl(u.getId()))
                .setEmail(nvl(u.getEmail()))
                .setName(nvl(u.getName()))
                .setBio(nvl(u.getBio()))
                .setBirthday(nvl(u.getBirthday()));
        if (u.getGender() != null) {
            builder.setGender(toProtoGender(u.getGender()));
        }
        if (u.getSocials() != null) {
            u.getSocials().forEach(s -> builder.addSocials(
                    Social.newBuilder().setLink(nvl(s.getLink())).setHide(s.isHide()).build()));
        }
        if (u.getGames() != null) {
            builder.addAllGames(u.getGames());
        }
        return builder.build();
    }

    private akiora.user.rest.model.Gender toRestGender(Gender g) {
        return switch (g) {
            case MALE -> akiora.user.rest.model.Gender.MALE;
            case FEMALE -> akiora.user.rest.model.Gender.FEMALE;
            default -> akiora.user.rest.model.Gender.HELICOPTER;
        };
    }

    private Gender toProtoGender(akiora.user.rest.model.Gender g) {
        return switch (g) {
            case MALE -> Gender.MALE;
            case FEMALE -> Gender.FEMALE;
            default -> Gender.HELICOPTER;
        };
    }

    private String nvl(String s) {
        return s == null ? "" : s;
    }
}
