from .network import QiNetwork
from typing import Union
import random

class QiUpdater(object):
    def __init__(self, Auth, Key, UpdateResult, UseFakeUserAgent: bool = True, Proxy = None) -> None:
        self.auth = str(Auth)
        self.key = str(Key)
        self.UpResult = UpdateResult
        self.ufa = UseFakeUserAgent
        self.proxy = Proxy
        self.networkClient = QiNetwork(self.auth, self.key, self.proxy)
    
    @property
    def status(self) -> str:
        return self.UpResult['status'] if "status" in self.UpResult.keys() else "Null"

    @property
    def status_det(self) -> str:
        return self.UpResult['status_det']if "status_det" in self.UpResult.keys() else "Null"
    
    @property
    def data(self) -> dict:
        return self.UpResult['data'] if "data" in self.UpResult.keys() else "Null"
    
    @property
    def chats(self) -> list:
        return self.data['chats'] if type(self.data) == dict and "chats" in self.data.keys() else "Null"
    
    @property
    def getLastChat(self) -> dict:
        return self.chats[0] if type(self.data) == dict and "chats" in self.data.keys() else "Null"
    
    @property
    def lastChat(self) -> dict:
        return self.chats[0] if type(self.data) == dict and "chats" in self.data.keys() else "Null"

    @property
    def newState(self) -> int:
        return self.data['new_state'] if type(self.data) == dict and 'new_state' in self.data.keys() else "Null"
    
    @property
    def timeStamp(self) -> str:
        return self.data['time_stamp'] if type(self.data) == dict and 'time_stamp' in self.data.keys() else "Null"
    
    @property
    def objectGuid(self) -> str:
        return self.getLastChat['object_guid'] if type(self.getLastChat) == dict and 'object_guid' in self.getLastChat.keys() else "Null"
    
    @property
    def chatId(self) -> str:
        return self.getLastChat['object_guid'] if type(self.getLastChat) == dict and 'object_guid' in self.getLastChat.keys() else "Null"
    
    @property
    def access(self) -> list:
        return self.getLastChat['access'] if type(self.getLastChat) == dict and 'access' in self.getLastChat.keys() else "Null"
    
    @property
    def countUnseen(self) -> int:
        return self.getLastChat['count_unseen'] if type(self.getLastChat) == dict and 'count_unseen' in self.getLastChat.keys() else "Null"
    
    @property
    def isMute(self) -> bool:
        return self.getLastChat['is_mute'] if type(self.getLastChat) == dict and 'is_mute' in self.getLastChat.keys() else "Null"
    
    @property
    def isPinned(self) -> bool:
        return self.getLastChat['is_pinned'] if type(self.getLastChat) == dict and 'is_pinned' in self.getLastChat.keys() else "Null"
    
    @property
    def getLastMessage(self) -> dict:
        return self.getLastChat['last_message'] if type(self.getLastChat) == dict and 'last_message' in self.getLastChat.keys() else "Null"
    
    @property
    def lastMessage(self) -> dict:
        return self.getLastChat['last_message'] if type(self.getLastChat) == dict and 'last_message' in self.getLastChat.keys() else "Null"
    
    @property
    def lastMessageId(self) -> str:
        return self.getLastMessage['message_id'] if type(self.getLastMessage) == dict and 'message_id' in self.getLastMessage.keys() else "Null"
    
    @property
    def messageId(self) -> str:
        return self.getLastMessage['message_id'] if type(self.getLastMessage) == dict and 'message_id' in self.getLastMessage.keys() else "Null"
    
    @property
    def lastMessageType(self) -> str:
        return self.getLastMessage['message_id'] if type(self.getLastMessage) == dict and 'message_id' in self.getLastMessage.keys() else "Null"
    
    @property
    def text(self) -> str:
        return self.getLastMessage['text'] if type(self.getLastMessage) == dict and 'text' in self.getLastMessage.keys() else "Null"
    
    @property
    def authorObjectGuid(self) -> str:
        return self.getLastMessage['author_object_guid'] if type(self.getLastMessage) == dict and 'author_object_guid' in self.getLastMessage.keys() else "Null"
    
    @property
    def isMine(self) -> str:
        return self.getLastMessage['is_mine'] if type(self.getLastMessage) == dict and 'is_mine' in self.getLastMessage.keys() else "Null"
    
    @property
    def authorTitle(self) -> str:
        return self.getLastMessage['author_title'] if type(self.getLastMessage) == dict and 'author_title' in self.getLastMessage.keys() else "Null"
    
    @property
    def authorType(self) -> str:
        return self.getLastMessage['author_type'] if type(self.getLastMessage) == dict and 'author_type' in self.getLastMessage.keys() else "Null"
    
    @property
    def lastSeenMyMid(self) -> str:
        return self.getLastChat['last_seen_my_mid'] if type(self.getLastChat) == dict and 'last_seen_my_mid' in self.getLastChat.keys() else "Null"
    
    @property
    def lastSeenPeerMid(self) -> str:
        return self.getLastChat['last_seen_peer_mid'] if type(self.getLastChat) == dict and 'last_seen_peer_mid' in self.getLastChat.keys() else "Null"
    
    @property
    def lastChatStatus(self) -> str:
        return self.getLastChat['status'] if type(self.getLastChat) == dict and 'status' in self.getLastChat.keys() else "Null"
    
    @property
    def time(self) -> str:
        return self.getLastChat['time'] if type(self.getLastChat) == dict and 'time' in self.getLastChat.keys() else "Null"
    
    @property
    def pinnedMessageId(self) -> str:
        return self.getLastChat['pinned_message_id'] if type(self.getLastChat) == dict and 'pinned_message_id' in self.getLastChat.keys() else "Null"
    
    @property
    def absObjects(self) -> dict:
        return self.getLastChat['abs_object'] if type(self.getLastChat) == dict and 'abs_object' in self.getLastChat.keys() else "Null"
    
    @property
    def absObjectGuid(self) -> str:
        return self.absObjects['object_guid'] if type(self.absObjects) == dict and 'object_guid' in self.absObjects.keys() else "Null"
    
    @property
    def absType(self) -> str:
        return self.absObjects['type'] if type(self.absObjects) == dict and 'type' in self.absObjects.keys() else "Null"
    
    @property
    def absTitle(self) -> str:
        return self.absObjects['title'] if type(self.absObjects) == dict and 'title' in self.absObjects.keys() else "Null"
    
    @property
    def absAvatarThumbnail(self) -> dict:
        return self.absObjects['avatar_thumbnail'] if type(self.absObjects) == dict and 'avatar_thumbnail' in self.absObjects.keys() else "Null"
    
    @property
    def absAvatarFileId(self) -> str:
        return self.absAvatarThumbnail['file_id'] if type(self.absAvatarThumbnail) == dict and 'file_id' in self.absAvatarThumbnail.keys() else "Null"
    
    @property
    def absAvatarMime(self) -> str:
        return self.absAvatarThumbnail['mime'] if type(self.absAvatarThumbnail) == dict and 'mime' in self.absAvatarThumbnail.keys() else "Null"
    
    @property
    def absAvatarDcId(self) -> str:
        return self.absAvatarThumbnail['dc_id'] if type(self.absAvatarThumbnail) == dict and 'dc_id' in self.absAvatarThumbnail.keys() else "Null"
    
    @property
    def absAvatarAccessHashRec(self) -> str:
        return self.absAvatarThumbnail['access_hash_rec'] if type(self.absAvatarThumbnail) == dict and 'access_hash_rec' in self.absAvatarThumbnail.keys() else "Null"
    
    @property
    def isVerified(self) -> bool:
        return self.absObjects['is_verified'] if type(self.absObjects) == dict and 'is_verified' in self.absObjects.keys() else "Null"
    
    @property
    def isDeleted(self) -> bool:
        return self.absObjects['is_deleted'] if type(self.absObjects) == dict and 'is_deleted' in self.absObjects.keys() else "Null"
    
    @property
    def isBlocked(self) -> bool:
        return self.getLastChat['is_blocked'] if type(self.getLastChat) == dict and 'is_blocked' in self.getLastChat.keys() else "Null"
    
    @property
    def lastDeletedMid(self) -> str:
        return self.getLastChat['last_deleted_mid'] if type(self.getLastChat) == dict and 'last_deleted_mid' in self.getLastChat.keys() else "Null"
    
    @property
    def groupMyLastSendTime(self) -> int:
        return self.getLastChat['group_my_last_send_time'] if type(self.getLastChat) == dict and 'group_my_last_send_time' in self.getLastChat.keys() else "Null"
    
    @property
    def pinnedMessageIds(self) -> list:
        return self.getLastChat['pinned_last_message_ids'] if type(self.getLastChat) == dict and 'pinned_last_message_ids' in self.getLastChat.keys() else "Null"
    
    @property
    def replyMessageInfo(self) -> Union[dict]:
        replx = self.networkClient.option({"object_guid": self.chatId, "message_ids": [self.lastMessageId]}, "getMessagesByID")['data']['messages'][0]
        if not 'reply_to_message_id' in replx.keys():
            return {"is_reply": False}
        else:
            data = self.networkClient.option({"object_guid": self.chatId, "message_ids": [replx['reply_to_message_id']]}, "getMessagesByID")['data']['messages'][0]
            data['is_reply'] = True
            return data

    def replyTo(self, text: str) -> dict:
        """
        Send a Message and reply on that
        """
        return self.networkClient.option({"object_guid": self.objectGuid, "text": text, "rnd": random.random() * 1e6 + 1, "reply_to_message_id": self.messageId}, "sendMessage", self.ufa)
