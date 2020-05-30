function setGuild(guild_id, guild_name, guild_settings,guild_icon_hash) {
    console.log(guild_id)
    console.log(guild_name)
    console.log(guild_settings)
    var img_url = concat("https://cdn.discordapp.com/icons/",guild_id,"/",guild_icon_hash,".png?size=512")
    console.log(img_url)
    document.getElementById('Guild Name').innerHTML = guild_name
    document.getElementById("Guild Img").src =img_url
    document.getElementById("temperature").innerHTML = guild_settings[guild_id][1]["temperature"];
    document.getElementById("top_k").innerHTML = guild_settings[guild_id][1]["top_k"];
    document.getElementById("top_p").innerHTML = guild_settings[guild_id][1]["top_p"];
    document.getElementById("seed").innerHTML = guild_settings[guild_id][1]["seed"];
    document.getElementById("auto_seed").innerHTML = guild_settings[guild_id][1]["auto_seed"];
    document.getElementById("max_history").innerHTML = guild_settings[guild_id][1]["max_history"];
    document.getElementById("max_length").innerHTML = guild_settings[guild_id][1]["max_length"];
    document.getElementById("no_sample").innerHTML = guild_settings[guild_id][1]["no_sample"];
}