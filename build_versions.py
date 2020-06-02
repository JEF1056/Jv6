from discord import Embed
def version_message(version, client, prefix):
    if version == 0:
        embed=Embed(title="New Jade Version!", description="Jade V6",color=0x80ff80)
        jess=client.get_user(249024790030057472)
        jade=client.get_user(410253782828449802)
        embed.set_author(name=str(jess), icon_url=str(jess.avatar_url), url="https://j-fan.ml")
        embed.set_thumbnail(url=str(jade.avatar_url))
        embed.add_field(name="New Features", value="This new version of jade is based on [GPT-2](https://openai.com/blog/better-language-models/)," +
        " and is able to acheive a stunning 88% accuracy in tests against real discord data. Alongside with the new, more powerful model, Jade now comes" +
        " with more settings than ever before (try typing `"+prefix+"-s`), and I hope that with these upgrades, Jade is better than ever", inline=False)
        embed.add_field(name="How to use?", value="Pretty simple! to get started, try typing a message in the format `"+prefix+"[message]`, such as " +
        " `"+prefix+"how's your day been?`. She'll respond and record the history. She will learn over time as you speak to her more and get acquainted!" +
        " type `"+prefix+"-h` for a help menu! More documentation can be found on her [github](https://github.com/JEF1056/Jv6).")
        embed.add_field(name="Advanced Settings", value="Lots of advanced settings exist in this new version of Jade, accessable via `"+prefix+"-s`." +
        " Most of them should work very well as-is, but you're free to change them any way you like. Be sure to upvote Jade on [top.gg](https://top.gg/bot/410253782828449802/vote)" +
        " to decrease your ratelimit timer and gain access to advanced settings!")
        embed.add_field(name="Conclusion", value="I'm excited to be able to deploy such an advancement to the Jade algorithm. I hope" +
        " that you'll have a great time using Jade, and look forward to your continued support! \n\n- Jess Fan\n*Solo developer of Jade*", inline=False)
        return embed
    elif version == 1:
        embed=Embed(title="Jade's Website", description="Jade V6",color=0x80ff80)
        jess=client.get_user(249024790030057472)
        jade=client.get_user(410253782828449802)
        embed.set_author(name=str(jess), icon_url=str(jess.avatar_url), url="https://j-fan.ml")
        embed.set_thumbnail(url=str(jade.avatar_url))
        embed.set_image(url="https://iili.io/JNImts.png")
        embed.add_field(name="New Features", value="Ho ho? What's this? Tired of making changes through hard-to-type commands?" +
        " Try out [Jade's Website](https://jadeai.ml)! changing settings is way easier to see and read!" +
        " Jade also now tracks more metrics and will soon be improving to a newer GPT encoder!", inline=False)
        embed.add_field(name="Conclusion", value="This is a short, small update to the Jade algorithm, but with possilbly huge implications! " +
        " Making Jade more accessable is an important aspect of Jade's goals, and i'm glad to take one more step toward it. \n\n- Jess Fan\n*Solo developer of Jade*", inline=False)
        return embed

async def make_help(dbli, client, prefix):
    embed=Embed(title="Help", description="Ah, so you don't know what you're doing.\n~~Don't worry, I don't either~~\n__                                                                          __" ,color=0x80ff80)
    embed.add_field(name=prefix+"[message]",value="Talks to Jade! (pretty simple) \n```"+prefix+"hello, how are you?```", inline=False)
    embed.add_field(name=prefix+"-h",value="Help menu (you're right here!!) \n```"+prefix+"-h```", inline=False)
    embed.add_field(name=prefix+"-v",value="[Vote for Jade!](https://top.gg/bot/410253782828449802/vote) enables settings that are supporter-only.\n```"+prefix+"-v```", inline=False)
    embed.add_field(name=prefix+"-p",value="Shows your user profile and any data Jade has collected about you! \n```"+prefix+"-p```", inline=False)
    embed.add_field(name=prefix+"-r [(optional) arg1] [(optional) arg2]",value="Reset function. Contains arguments: `history` and `settings` \n```"+prefix+"-r history settings```", inline=False)
    embed.add_field(name=prefix+"-s [setting] [value]",value="Jade's neural network settings. (no arguments for a panel) \nContains (working) arguments: `seed`,`temperature`,`top_k`,`top_p` \n```"+prefix+"-s seed 100```", inline=False)
    embed.set_image(url=await dbli.get_widget_large(client.user.id))
    return embed