from QiRub import ClientMessenger, Parse

AUTH = ""
KEY = ""
GUID = ""

dbs = {
    "image": "C:\\Users\\SYSTEM\\Pictures\\photo.jpg",
    "video": "C:\\Users\\SYSTEM\\Videos\\video.mp4",
    "music": "C:\\Users\\SYSTEM\\Musics\\music.mp3",
    "voice": "C:\\Users\\SYSTEM\\Voices\\voice.mp3"
}

app = ClientMessenger(AuthToken=AUTH, PrivateKey=KEY)
parse = Parse()

img = app.sendImage(GUID, dbs['image'], dbs['image'], "Hello world", isSpoil=True)
parse.JsonRichParse(img)

vid = app.sendVideo(GUID, dbs['video'], dbs['video'], isSpoil=False)
parse.JsonRichParse(vid)

mus = app.sendMusic(GUID, dbs['music'], dbs['music'], "Its make me Happy !", 321)
parse.JsonRichParse(mus)

voice = app.sendVoice(GUID, dbs['voice'], dbs['voice'], "Nice to Meet you !", 43)
parse.JsonRichParse(voice)
