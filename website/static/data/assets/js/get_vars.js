function setGuild(guild_id, guild_name, guild_settings) {
    console.log(guild_id)
    console.log(guild_name)
    console.log(guild_settings)
    document.getElementById('Guild Name').innerHTML = guild_name
    document.getElementById("temperature").innerHTML = guild_settings[guild_id[0]][1]["temperature"];
    document.getElementById("top_k").innerHTML = guild_settings[guild_id[0]][1]["top_k"];
    document.getElementById("top_p").innerHTML = guild_settings[guild_id[0]][1]["top_p"];
    document.getElementById("seed").innerHTML = guild_settings[guild_id[0]][1]["seed"];
    document.getElementById("auto_seed").innerHTML = guild_settings[guild_id[0]][1]["auto_seed"];
    document.getElementById("max_history").innerHTML = guild_settings[guild_id[0]][1]["max_history"];
    document.getElementById("max_length").innerHTML = guild_settings[guild_id[0]][1]["max_length"];
    document.getElementById("no_sample").innerHTML = guild_settings[guild_id[0]][1]["no_sample"];
}