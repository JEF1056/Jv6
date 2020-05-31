function setGuild(guild_id, guild_name, guild_settings,guild_icon_hash) {
    console.log(guild_id)
    console.log(guild_name)
    console.log(guild_settings)
    var img_url = "https://cdn.discordapp.com/icons/"+guild_id+"/"+guild_icon_hash+".png?size=512"
    console.log(img_url)
    var date = new Date(guild_settings["t1"] * 1000);
    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();
    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    document.getElementById("settings_small_text").innerHTML = "Most recent timestamp: "+formattedTime+"\nSave file version: "+guild_settings["user_version"];
    document.getElementById('Guild Name').innerHTML = guild_name;
    document.getElementById("Guild Img").src =img_url;
    document.getElementById("temperature").innerHTML = guild_settings[guild_id]["settings"]["temperature"];
    document.getElementById("top_k").innerHTML = guild_settings[guild_id]["settings"]["top_k"];
    document.getElementById("top_p").innerHTML = guild_settings[guild_id]["settings"]["top_p"];
    document.getElementById("seed").innerHTML = guild_settings[guild_id]["settings"]["seed"];
    document.getElementById("auto_seed").innerHTML = guild_settings[guild_id]["settings"]["auto_seed"];
    document.getElementById("max_history").innerHTML = guild_settings[guild_id]["settings"]["max_history"];
    document.getElementById("max_length").innerHTML = guild_settings[guild_id]["settings"]["max_length"];
    document.getElementById("no_sample").innerHTML = guild_settings[guild_id]["settings"]["no_sample"];
}