function setGuild(guild_settings) {
    for (var key in guild_settings) {document.getElementById(key).innerHTML = guild_settings[key];}
}   