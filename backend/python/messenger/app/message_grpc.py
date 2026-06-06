import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject

from messenger.v1.messenger_service_pb2 import (
    AddReactionRequest,
    DeleteMessageRequest,
    GetMessageHistoryRequest,
    GetMessageRequest,
    GetReactionsRequest,
    GetUnreadCountRequest,
    GetUserMessagesRequest,
    ListMessagesRequest,
    ListMessagesResponse,
    MarkAsReadRequest,
    MessageResponse,
    MessageShortProto,
    ReactionProto,
    RemoveReactionRequest,
    SendMessageRequest,
    UpdateMessageRequest,
    MessageStatus,
)
from messenger.v1.messenger_service_pb2_grpc import MessageServiceServicer
from common.types_pb2 import Empty

from domain.services.message import MessageService
from domain.entities.message import Message


_MESSAGE_STATUS_REVERSE = {
    "sent": MessageStatus.SENT,
    "read": MessageStatus.READ,
}


def _message_to_proto(msg: Message) -> MessageResponse:
    return MessageResponse(
        id=str(msg.id),
        chat_id=str(msg.chat_id),
        creator_id=str(msg.creator_id),
        body=msg.body,
        status=_MESSAGE_STATUS_REVERSE.get(msg.status, MessageStatus.SENT),
        read_by=[str(u) for u in msg.read_by],
        timestamp=int(msg.timestamp.timestamp()),
        history=[
            MessageShortProto(body=h.body, timestamp=int(h.timestamp.timestamp()))
            for h in msg.history
        ],
        reply_to=str(msg.reply_to) if msg.reply_to else None,
        reactions=[
            ReactionProto(emote_id=r.emote_id, user_id=r.user_id)
            for r in msg.reactions
        ],
        spoiler=msg.spoiler,
    )


class MessageGrpc(MessageServiceServicer):
    @inject
    async def SendMessage(
        self,
        request: SendMessageRequest,
        context: grpc.aio.ServicerContext,
    ) -> MessageResponse:
        reply_to = UUID(request.reply_to) if request.HasField("reply_to") else None
        msg = await MessageService.create_message(
            chat_id=UUID(request.chat_id),
            creator_id=UUID(request.creator_id),
            body=request.body,
            reply_to=reply_to,
            spoiler=request.spoiler,
        )
        return _message_to_proto(msg)

    @inject
    async def ListMessages(
        self,
        request: ListMessagesRequest,
        context: grpc.aio.ServicerContext,
    ) -> ListMessagesResponse:
        limit = request.pagination.page_size if request.HasField("pagination") else 50
        before_ts = (
            request.pagination.before_timestamp
            if request.HasField("pagination") and request.pagination.before_timestamp
            else None
        )
        messages = await MessageService.get_messages(
            chat_id=UUID(request.chat_id),
            limit=limit,
            before_timestamp=before_ts,
        )
        if request.HasField("filter"):
            if request.filter.creator_id:
                creator_id = UUID(request.filter.creator_id)
                messages = [message for message in messages if message.creator_id == creator_id]
            if request.filter.status:
                status = "read" if request.filter.status == MessageStatus.READ else "sent"
                messages = [message for message in messages if message.status == status]
            if request.filter.has_reactions:
                messages = [message for message in messages if message.reactions]
        return ListMessagesResponse(
            messages=[_message_to_proto(message) for message in messages],
            total_count=len(messages),
        )

    @inject
    async def GetMessage(
        self,
        request: GetMessageRequest,
        context: grpc.aio.ServicerContext,
    ) -> MessageResponse:
        message = await Message.get(UUID(request.message_id))
        if not message:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Message not found")
        return _message_to_proto(message)

    @inject
    async def UpdateMessage(
        self,
        request: UpdateMessageRequest,
        context: grpc.aio.ServicerContext,
    ) -> MessageResponse:
        msg = await MessageService.update_message(
            message_id=UUID(request.message_id),
            new_body=request.new_body,
            editor_id=UUID(request.editor_id),
        )
        return _message_to_proto(msg)

    @inject
    async def DeleteMessage(
        self,
        request: DeleteMessageRequest,
        context: grpc.aio.ServicerContext,
    ) -> Empty:
        await MessageService.delete_message(
            message_id=UUID(request.message_id),
            deleter_id=UUID(request.deleter_id),
        )
        return Empty()

    @inject
    async def MarkAsRead(
        self,
        request: MarkAsReadRequest,
        context: grpc.aio.ServicerContext,
    ) -> MessageResponse:
        msg = await MessageService.mark_as_read(
            message_id=UUID(request.message_id),
            user_id=UUID(request.user_id),
        )
        return _message_to_proto(msg)

    @inject
    async def AddReaction(
        self,
        request: AddReactionRequest,
        context: grpc.aio.ServicerContext,
    ) -> MessageResponse:
        msg = await MessageService.add_reaction(
            message_id=UUID(request.message_id),
            user_id=UUID(request.user_id),
            emote_id=request.emote_id,
        )
        return _message_to_proto(msg)

    @inject
    async def RemoveReaction(
        self,
        request: RemoveReactionRequest,
        context: grpc.aio.ServicerContext,
    ) -> MessageResponse:
        msg = await MessageService.remove_reaction(
            message_id=UUID(request.message_id),
            user_id=UUID(request.user_id),
            emote_id=request.emote_id,
        )
        return _message_to_proto(msg)

    @inject
    async def GetUnreadCount(
        self,
        request: GetUnreadCountRequest,
        context: grpc.aio.ServicerContext,
    ):
        from messenger.v1 import messenger_service_pb2 as pb2
        user_id = UUID(request.user_id)
        messages = await Message.find(Message.chat_id == UUID(request.chat_id)).to_list()
        return pb2.GetUnreadCountResponse(
            count=len([message for message in messages if user_id not in message.read_by])
        )

    @inject
    async def GetReactions(
        self,
        request: GetReactionsRequest,
        context: grpc.aio.ServicerContext,
    ):
        from messenger.v1 import messenger_service_pb2 as pb2
        message = await Message.get(UUID(request.message_id))
        if not message:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Message not found")
        return pb2.GetReactionsResponse(
            reactions=[
                ReactionProto(emote_id=reaction.emote_id, user_id=reaction.user_id)
                for reaction in message.reactions
            ]
        )

    @inject
    async def GetMessageHistory(
        self,
        request: GetMessageHistoryRequest,
        context: grpc.aio.ServicerContext,
    ) -> ListMessagesResponse:
        message = await Message.get(UUID(request.message_id))
        if not message:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Message not found")
        return ListMessagesResponse(messages=[_message_to_proto(message)], total_count=1)

    @inject
    async def GetUserMessages(
        self,
        request: GetUserMessagesRequest,
        context: grpc.aio.ServicerContext,
    ) -> ListMessagesResponse:
        query = Message.find(Message.creator_id == UUID(request.user_id))
        if request.HasField("chat_id"):
            query = query.find(Message.chat_id == UUID(request.chat_id))
        limit = request.pagination.page_size if request.HasField("pagination") else 50
        messages = await query.sort(-Message.timestamp).limit(limit).to_list()
        return ListMessagesResponse(
            messages=[_message_to_proto(message) for message in messages],
            total_count=len(messages),
        )
