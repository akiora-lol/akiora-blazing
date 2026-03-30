package akiora.team.grpc;

import akiora.team.grpc.proto.CreateGroupRequest;
import akiora.team.grpc.proto.GetGroupRequest;
import akiora.team.grpc.proto.GroupResponse;
import akiora.team.grpc.proto.GroupServiceGrpc;
import akiora.team.grpc.proto.PatchGroupRequest;
import io.grpc.Status;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;

@GrpcService
public class GroupGrpcService extends GroupServiceGrpc.GroupServiceImplBase {

    @Override
    public void createGroup(CreateGroupRequest request, StreamObserver<GroupResponse> responseObserver) {
        responseObserver.onError(Status.UNIMPLEMENTED.withDescription("Not implemented yet").asRuntimeException());
    }

    @Override
    public void updateGroup(PatchGroupRequest request, StreamObserver<GroupResponse> responseObserver) {
        responseObserver.onError(Status.UNIMPLEMENTED.withDescription("Not implemented yet").asRuntimeException());
    }

    @Override
    public void getGroup(GetGroupRequest request, StreamObserver<GroupResponse> responseObserver) {
        responseObserver.onError(Status.UNIMPLEMENTED.withDescription("Not implemented yet").asRuntimeException());
    }
}
