from QiRub import ClientMessenger

AUTH = ""
KEY = ""

app = ClientMessenger(AuthToken=AUTH, PrivateKey=KEY)

msgset = set()

while 1:
    for msg in app.onMessage():
        text = msg.text
        chat = msg.chatId
        msgid = msg.messageId

        if not msgid in msgset:
            msgset.add(msgid)

            if text == "/start":
                app.sendMessage(chat, "Hello QiRub World !", msgid)
            
            elif text.startswith("say"):
                repeater = text.replace("say ", "")

                if repeater in ("say", "", " "):
                    app.sendMessage(chat, "Error: Cannot get Text in front of `say`", msgid)
                else:
                    app.sendMessage(chat, repeater, msgid)
        else:
            msgset.add(msgid)
