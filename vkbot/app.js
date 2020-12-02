const {settings} = require('./settings')
const { VK } = require('vk-io')
const botDiscord = require('./botDiscordData')
const toDiscord = new botDiscord() 
const vk = new VK({
    token: settings.TOKEN,
    pollingGroupId: settings.GROUP_ID,
    apiMode: settings.API_MODE
})

vk.updates.use(async (msg,next)=>{
    if(msg.senderType !== 'user') return false;
    if(msg.peerType !== 'chat'){
        msg.send("Я работаю только в беседе(Или не работаю вообще). Добавь меня в беседу")
        return false
    }

    if (msg.text !== undefined) {
        console.log(msg);
        console.log(msg.senderId)

        if (msg.text.trim()==='!nigger'){
            vk.api.messages.removeChatUser({
                chat_id: msg.chatId,
                user_id: msg.senderId,
            });
        }
        else {
            msg.text.trim()[0] === '!' ? toDiscord.handleMessage(msg.text.trim()).then((value) => {
                msg.send(value)
            }).catch(e => console.log(e)) : null;
        }
    }
    
    next();
})







vk.updates.start().catch(console.error);
console.log('[NodeJS][VK] - Logged on as Captain Cocker');
console.log('-------------');