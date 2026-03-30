package akiora.user.grpc;

import io.grpc.stub.StreamObserver;
import lombok.RequiredArgsConstructor;
import net.devh.boot.grpc.server.service.GrpcService;
import akiora.user.domain.service.UserService;
import akiora.user.grpc.proto.GetUserRequest;
import akiora.user.grpc.proto.UserRequest;
import akiora.user.grpc.proto.UserResponse;
import akiora.user.grpc.proto.UserServiceGrpc;
import akiora.user.mapper.UserMapper;

@GrpcService
@RequiredArgsConstructor
public class UserGrpcService extends UserServiceGrpc.UserServiceImplBase {

    private final UserService userService;
    private final UserMapper userMapper;
    private final UserGrpcMapper grpcMapper;

    @Override
    public void createUser(UserRequest request, StreamObserver<UserResponse> responseObserver) {
        var result = userService.createUser(userMapper.restToDomain(grpcMapper.toRestUser(request)));
        responseObserver.onNext(grpcMapper.toProtoResponse(userMapper.domainToRest(result)));
        responseObserver.onCompleted();
    }

    @Override
    public void updateUser(UserRequest request, StreamObserver<UserResponse> responseObserver) {
        var result = userService.updateUser(userMapper.restToDomain(grpcMapper.toRestUser(request)));
        responseObserver.onNext(grpcMapper.toProtoResponse(userMapper.domainToRest(result)));
        responseObserver.onCompleted();
    }

    @Override
    public void getUser(GetUserRequest request, StreamObserver<UserResponse> responseObserver) {
        var domain = request.getId().isBlank()
                ? userService.getUserByEmail(request.getEmail())
                : userService.getUserById(request.getId());
        responseObserver.onNext(grpcMapper.toProtoResponse(userMapper.domainToRest(domain)));
        responseObserver.onCompleted();
    }
}
