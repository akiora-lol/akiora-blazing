package akiora.user.domain.service;

import lombok.RequiredArgsConstructor;
import akiora.user.domain.model.User;
import akiora.user.mapper.UserMapper;
import akiora.user.persistence.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

import static akiora.Constant.LEAGUE_OF_LEGENDS;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper mapper;

    public User createUser(User user) {
        var dataUser = mapper.domainToData(user);
        dataUser.setGames(List.of(LEAGUE_OF_LEGENDS));
        return mapper.dataToDomain(userRepository.save(dataUser));
    }

    public User updateUser(User user) {
        checkUserExistsById(user.getId());
        var dataUser = mapper.domainToData(user);
        dataUser.setGames(List.of(LEAGUE_OF_LEGENDS));
        return mapper.dataToDomain(userRepository.save(dataUser));
    }

    public User getUserById(String id) {
        return mapper.dataToDomain(userRepository.findById(id).get());
    }

    public User getUserByEmail(String email) {
        return mapper.dataToDomain(userRepository.findByEmail(email));
    }

    public User deleteUserById(String id) {
        var user = getUserById(id);
        userRepository.deleteById(id);
        return user;
    }

    private void checkUserExistsById(String id) {
        userRepository.findById(id).orElseThrow();
    }
}
