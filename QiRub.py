"""
This Source is the Main part of QiRub Project

QiRub is a Project for Rubika Client Handler
QiRub includes ( 'httpx', 'pycryptodome', 'fake_useragent', 'rich', 'mutagen' )

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
from mutagen import mp3, File
from tempfile import NamedTemporaryFile
import re
import time
import random
import httpx
import io
import os
import base64

__version__ = "1.0.9"

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
    
    # Thanks to Pyrubi
    def checkMetadata(self, text):
        if text is None:
            return [], ""

        real_text = re.sub(r"``|\*\*|__|~~|--|@@|##|", "", text)
        metadata = []
        conflict = 0
        mentionObjectIndex = 0
        result = []

        patterns = {
            "Mono": r"\`\`([^``]*)\`\`",
            "Bold": r"\*\*([^**]*)\*\*",
            "Italic": r"\_\_([^__]*)\_\_",
            "Strike": r"\~\~([^~~]*)\~\~",
            "Underline": r"\-\-([^__]*)\-\-",
            "Mention": r"\@\@([^@@]*)\@\@",
            "Spoiler": r"\#\#([^##]*)\#\#",
        }

        for style, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                metadata.append((match.start(), len(match.group(1)), style))

        metadata.sort()

        for start, length, style in metadata:
            if not style == "Mention":
                result.append({
                    "type": style,
                    "from_index": start - conflict,
                    "length": length,
                })
                conflict += 4
            else:
                mentionObjects = [i.group(1) for i in re.finditer(r"\@\(([^(]*)\)", text)]
                mentionType = self.guessLink(mentionObjects[mentionObjectIndex]) or "Link"

                if mentionType == "Link":
                    result.append(
                        {
                            "from_index": start - conflict,
                            "length": length,
                            "link": {
                                "hyperlink_data": {
                                    "url": mentionObjects[mentionObjectIndex]
                                },
                                "type": "hyperlink",
                            },
                            "type": mentionType,
                        }
                    )
                else:
                    result.append(
                        {
                            "type": "MentionText",
                            "from_index": start - conflict,
                            "length": length,
                            "mention_text_object_guid": mentionObjects[mentionObjectIndex],
                            "mention_text_object_type": mentionType
                        }
                    )
                real_text = real_text.replace(f"({mentionObjects[mentionObjectIndex]})", "")
                conflict += 6 + len(mentionObjects[mentionObjectIndex])
                mentionObjectIndex += 1
                
        return result, real_text
    
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
        
        return f"98{p}"
    
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
        
    def guessLink(self, link: str):
        if "rubika.ir/joing" in link: return "Group"
        elif "rubika.ir/joinc" in link: return "Channel"
        
    def endpointHash(self, link: str):
        if "/" in link:
            return link.split("/")[-1]
        else:
            return link
        
    def getDefaultTumbInline(self) -> str:
        return "iVBORw0KGgoAAAANSUhEUgAAACgAAAARCAIAAAAg6XlfAAAEwUlEQVR4nK1VXWwUVRQ+587s7HZ3u+x0u/3bav8WgQqkP1RpKdW0adXgSxFjCg9gxJhomvCIz/pgNE0gjfHBv6ARjVFDNCUagkkLTbS0Sw00BYoUuuy23dLZ7ezs7szszD0+jMEXoj70PJ2cLznfPSfnfh8SEWxiEAFxYAIALCsX/1z9fDpxt6asb2DHW8GSCgDgRAwRAHAzibntUGazN+cefPZAuSShcE3hSW2j0lvW1fT60/VDLkEkIAAUN42VCJhgq2v58x+ZG2O+KFflLZbEGGa2SO5lvXQkNr/N+O1Q7RN7AhVAgETkDI2Ij+r2/yDigFiY+lb/aRTWkuLuSnelN8v1ZKh4rijPqi1c2AkolDbIJAjtZZVDkR3iI/sSkVN8JKUTDkRECADICrEZ7fS7UoR4QOaIuqW4WWhn9ZtSuDd7/XpsecEtipIQZmUlV+4s6T/eEQFAVVVVVYPBoN/vN01TkiRELBQKAKAoCgBEIhEAcCDbtonItu1UKuX3+2VZLuo6c7nshUVzqYajxxtICIxj00vSjtfAV70N4P1nq369W3/2xlUyLd+5eOj8/eyGKebz+ZGRkYaGhkwm09HRMTU1deLEidnZ2cXFxXw+n8vlfD6fYRj79++fnp4+fPjwzMxMJpNZWVkxTdMwjM7OTm1DFeQtnX6/CoYn659PNHl6X9m15yACAHEOiIi99VtbKmreGf5CurYmlLqgVGK6rgeDwWPHjkWj0Xg83tPTc+rUqYmJiYGBAU3T9u7de+DAgVQqlU6nDcMgItM0dV03TbOjoyMSiSiKYtmWbhYZ43mSxij6lb4rUaxWMqmMkuYEDNEqWllNE00rm7LmCbKARRuZ2+1OJpOjo6OJRKK3t7e9vX19fb21tdXv9xcKhcnJyZMnT/b39zvbRkSPxwMAjLHZ2dmVlRUism3uFeCWJX9stv1hVQvAXWAS4EY2u7q6qmlaPp8jzjmQ4IKsAddVECxVLBQKVVVVw8PDD8+qsbExHA4713706NF0On3mzJnjx4/H4/GlpaVYLNbc3JxIJPr6+mzbvnDhQn1dQ8A2bxrBqQ2hRTYFBBciASBjlmWZpimKIoIN6MraUpVkDMlLT7kV0efzdXd3ExHnHBEZYy0tLaFQCBG7u7t1Xa+tre3q6mKMDQ4Ojo2NRSKRffv22bY9Pj4uSdKRI0eU9bTX7165vWwTLW4UmcETRG2InKFBgEAAAJLMteShwM223N2Qp5hD138r18Ov9e/xzacTn7z3c0lTeVz2hp+L9rZEng946ktczB9GLMK9MXb7rOvKvdx9WVfK0AIRADjnjLGHLZzREdGpOwni31LjbIVz7rzYyRljW5+sWW4so2i5wEkkmlK12Lr5THngZW08eOvLYuYaCd684GbVGY+Y5HLP5mg1EQHi15dvnP5+JrmqNvdvL9/+OMvN+4zv+kvnWvNiZdYjcNSvrnG1ILb1eQ++vWkm4SxjNaON/hCbgQd1j12uMieRCtsqQkGvq0Qr1C9r8r06qecNT9sLsLnuZHMSGALAkrJwaeGDudXfOYhtlf6AqDN3dTQ8VF8+yAQJHJHfXD8mAk5cYAwA5pIXf7nxYcSr7I682Fj5qlsKAfxjnX8BoH+PlgeA47wAAAAASUVORK5CYII="
    
    def getImageThumbnail(self, bytes:bytes) -> str:
        try:
            from PIL import Image
        except ImportError:
            os.system("pip install pillow")
            from PIL import Image
            
        image = Image.open(io.BytesIO(bytes))
        width, height = image.size
        if height > width:
            new_height = 40
            new_width  = round(new_height * width / height)
        else:
            new_width = 40
            new_height = round(new_width * height / width)
        image = image.resize((new_width, new_height), Image.LANCZOS)
        changed_image = io.BytesIO()
        image.save(changed_image, format="PNG")
        return base64.b64encode(changed_image.getvalue()).decode("UTF-8")
    
    def getImageSize(self, bytes:bytes) -> str:
        try:
            from PIL import Image
        except ImportError:
            os.system("pip install pillow")
            from PIL import Image

        width, height = Image.open(io.BytesIO(bytes)).size
        return width , height
    
    def getVideoData(self, bytes:bytes) -> list:
        try:
            from moviepy.editor import VideoFileClip

            with NamedTemporaryFile(delete=False, dir=".") as temp_video:
                temp_video.write(bytes)
                temp_path = temp_video.name

            os.chmod(temp_path, 0o777)

            try:
                from PIL import Image
            except ImportError:
                os.system("pip install pillow")
                from PIL import Image

            with VideoFileClip(temp_path) as clip:
                duration = clip.duration
                resolution = clip.size
                thumbnail = clip.get_frame(0)
                thumbnail_image = Image.fromarray(thumbnail)
                thumbnail_buffer = io.BytesIO()
                thumbnail_image.save(thumbnail_buffer, format="JPEG")
                thumbnail_b64 = base64.b64encode(thumbnail_buffer.getvalue()).decode("UTF-8")
                clip.close()

            os.remove(temp_path)

            return thumbnail_b64, resolution, duration
        except ImportError:
            print("Can't get video data! Please install the moviepy library by following command:\npip install moviepy" + "\033[00m")
            return self.getDefaultTumbInline(), [900, 720], 1
        except:
            return self.getDefaultTumbInline(), [900, 720], 1
        
    def getVoiceDuration(self, bytes:bytes) -> int:
        file = io.BytesIO()
        file.write(bytes)
        file.seek(0)
        return mp3.MP3(file).info.length
    
    def getMusicArtist(self, bytes:bytes) -> str:
        try:
            audio = File(io.BytesIO(bytes), easy=True)

            if audio and "artist" in audio:
                return audio["artist"][0]
            
            return "qirubika"
        except Exception:
            return "qirubika"

    def getMe(self):
        return self.network.option({}, "getUserInfo", self.ufa)

    def getChatsUpdates(self):
        return self.network.option({"state": time.time() - 150}, "getChatsUpdates", self.ufa)
    
    def getChats(self):
        return self.network.option({"start_id": None}, "getChats", self.ufa)

    def onMessage(self):
        yield QiUpdater(self.authtoken, self.privatekey, self.getChatsUpdates(), self.ufa, self.proxy)

    def onAutoMessage(self, print_text: bool = False, plugin_text: str = ""):
        try:
            msgset = set()
            for msg in self.onMessage():
                if not msg.messageId in msgset:
                    msgset.add(msg.messageId)
                    if print_text:
                        if "<QI@Text>" in plugin_text:
                            print(plugin_text.replace("<QI@Text>", msg.text))
                        else:
                            print(msg.text)
                    return msg
                else:
                    msgset.add(msg.messageId)
                    return msg
        except KeyboardInterrupt:
            exit(1)

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
    
    def checkChannelUsername(self, username: str, replace_tag: bool = True):
        return self.network.option({"username": username.replace("@", "")},
                                   "checkChannelUsername", self.ufa) if replace_tag else self.network.option({"username": username},
                                   "checkChannelUsername", self.ufa)
    
    def checkChannelUsernames(self, usernames: list, replace_tag: bool = True):
        if not type(usernames) == list:
            raise ValueError("`usernames` parameter in checkChannelUsernames is not list")
        
        dbs = {}

        for username in usernames:
            dbs[username] = self.checkChannelUsername(username=username, replace_tag=replace_tag)

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
    
    def setGroupAdmin(self, group_guid: str, member_guid: str, action: str = "SetAdmin", access_list: list = []):
        if not action in self.group_admins_actions:
            raise ValueError("`action` parameter in ( setGroupAdmin / addGroupAdmin ) functions, is not available, to see more actions print `group_admins_actions` property")
        
        if type(access_list) != list and type(access_list) == str:
            access_list = [access_list]

        return self.network.option({"group_guid": group_guid, "member_guid": member_guid,
                                    "action": action, "access_list": access_list}, "setGroupAdmin", self.ufa)
    
    def addGroupAdmin(self, channel_guid: str, member_guid: str, action: str = "SetAdmin", access_list: list = []):
        return self.setGroupAdmin(channel_guid=channel_guid, member_guid=member_guid,
                                  action=action, access_list=access_list)
    
    def updateChannelUsername(self, channel_guid: str, username: str, replace_tag: bool = True):
        return self.network.option({"channel_guid": channel_guid,
                                    "username": username.replace("@", "")}, "updateChannelUsername", self.ufa) if replace_tag else self.network.option({"channel_guid": channel_guid,
                                    "username": username}, "updateChannelUsername", self.ufa)
    
    def sendMessage(self, chat_object_guid: str, text_message: str, reply_to_message_id: str = None):
        metadata = self.checkMetadata(text_message)

        inp = {
            "object_guid": chat_object_guid,
            "text": text_message,
            "reply_to_message_id": reply_to_message_id,
            "rnd": random.random() * 1e6 + 1
        }

        if metadata[0] != []:
            inp["metadata"] = {"meta_data_parts": metadata[0]}

        return self.network.option(inp, "sendMessage", self.ufa)

    def requestSendFile(self, file_name: str, mime: str, size: str):
        return self.network.option({"file_name": file_name, "mime": mime, "size": size}, "requestSendFile", self.ufa)
    
    def __sendFileInline(
            self,
            objectGuid:str,
            file:str,
            text:str,
            messageId:str,
            fileName:str,
            type:dict,
            isSpoil:bool=False,
            customThumbInline:str=None,
            time:int=None,
            performer:str=None
    ) -> dict:
        uploadData:dict = self.network.upload(file=file, fileName=fileName)
        if not uploadData: return
        
        input:dict = {
            "file_inline": {
                "dc_id": uploadData["dc_id"],
                "file_id": uploadData["id"],
                "file_name": uploadData["file_name"],
                "size": uploadData["size"],
                "mime": uploadData["mime"],
                "access_hash_rec": uploadData["access_hash_rec"],
                "type": type,
                "is_spoil": isSpoil
            },
            "object_guid": objectGuid,
            "rnd": str(random.randint(-99999999, 99999999)),
            "reply_to_message_id": messageId
        }

        if type in ["Image", "Video", "Gif", "VideoMessage"]:
            customThumbInline = self.getImageThumbnail(
                customThumbInline
                if isinstance(customThumbInline, bytes)
                else httpx.get(customThumbInline).text
                if self.guessLink(customThumbInline)
                else open(customThumbInline, "rb").read()
            ) if customThumbInline else None

            if not type == "Image":
                videoData:list = self.getVideoData(uploadData["file"])
                input["file_inline"]["time"] = videoData[2] * 1000

            fileSize:list = self.getImageSize(uploadData["file"]) if type == "Image" else videoData[1]
            input["file_inline"]["width"] = fileSize[0]
            input["file_inline"]["height"] = fileSize[1]

            if type == "VideoMessage":
                input["file_inline"]["type"] = "Video"
                input["file_inline"]["is_round"] = True

            input["file_inline"]["thumb_inline"] = customThumbInline or (self.getImageThumbnail(uploadData["file"]) if type == "Image" else videoData[0])

        if type in ["Music", "Voice"]:
            input["file_inline"]["time"] = (time or self.getVoiceDuration(uploadData["file"])) * (1000 if type == "Voice" else 1)

            if type == "Music":
                input["file_inline"]["music_performer"] = performer or self.getMusicArtist(uploadData["file"])

        metadata:list = self.checkMetadata(text)
        if metadata[1]: input["text"] = metadata[1]
        if metadata[0]: input["metadata"] = {"meta_data_parts": metadata[0]}

        return self.network.option(
            method="sendMessage",
            input_data=input,
            use_fake_useragent=self.ufa
        )
    
    def sendFile(self, objectGuid:str, file:str, messageId:str, text:str, fileName:str) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="File"
        )
    
    def sendImage(self, objectGuid:str, file:str, fileName:str, text:str = None, messageId:str = None, isSpoil:bool = False, thumbInline:str = None) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="Image",
            isSpoil=isSpoil,
            customThumbInline=thumbInline
        )
    
    def sendVideo(self, objectGuid:str, file:str, fileName:str, text:str, messageId:str = None, isSpoil:bool = False, thumbInline:str = None) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="Video",
            isSpoil=isSpoil,
            customThumbInline=thumbInline
        )
    
    def sendVideoMessage(self, objectGuid:str, file:str, fileName:str, text:str, messageId:str = None, thumbInline:str = None) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="VideoMessage",
            customThumbInline=thumbInline
        )
    
    def sendGif(self, objectGuid:str, file:str, fileName:str, text:str, messageId:str = None, thumbInline:str = None) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="Gif",
            customThumbInline=thumbInline
        )
    
    def sendMusic(self, objectGuid:str, file:str, fileName:str, text:str, messageId:str = None, performer = None, thumbInline:str = None) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="Music",
            performer=performer
        )
    
    def sendVoice(self, objectGuid:str, file:str, fileName:str, text:str, messageId:str = None) -> dict:
        return self.__sendFileInline(
            objectGuid=objectGuid,
            file=file,
            text=text,
            messageId=messageId,
            fileName=fileName,
            type="Voice",
            time=self.getVoiceDuration(open(file, 'rb').read())
        )
    
    def sendLocation(self, objectGuid:str, latitude:int, longitude:int, messageId:str = None) -> dict:
        return self.network.option(
            method="sendMessage",
            input={
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "object_guid":objectGuid,
                "rnd": random.randint(-99999999, 99999999),
                "reply_to_message_id": messageId
            }
        )
    
    def sendMessageAPICall(self, objectGuid:str, text:str, messageId:str, buttonId:str) -> dict:
        return self.network.option(
            method="sendMessageAPICall",
            input={
                "text": text,
                "object_guid": objectGuid,
                "message_id": messageId,
                "aux_data": {"button_id": buttonId}
            },
            use_fake_useragent=self.ufa
        )
    
    def editMessage(self, objectGuid, text, messageId) -> dict:
        metadata = self.checkMetadata(text)
        data = {
            "object_guid": objectGuid,
            "text": metadata[1],
            "message_id": messageId,
        }
        if metadata[0] != []:
            data["metadata"] = {"meta_data_parts": metadata[0]}
        return self.network.option(data, "editMessage", self.ufa)
    
    def deleteAvatar(self, object_guid: str, avatar_id: str):
        return self.network.option({"object_guid": object_guid, "avatar_id": avatar_id}, "deleteAvatar", self.ufa)
    
    def deleteChatHistory(self, object_guid: str, last_message_id: str):
        return self.network.option({"object_guid": object_guid, "last_message_id": last_message_id}, "deleteChatHistory", self.ufa)
    
    def getAbsObjects(self, object_guids: list):
        if type(object_guids) == str:
            object_guids = [object_guids]

        return self.network.option({"object_guid": object_guids}, "getAbsObjects", self.ufa)
        
    def abstractionObjects(self, object_guids: list):
        return self.getAbsObjects(object_guids=object_guids)
    
    def getAvatars(self, object_guid: str):
        return self.network.option({'object_guid': object_guid}, "getAvatars", self.ufa)
    
    def getAvatarsArray(self, object_guids: list):
        if not type(object_guids) == list:
            raise ValueError("`object_guids` parameter of method getAvatarsArray is not list")
        
        dbs = {}

        for guid in object_guids:
            dbs[guid] = self.getAvatars(guid)

        return dbs
    
    def getChats(self, start_id: str = None):
        return self.network.option({"start_id": start_id}, "getChats", self.ufa)
    
    def getLinkFromAppUrl(self, app_url: str):
        return self.network.option({"app_url": app_url}, "getLinkFromAppUrl", self.ufa)
    
    @property
    def search_chat_messages_types(self):
        return (
            "Text",
            "Hashtag"
        )

    def searchTextMessages(self, object_guid: str, text: str):
        return self.network.option({"object_guid": object_guid, "search_text": text, "type": "Text"}, "searchChatMessages", self.ufa)
    
    def searchHashtagMessages(self, object_guid: str, hashtag: str):
        return self.network.option({"object_guid": object_guid, "search_text": hashtag, "type": "Hashtag"}, "searchChatMessages", self.ufa)
    
    def seenChats(self, seen_dictionary: dict):
        return self.network.option({"seen_list": seen_dictionary}, "seenChats", self.ufa)
    
    @property
    def chat_activities(self):
        return (
            "Typing",
            "Uploading",
            "Recording"
        )

    def sendChatActivity(self, object_guid: str, activity: str = "Typing"):
        if not activity in self.chat_activities:
            raise ValueError("`activity` parameter does not available in sendChatActivity, to see more options print `chat_activities` property")
        
        return self.network.option({
            "object_guid": object_guid,
            "activity": activity
        }, "sendChatActivity", self.ufa)
    
    @property
    def chat_actions(self): 
        return ('Mute', 'Unmute')

    def setActionChat(self, object_guid: str, action: str = "Mute"):
        if not action in self.chat_actions:
            raise ValueError("`action` parameter does not available in setActionChat, to see more options print `chat_actions` property")
        
        return self.network.option({"object_guid": object_guid, "action": action}, "setActionChat", self.ufa)
    
    def uploadAvatar(self, object_guid: str, image: str):
        if not os.path.exists(image):
            raise ValueError("`image` parameter, get an unexist path")
        
        database = {}

        if type(image) == str:
            database['file_name'] = image.split("/")[-1]
        
        else:
            database['file_name'] = "qirubika.jpg"

        uploaded = self.network.upload(image, database["file_name"], os.path.getsize(image))

        return self.network.option({
            "object_guid": object_guid,
            "thumnail_file_id": uploaded['id'],
            "main_file_id": uploaded['id']
        }, "uploadAvatar", self.ufa)
    
    def addAddressBook(self, phone: str, first_name: str, last_name: str = ''):
        return self.network.option({"phone": phone, "first_name": first_name, "last_name": last_name}, "addAddressBook", self.ufa)
    
    def deleteContact(self, user_guid: str):
        return self.network.option({"user_guid": user_guid}, "deleteContact", self.ufa)
    
    def getContacts(self, start_id: str = None):
        return self.network.option({"start_id": start_id}, "getContacts", self.ufa)
    
    def getContactsUpdates(self):
        return self.network.option({"state": round(time.time()) - 150}, "getContactsUpdates", self.ufa)
    
    def getObjectByUsername(self, username: str, replace_tag: bool = True):
        return self.network.option({"username": username.replace("@", "")}, "getObjectByUsername", self.ufa) if replace_tag else \
               self.network.option({"username": username}, "getObjectByUsername", self.ufa)
    
    def getProfileLinkItems(self, object_guid: str):
        return self.network.option({"object_guid": object_guid}, "getProfileLinkItems", self.ufa)
    
    def getRelatedObjects(self, object_guid: str):
        return self.network.option({"object_guid": object_guid}, "getRelatedObjects", self.ufa)
    
    def getTranscription(self, message_id: str, transcription_id: str):
        return self.network.option({"message_id": message_id, "transcription_id": transcription_id}, "getTranscription", self.ufa)
    
    def searchGlobalObjects(self, search_text: str):
        return self.network.option({"search_text": search_text}, "searchGlobalObjects", self.ufa)
    
    def addToMyGifSet(self, object_guid: str, message_id: str):
        return self.network.option({"object_guid": object_guid, "message_id": message_id}, "addToMyGifSet", self.ufa)
    
    def getMyGifSet(self):
        return self.network.option({}, "getMyGifSet", self.ufa)
    
    def removeFromMyGifSet(self, file_id: str):
        return self.network.option({"file_id": file_id}, "removeFromMyGifSet", self.ufa)
    
    def addGroup(self, title: str, member_guids: list):
        if type(member_guids) == str:
            member_guids = [member_guids]

        return self.network.option({"title": title, "member_guids": member_guids}, "addGroup", self.ufa)
    
    def addGroupMembers(self, group_guid: str, member_guids: list):
        if type(member_guids) == str:
            member_guids = [member_guids]
        
        return self.network.option({"group_guid": group_guid, "member_guids": member_guids}, "addGroupMembers", self.ufa)
    
    @property
    def ban_group_member_actions(self):
        return (
            "Set",
            "Unset"
        )

    def banGroupMember(self, group_guid: str, member_guid: str):
        return self.network.option({"group_guid": group_guid, "member_guid": member_guid,
                                    "action": "Set"}, "banGroupMember", self.ufa)
    
    def createGroupVoiceChat(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "createGroupVoiceChat", self.ufa)
    
    def deleteNoAccessGroupChat(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "deleteNoAccessGroupChat", self.ufa)
    
    def editGroupInfo(self,
                group_guid: str,
                title: str = None,
                description: str = None,
                slow_mode: str = None,
                event_messages: bool = None,
                sign_messages: str = None,
                chat_reaction_setting: dict = None,
                chat_history_for_new_members: str = "Hidden"):
        
        updatedParameters = []
        inp = {
            "group_guid": group_guid
        }

        if title is not None:
            inp['title'] = title
            updatedParameters.append('title')

        if description is not None:
            inp['description'] = description
            updatedParameters.append('description')

        if slow_mode is not None:
            inp['slow_mode'] = slow_mode
            updatedParameters.append("slow_mode")

        if event_messages is not None:
            inp['event_messages'] = event_messages
            updatedParameters.append("event_messages")

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
        return self.network.option({"group_guid": group_guid, "start_id": start_id}, "getBannedGroupMembers", self.ufa)
    
    def getGroupAdminAccessList(self, group_guid: str, member_guid: str):
        return self.network.option({"group_guid": group_guid, "member_guid": group_guid}, "getGroupAdminAccessList", self.ufa)
    
    def getGroupAdminMembers(self, group_guid: str, start_id: str = None):
        return self.network.option({"group_guid": group_guid, "start_id": start_id}, "getGroupAdminMembers", self.ufa)
    
    def getGroupAllMembers(self, group_guid: str, search_text: str = None, start_id: str = None):
        return self.network.option({"group_guid": group_guid, "search_text": search_text, "start_id": start_id}, "getGroupAllMembers", self.ufa)
    
    def getGroupDefaultAccess(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "getGroupDefaultAccess", self.ufa)
    
    def getGroupInfo(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "getGroupInfo", self.ufa)
    
    def getGroupLink(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "getGroupInfo", self.ufa)
    
    def getGroupMentionList(self, group_guid: str, search_mention: str = None):
        return self.network.option({"group_guid": group_guid, "search_mention": search_mention}, "getGroupMentionList", self.ufa)
    
    def getGroupVoiceChatUpdates(self, group_guid: str, voice_chat_id: str):
        return self.network.option({"group_guid": group_guid, "voice_chat_id": voice_chat_id, "state": round(time.time()) - 150}, "getGroupVoiceChatUpdates", self.ufa)
    
    def groupPreviewByJoinLink(self, link: str, use_endpoint_hash: bool = True):
        return self.network.option({"hash_link": self.endpointHash(link)}, "groupPreviewByJoinLink", self.ufa) if use_endpoint_hash else \
               self.network.option({"hash_link": link}, "groupPreviewByJoinLink", self.ufa)
    
    def leaveGroupVoiceChat(self, group_guid: str, voice_chat_id: str):
        return self.network.option({"group_guid": group_guid, "voice_chat_id": voice_chat_id}, "leaveGroupVoiceChat", self.ufa)
    
    def removeGroup(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "removeGroup", self.ufa)
    
    def setGroupDefaultAccess(self, group_guid: str, access_list: list = []):
        if type(access_list) == str:
            access_list = [access_list]

        return self.network.option({"group_guid": group_guid, "access_list": access_list}, "setGroupDefaultAccess", self.ufa)
    
    def setGroupLink(self, group_guid: str):
        return self.network.option({"group_guid": group_guid}, "setGroupLink", self.ufa)
    
    def changeGroupLink(self, group_guid: str):
        return self.setGroupLink(group_guid=group_guid)
    
    def setGroupVoiceChatSetting(self, group_guid: str, voice_chat_id: str, title: str = None):
        inp = {
            "group_guid": group_guid,
            "voice_chat_id": voice_chat_id
        }

        updatedParameters = []

        if title is not None:
            inp['title'] = title
            updatedParameters.append("title")

        inp['updated_parameters'] = updatedParameters

        return self.network.option(inp, "setGroupVoiceChatSetting", self.ufa)
    
    def checkUserUsername(self, username: str, replace_tag: bool = True):
        return self.network.option({"username": username.replace("@", "")}, "checkUserUsername", self.ufa) if replace_tag else \
               self.network.option({"username": username}, "checkUserUsername", self.ufa)
    
    def deleteUserChat(self, user_guid: str, last_deleted_message_id: str):
        return self.network.option({"user_guid": user_guid, "last_deleted_message_id": last_deleted_message_id}, "deleteUserChat", self.ufa)
    
    @property
    def block_user_actions(self):
        return (
            "Block",
            "Unblock"
        )

    def blockUser(self, user_guid: str):
        return self.network.option({"user_guid": user_guid, "action": "Block"}, "setBlockUser", self.ufa)
    
    def getChatInfo(self, guid: str):
        type = self.guessGuid(guid=guid)
        return self.network.option({f"{type.lower()}_guid": guid}, f"get{type}Info", self.ufa)
