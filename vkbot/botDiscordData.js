const {settings} = require('./settings')
const fetch = require('node-fetch')

class botDiscord{
    
    constructor(){

    this.command_prefix='!'

    this.commands = [
        'join',
        'play',
        'volume',
        'stop',
        'golosovanie',
        'playlist',
        'next',
        'showList',
        'add',
        'drop',
    ]
    }


    handleMessage(text){
        let args;
        this.commands.forEach(element => {
            if (text.startsWith(this.command_prefix+element)) {
                args = this._parseCommand(element,text)        
                //тогда мы должны запустить команду в python

                
                

                
            }
        });
        return this.fetchAsync(args)
    }

    _parseCommand(command,text){
        let _args = []


        _args =_args.concat(text.substr(1).split(" "))
        let parsed_args=[]

        _args.map((value) =>{
        if(value !== ''){
            parsed_args.push(value)
        } 
        })
        
        return parsed_args
    }

    async fetchAsync(args) {
        const command = {
            'command':args
        }
        try {
            const response = await fetch(`${settings.URL}event?authkey=${settings.AUTHKEY}`, {
                method: 'post',
                body: JSON.stringify(command),
                headers: {
                    'Content-Type':'application/json',
                    'Accept': '*/*',
                    'Accept-Encoding':'gzip, deflate, br'
                }
            })
            
            const json = await response.json()
        
        //console.log(json);
        if (json.status=='failed') { 
            return `Ошибка: ${json.message}`
        }
        else {
            //console.log(typeof json.message);
            //console.log(json.message);
            return json.message
        }
    }
        catch (e){
            console.error(e);
        }
    }
}


module.exports = botDiscord