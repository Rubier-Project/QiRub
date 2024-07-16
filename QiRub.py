"""
This Source is the Main part of QiRub Project

QiRub is a Project for Rubika Client Handler
QiRub includes ( 'httpx', 'pycryptodome', 'fake_useragent' )

In fact when you import the ClientMessenger class or
    run the source what called ClientMessenger class, its automatically set a
        random fake user agent to have a better connection, you can off/on that on ClientMessenger class on the
            `UseFakeUserAgent` Parameter with boolean types, also you can use Proxy, on the `Proxy` Parameter to set your proxies and have a better connection
        

Make Sure you use the latest version of QiRub, for
More info you can visit our github, also you can access
To new News, Updates, Bug Fixes, ... with github

Github: https://github.com/Rubier-Project/QiRub

"""

from .network import QiNetwork
from .updater import QiUpdater
from .DataParse import Parse
import time

__version__ = "1.0.0"

class ClientMessenger(object):
    def __init__(self, AuthToken: str, PrivateKey: str, UseFakeUserAgent: bool = True, Proxy = None):
        self.authtoken = AuthToken
        self.privatekey = PrivateKey.replace("-----BEGIN PRIVATE KEY-----\n", "").replace("\n-----END PRIVATE KEY-----", "")

        self.ufa = UseFakeUserAgent
        self.proxy = Proxy
        
        self.network = QiNetwork(self.authtoken, self.privatekey, Proxy)
    
    @property
    def accountInfo(self):
        return self.network.option({}, "getUserInfo", self.ufa)
    
    def handlePhoneNumber(self, phone: str):
        p = ""
        if phone.startswith("0"):
            p = phone[1:]
        elif phone.startswith("98"):
            p = phone[2:]
        elif phone.startswith("+98"):
            p = phone[3:]
        else:
            p = phone
        
        return p
    
    def guessGuid(self, guid: str):
        if guid.startswith("c0"):
            return "Channel"
        elif guid.startswith("g0"):
            return "Group"
        elif guid.startswith("u0"):
            return "User"
        elif guid.startswith("b0"):
            return "Bot"
        elif guid.startswith("s0"):
            return "Service"
        
    def endpointHash(self, link: str):
        if "/" in link:
            return link.split("/")[-1]
        else:
            return link

    def getMe(self):
        return self.network.option({}, "getUserInfo", self.ufa)

    def getChatsUpdates(self):
        return self.network.option({"state": time.time() - 150}, "getChatsUpdates", self.ufa)
    
    def getChats(self):
        return self.network.option({"start_id": None}, "getChats", self.ufa)

    def onMessage(self):
        yield QiUpdater(self.authtoken, self.privatekey, self.getChatsUpdates(), self.ufa, self.proxy)

    def onChatMessage(self, chat_object_guid: str):
        try:
            datas = self.getChatsUpdates()
            if datas['data']['chats'][0]['object_guid'] == chat_object_guid:
                return datas['data']['chats'][0]
            else:
                return {}
        except Exception as ERROR:
            return {"error": True, "base": str(ERROR)}
    
    @property
    def send_code_types(self):
        return ("SMS", "Internal")

    def sendCode(self, phone_number: str, pass_key: str, send_type: str = "SMS", parsePhoneNumber: bool = True):
        if not send_type in self.send_code_types:
            raise ValueError(f"Send type does not available, use send_code_types property to see more of that")
        return self.network.option({"phone_number": self.handlePhoneNumber(phone_number), "pass_key": pass_key,
                                    "send_type": send_type}, "sendCode", self.ufa) if parsePhoneNumber else self.network.option({"phone_number": phone_number, "pass_key": pass_key,
                                    "send_type": send_type}, "sendCode", self.ufa)
    
    def signIn(self, phone_number: str, phone_code: str, phone_code_hash: str, public_key: str, parsePhoneNumber: bool = True):
        return self.network.option({"phone_number": phone_number, "phone_code": phone_code,
                                    "phone_code_hash": phone_code_hash, "public_key": public_key}, "signIn", self.ufa) if parsePhoneNumber else self.network.option({"phone_number": self.handlePhoneNumber(phone_number), "phone_code": phone_code,
                                    "phone_code_hash": phone_code_hash, "public_key": public_key}, "signIn", self.ufa)

    def addChannel(self, title: str, description: str = None, member_guids: list = None):
        return self.network.option({"title": title, "description": description,
                                    "member_guids": member_guids}, "addChannel", self.ufa) if type(member_guids) == list else self.network.option({"title": title, "description": description,
                                    "member_guids": [member_guids]}, "addChannel", self.ufa)
    
    def addChannelMembers(self, object_guid: str, member_guids: list = None):
        return self.network.option({"channel_guid": object_guid, "member_guids": member_guids}, "addChannelMembers", self.ufa) if type(member_guids) == list else \
               self.network.option({"channel_guid": object_guid, "member_guids": [member_guids]}, "addChannelMembers", self.ufa)
    
    @property
    def ban_channel_member_actions(self):
        return ("Set", "Unset")

    def banChannelMember(self, object_guid: str, member_guid: str):
        return self.network.option({"channel_guid": object_guid, "member_guid": member_guid,
                                    "action": "Set"}, "banChannelMember", self.ufa)
    
    def banChannelMembers(self, object_guid: str, member_guids: list):

        if type(member_guids) != list and type(member_guids) == str:
            member_guids = [member_guids]

        dbs = {}

        for _ in member_guids:
            dbs[_] = self.banChannelMember(object_guid=object_guid, member_guid=_)
        
        return dbs

    def channelPreviewByJoinLink(self, link: str, use_endpoint_hash: bool = True):
        return self.network.option({"hash_link": self.endpointHash(link)},
                                   "channelPreviewByJoinLink", self.ufa) if use_endpoint_hash else self.network.option({"hash_link": link},
                                   "channelPreviewByJoinLink", self.ufa)
    
    def checkChannelUsername(self, username: str, replace_hashtag: bool = True):
        return self.network.option({"username": username.replace("@", "")},
                                   "checkChannelUsername", self.ufa) if replace_hashtag else self.network.option({"username": username},
                                   "checkChannelUsername", self.ufa)
    
    def checkChannelUsernames(self, usernames: list, replace_hashtag: bool = True):
        if not type(usernames) == list:
            raise ValueError("`usernames` parameter in checkChannelUsernames is not list")
        
        dbs = {}

        for username in usernames:
            dbs[username] = self.checkChannelUsername(username=username, replace_hashtag=replace_hashtag)

        return dbs
    
    def createChannelVoiceChat(self, channel_guid: str):
        return self.network.option({"channel_guid": channel_guid},
                                   "createChannelVoiceChat", self.ufa)
    
    def deleteNoAccessGroupChat(self, group_guid: str):
        return self.network.option({"group_guid": group_guid},
                                   "deleteNoAccessGroupChat", self.ufa)
    
    def discardChannelVoiceChat(self, channel_guid: str, voice_chat_id: str):
        return self.network.option({"channel_guid": channel_guid, 
                                    "voice_chat_id": voice_chat_id}, "discardChannelVoiceChat", self.ufa)
    
    @property
    def chat_history_for_new_members_list(self):
        return ('Hidden', 'Visible')

    def editChannelInfo(self,
                channel_guid: str,
                title: str = None,
                description: str = None,
                channel_type: str = None,
                sign_messages: str = None,
                chat_reaction_setting: dict = None,
                chat_history_for_new_members: str = "Hidden"):
        
        updatedParameters = []
        inp = {
            "channel_guid": channel_guid
        }

        if title is not None:
            inp['title'] = title
            updatedParameters.append('title')

        if description is not None:
            inp['description'] = description
            updatedParameters.append('description')

        if channel_type is not None:
            inp['channel_type'] = channel_type
            updatedParameters.append('channel_type')

        if sign_messages is not None:
            inp['sign_messages'] = sign_messages
            updatedParameters.append('sign_messages')

        if chat_reaction_setting is not None:
            inp['chat_reaction_setting'] = chat_reaction_setting
            updatedParameters.append('chat_reaction_setting')

        if chat_history_for_new_members is not None:
            if chat_history_for_new_members not in self.chat_history_for_new_members_list:
                raise ValueError('`chat_history_for_new_members` parameter in editChannelInfo is not available, to see more options use `chat_history_for_new_members_list` property.')

            inp['chat_history_for_new_members'] = chat_history_for_new_members
            updatedParameters.append('chat_history_for_new_members')

        inp['updated_parameters'] = updatedParameters

        return self.network.option(inp, "editChannelInfo", self.ufa)
    
    def getBannedGroupMembers(self, group_guid: str, start_id: str = None):
        return self.network.option({
            "group_guid": group_guid,
            "start_id": start_id
        }, "getBannedGroupMembers", self.ufa)
    
    def getChannelAdminAccessList(self, channel_guid: str, admin_user_guid: str):
        return self.network.option({
            "channel_guid": channel_guid,
            "member_guid": admin_user_guid
        }, "getChannelAdminAccessList", self.ufa)
    
    def getChannelAdminsAccessList(self, channel_guid: str, admins_user_guids: list):
        if not type(admins_user_guids) == list:
            raise ValueError("`admins_user_guids` parameter in getChannelAdminsAccessList is not list")
        
        dbs = {}

        for guid in admins_user_guids:
            dbs[guid] = self.getChannelAdminAccessList(channel_guid=channel_guid, admin_user_guid=guid)

        return dbs
    
    def getChannelAdminMembers(self, channel_guid: str, start_id: str = None):
        return self.network.option({
            "channel_guid": channel_guid,
            "start_id": start_id
        }, "getChannelAdminMembers", self.ufa)
    
    def getChannelAllMembers(self, channel_guid: str, search_text: str = '', start_id: str = None):
        return self.network.option({
            "channel_guid": channel_guid,
            "start_id": start_id
        }, "getChannelAllMembers", self.ufa)
    
    def getChannelInfo(self, channel_guid: str):
        return self.network.option({"channel_guid": channel_guid}, "getChannelInfo", self.ufa)
    
    def getChannelLink(self, channel_guid: str):
        return self.network.option({"channel_guid": channel_guid}, "getChannelLink", self.ufa)
    
    def getGroupDefaultAccess(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "getGroupDefaultAccess", self.ufa)
    
    def getGroupMentionList(self, group_guid: str, search_mention: str = None):
        return self.network.option({"group_guid": group_guid, "search_mention": search_mention}, "getGroupMentionList", self.ufa)
    
    def getGroupVoiceChatUpdates(self, group_guid: str, voice_chat_id: str  ):
        return self.network.option({"group_guid": group_guid, "voice_chat_id": voice_chat_id, "state": round(time.time()) - 150}, "getGroupVoiceChatUpdates", self.ufa)
    
    @property
    def join_channel_actions(self):
        return (
            "Join",
            "Remove",
            "Archive"
        )
    
    def joinChannelAction(self, channel_guid: str, action: str):
        if not action in self.join_channel_actions:
            raise ValueError("`action` parameter in joinChannelAction does not available, to see more actions print `join_channel_actions` property")
        
        return self.network.option({"channel_guid": channel_guid, "action": action}, "joinChannelAction", self.ufa)
    
    def joinChannelByLink(self, link: str, use_endpoint_hash: bool = True):
        return self.network.option({"hash_link": self.endpointHash(link)},
                                   "joinChannelByLink", self.ufa) if use_endpoint_hash else self.network.option({"hash_link": self.endpointHash(link)},
                                   "joinChannelByLink", self.ufa)
    
    def joinGroup(self, link: str, use_endpoint_hash: bool = True):
        return self.network.option({"hash_link": self.endpointHash(link)},
                                   "joinGroup", self.ufa) if use_endpoint_hash else self.network.option({"hash_link": self.endpointHash(link)},
                                   "joinGroup", self.ufa)
    
    def leaveGroup(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "leaveGroup", self.ufa)
    
    def leaveGroupVoiceChat(self, group_guid: str, voice_chat_id: str):
        return self.network.option({"group_guid": group_guid, "voice_chat_id": voice_chat_id}, "leaveGroupVoiceChat", self.ufa)
    
    def removeChannel(self, channel_guid: str):
        return self.network.option({"channel_guid": channel_guid}, "removeChannel", self.ufa)
    
    def seenChannelMessages(self, channel_guid: str, min_id: int, max_id: int):
        return self.network.option({"channel_guid": channel_guid, "min_id": min_id, "max_id": max_id}, "seenChannelMessages", self.ufa)
    
    def setChannelLink(self, channel_guid: str):
        return self.network.option({"channel_guid": channel_guid}, "setChannelLink", self.ufa)
    
    def changeChannelLink(self, channel_guid: str):
        return self.setChannelLink(channel_guid=channel_guid)
    
    def setChannelVoiceChatSetting(self, channel_guid: str, voice_chat_id: str, title: str = None):
        inp = {
            "channel_guid": channel_guid,
            "voice_chat_id": voice_chat_id
        }

        updatedParameters = []

        if title is not None:
            inp['title'] = title
            updatedParameters.append("title")

        inp['updated_parameters'] = updatedParameters

        return self.network.option(inp, "setChannelVoiceChatSetting", self.ufa)
    
    def changeChannelVoiceChatSetting(self, channel_guid: str, voice_chat_id: str, title: str = None):
        return self.setChannelVoiceChatSetting(channel_guid=channel_guid, voice_chat_id=voice_chat_id, title=title)
    
    @property
    def group_admins_actions(self):
        return (
            "SetAdmin",
            "UnsetAdmin"
        )
    
    def setGroupAdmin(self, channel_guid: str, member_guid: str, action: str = "SetAdmin", access_list: list = []):
        if not action in self.group_admins_actions:
            raise ValueError("`action` parameter in ( setGroupAdmin / addGroupAdmin ) functions, is not available, to see more actions print `group_admins_actions` property")
        
        if type(access_list) != list and type(access_list) == str:
            access_list = [access_list]

        return self.network.option({"channel_guid": channel_guid, "member_guid": member_guid,
                                    "action": action, "access_list": access_list}, "setGroupAdmin", self.ufa)
    
    def addGroupAdmin(self, channel_guid: str, member_guid: str, action: str = "SetAdmin", access_list: list = []):
        return self.setGroupAdmin(channel_guid=channel_guid, member_guid=member_guid,
                                  action=action, access_list=access_list)
    
    def updateChannelUsername(self, channel_guid: str, username: str, replace_hashtag: bool = True):
        return self.network.option({"channel_guid": channel_guid,
                                    "username": username.replace("@", "")}, "updateChannelUsername", self.ufa) if replace_hashtag else self.network.option({"channel_guid": channel_guid,
                                    "username": username.replace("@", "")}, "updateChannelUsername", self.ufa)
