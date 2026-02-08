def setup(bot):
    @bot.command()
    async def hello(ctx):
        await ctx.send("Plugin system working ✅")
