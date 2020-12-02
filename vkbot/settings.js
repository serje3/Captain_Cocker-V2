module.exports.settings = {
    //to auth vk api
    TOKEN: process.env.TOKEN_VK,
    GROUP_ID:process.env.GROUPID,
    API_MODE: "parallel",

    //fetch()
    URL:'https://0.0.0.0:'+process.env.PORT+'/',
    AUTHKEY: process.env.AUTHKEY

}