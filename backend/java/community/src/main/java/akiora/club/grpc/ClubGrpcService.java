package akiora.club.grpc;

import akiora.club.grpc.proto.ClubResponse;
import akiora.club.grpc.proto.ClubServiceGrpc;
import akiora.club.grpc.proto.CreateClubRequest;
import akiora.club.grpc.proto.GetClubRequest;
import akiora.club.grpc.proto.PatchClubRequest;
import io.grpc.Status;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;

@GrpcService
public class ClubGrpcService extends ClubServiceGrpc.ClubServiceImplBase {

    @Override
    public void createClub(CreateClubRequest request, StreamObserver<ClubResponse> responseObserver) {
        responseObserver.onError(Status.UNIMPLEMENTED.withDescription("Not implemented yet").asRuntimeException());
    }

    @Override
    public void updateClub(PatchClubRequest request, StreamObserver<ClubResponse> responseObserver) {
        responseObserver.onError(Status.UNIMPLEMENTED.withDescription("Not implemented yet").asRuntimeException());
    }

    @Override
    public void getClub(GetClubRequest request, StreamObserver<ClubResponse> responseObserver) {
        responseObserver.onError(Status.UNIMPLEMENTED.withDescription("Not implemented yet").asRuntimeException());
    }
}
