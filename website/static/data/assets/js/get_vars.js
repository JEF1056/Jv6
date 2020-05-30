function setGuild(guild_settings) {
    document.getElementById("temperature").innerHTML = guild_settings["temperature"];
    document.getElementById("top_k").innerHTML = guild_settings["top_k"];
    document.getElementById("top_p").innerHTML = guild_settings["top_p"];
    document.getElementById("seed").innerHTML = guild_settings["seed"];
    document.getElementById("auto_seed").innerHTML = guild_settings["auto_seed"];
    document.getElementById("max_history").innerHTML = guild_settings["max_history"];
    document.getElementById("max_length").innerHTML = guild_settings["max_length"];
    document.getElementById("no_sample").innerHTML = guild_settings["no_sample"];
}