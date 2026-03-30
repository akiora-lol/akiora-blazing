package akiora.user.rest.controller;

import lombok.RequiredArgsConstructor;
import akiora.user.domain.service.UserService;
import akiora.user.mapper.UserMapper;
import akiora.user.rest.model.request.UserRequest;
import akiora.user.rest.model.response.UserResponse;
import org.springframework.web.bind.annotation.*;

@RequestMapping("/v1/users")
@RestController
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final UserMapper userMapper;

    @PostMapping
    public UserResponse createUser(@RequestBody UserRequest userRequest) {
        var restUser = userMapper.restToDomain(userRequest.getUser());
        return new UserResponse(userMapper.domainToRest(userService.createUser(restUser)));
    }

    @GetMapping("/{id}")
    public UserResponse getUserById(@PathVariable("id") String id) {
        return new UserResponse(userMapper.domainToRest(userService.getUserById(id)));
    }

    @GetMapping("/by-email/{email}")
    public UserResponse getUserByEmail(@PathVariable("email") String email) {
        return new UserResponse(userMapper.domainToRest(userService.getUserByEmail(email)));
    }

    @DeleteMapping("/{id}")
    public UserResponse deleteUserById(@PathVariable("id") String id) {
        return new UserResponse(userMapper.domainToRest(userService.deleteUserById(id)));
    }

    @PatchMapping
    public UserResponse updateUser(@RequestBody UserRequest userRequest) {
        var restUser = userMapper.restToDomain(userRequest.getUser());
        return new UserResponse(userMapper.domainToRest(userService.updateUser(restUser)));
    }
}
