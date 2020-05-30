function setGuild(guild_settings[1]) {
    document.getElementById("temperature").innerHTML = guild_settings[1]["temperature"];
    document.getElementById("top_k").innerHTML = guild_settings[1]["top_k"];
    document.getElementById("top_p").innerHTML = guild_settings[1]["top_p"];
    document.getElementById("seed").innerHTML = guild_settings[1]["seed"];
    document.getElementById("auto_seed").innerHTML = guild_settings[1]["auto_seed"];
    document.getElementById("max_history").innerHTML = guild_settings[1]["max_history"];
    document.getElementById("max_length").innerHTML = guild_settings[1]["max_length"];
    document.getElementById("no_sample").innerHTML = guild_settings[1]["no_sample"];
}