const {settings} = require('./settings')
const { VK, Keyboard } = require('vk-io')
const { HearManager } = require('@vk-io/hear')
let chats = require('./chats.json')
const fs = require('fs')
const botDiscord = require('./botDiscordData')
const toDiscord = new botDiscord() 
const vk = new VK({
    token: settings.TOKEN,
    pollingGroupId: settings.GROUP_ID,
    apiMode: settings.API_MODE
})



const hearManager = new HearManager();

vk.updates.on('message_new', (context, next) => {
	const { messagePayload } = context;

	context.state.command = messagePayload && messagePayload.command
		? messagePayload.command
		: null;

	return next();
});

vk.updates.on('message_new', hearManager.middleware);

// Simple wrapper for commands
const hearCommand = (name, conditions, handle) => {
	if (typeof handle !== 'function') {
		handle = conditions;
		conditions = [`/${name}`];
	}
	console.log(name,conditions,handle)
	if (!Array.isArray(conditions)) {
		conditions = [conditions];
	}

	hearManager.hear(
		[
			(text, { state }) => (
				state.command === name
			),
			...conditions
		],
		handle
	);
};




vk.updates.use(async (msg,next)=>{
    if(msg.senderType !== 'user') return false;
    if(msg.peerType !== 'chat'){
        msg.send("Я работаю только в беседе(Или не работаю вообще). Добавь меня в беседу")
        return false
    }

    if (msg.text !== undefined) {
        // console.log(msg);
        // console.log(msg.senderId)
		const chat = chats.filter(item => item.chatId === msg.chatId)[0]
    	if (!chat){

			chats.push({
				chatId:msg.chatId,
				channel: null,
				inchannel: false,
			})
			fs.writeFileSync('vkbot/chats.json', JSON.stringify(chats,null,'\t'))
			console.log(chats)
    	}

        if (msg.text.trim().startsWith('!nigger')){
            vk.api.messages.removeChatUser({
                chat_id: msg.chatId,
                user_id: msg.senderId,
            }).catch(e => msg.send("Сучька"));
        }
        else {
            msg.text.trim()[0] === '!' ? toDiscord.handleMessage(msg.text.trim()).then((value) => {
                msg.send(value)
            }).catch(e => console.log(e)) : null;
        }
    }
    
    next();
})



hearCommand('start', (context, next)=>{
    context.state.command = 'help';

	return Promise.all([
		context.send('Але'),

		next()
	]);
})


hearCommand('help', async (context) => {
	await context.send({
		message: `
			Список команд
			/setchannel - установить главный канал
			!join - присоединиться к голосовому чату в дискорде
			!playlist - Включить плейлист в голосовом чате в дискорде
			!showList - Показать список песен
			!nigger - стать счастливым, избравиться от депрессии, получить много денег, нобелевскую премию, жену, сына, дочь, 10 килограммого сома из реки Ахтуба, преисполниться в этой жизни, постичь дзен, прекратить все войны, болезни, нищеты, воровство, несправедливость
		`,
		keyboard: Keyboard.builder()
			.textButton({
				label: 'Присоединиться к голосовому чату',
				payload: {
					command: 'join'
				},
                color: Keyboard.POSITIVE_COLOR
			})
			.row()
			.textButton({
				label: 'Включить плейлист',
				payload: {
					command: 'playlist'
				},
				color: Keyboard.PRIMARY_COLOR
			})
			.textButton({
				label: 'Остановить и выйти',
				payload: {
					command: 'stop'
				},
				color: Keyboard.PRIMARY_COLOR
			}).row()
            .textButton({
				label: 'nigger',
				payload: {
					command: 'nigger'
				},
				color: Keyboard.NEGATIVE_COLOR
			}),
	});
});

hearCommand('setchannel', ['setchannel',/\/setchannel ([a-z]|[а-я])+/g],async (msg)=>{
	// msg.text.trim().slice()
	console.log(msg.text)
	console.log(1,msg.text.trim().slice(12))
	console.log(2, msg.text.trim().slice(11))

	chats = chats.map(item =>{
		if(item.chatId === msg.chatId) {
			item.channel = msg.text.trim().slice(12).trim()
		}
		return item
		})
	fs.writeFileSync('vkbot/chats.json', JSON.stringify(chats,null,'\t'))

})

hearCommand('join', async (msg)=>{
	const chat = chats.filter(item => item.chatId === msg.chatId)[0]
	if (chat.channel === null){
		msg.send("Основной голосовой канал не указан, для этого /setchannel название канала")
	}
	else {
		toDiscord.handleMessage('!join ' + chat.channel).then((value) => {
			msg.send(value)
			chats = chats.map(item =>{
				if(item.chatId === msg.chatId) {
					item.inchannel = true
				}
				return item
			})
			fs.writeFileSync('vkbot/chats.json', JSON.stringify(chats,null,'\t'))
		}).catch(e => console.log(e))
	}
	})




hearCommand('playlist', async (msg)=>{

	const chat = chats.filter(item => item.chatId === msg.chatId)[0]

	if (chat.inchannel===false && chat.channel !== null){
		msg.send("Голосовой канал не определен, подключаюсь к основному")

		toDiscord.handleMessage('!join ' + chat.channel).then((value) => {
			msg.send(value)
			chats = chats.map(item =>{
				if(item.chatId === msg.chatId) {
					item.inchannel = true
				}
				return item
			})
			fs.writeFileSync('vkbot/chats.json', JSON.stringify(chats,null,'\t'))


		}).then( value =>
			toDiscord.handleMessage('!playlist').then((value1) => {
				msg.send(value1)
			}).catch(e => console.log(e))
		).catch(e => console.log(e))
		msg.send("Играет плейлист")
	} else if(chat.inchannel===false){
		msg.send("Нет подключения к голосовому чату")
	} else{
		toDiscord.handleMessage('!playlist').then((value) => {
			msg.send(value)
		}).catch(e => console.log(e))
	}


})

hearCommand('stop', async (msg)=>[
	toDiscord.handleMessage('!stop ').then((value) => {
		msg.send(value)

		chats = chats.map(item =>{
			if(item.chatId === msg.chatId) {
				item.inchannel = false
			}
			return item
		})
		fs.writeFileSync('vkbot/chats.json', JSON.stringify(chats,null,'\t'))
	}).catch(e => console.log(e))
])

hearCommand('nigger', async (context) =>{
    vk.api.messages.removeChatUser({
                chat_id: context.chatId,
                user_id: context.senderId,
            }).catch(e => context.send("Сучька"));
})




vk.updates.start().catch(console.error);
console.log('[NodeJS][VK] - Logged on as Captain Cocker');
console.log('-------------');