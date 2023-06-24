import discord
from discord.ext import commands

# Set up bot client
bot = commands.Bot(command_prefix='!')

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')

# Command: Ping
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Calculate bot's latency in milliseconds
    await ctx.send(f'Pong! Latency: {latency}ms')

# Command: Kick
@bot.command()
@commands.has_permissions(kick_members=True)  # Restrict command to users with kick_members permission
async def kick(ctx, member: discord.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} has been kicked.')

# Command: Ban
@bot.command()
@commands.has_permissions(ban_members=True)  # Restrict command to users with ban_members permission
async def ban(ctx, member: discord.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned.')

# Command: Quote
@bot.command()
async def quote(ctx, channel: discord.TextChannel, message_id: int):
    try:
        message = await channel.fetch_message(message_id)
        await ctx.send(f'Quoted message: {message.content}')
    except discord.NotFound:
        await ctx.send('Message not found.')

# Event: Member joins the server
@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.channels, name='welcome')
    await welcome_channel.send(f'Welcome, {member.mention}! Enjoy your stay.')

# Event: Member leaves the server
@bot.event
async def on_member_remove(member):
    goodbye_channel = discord.utils.get(member.guild.channels, name='goodbye')
    await goodbye_channel.send(f'Goodbye, {member.name}. We will miss you.')

# Command: Reaction Roles
@bot.command()
async def reaction_roles(ctx):
    message = await ctx.send('React with ✅ to get the "Member" role.')
    await message.add_reaction('✅')

    def check(reaction, user):
        return str(reaction.emoji) == '✅' and reaction.message == message

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        role = discord.utils.get(ctx.guild.roles, name='Member')
        await user.add_roles(role)
        await ctx.send(f'{user.mention} has been assigned the "Member" role.')
    except TimeoutError:
        await ctx.send('No reaction received within 60 seconds.')

# Command: Create Poll
@bot.command()
async def create_poll(ctx, question, *options):
    if len(options) < 2 or len(options) > 9:
        await ctx.send('Please provide 2 to 9 options for the poll.')
    else:
        poll_embed = discord.Embed(title='Poll', description=question, color=discord.Color.blue())
        for i, option in enumerate(options):
            poll_embed.add_field(name=f'Reaction {i+1}', value=option, inline=False)

        poll_message = await ctx.send(embed=poll_embed)

        for i in range(len(options)):
            await poll_message.add_reaction(chr(0x1f1e6 + i))  # Unicode flag reactions

# Run the bot
bot.run('YOUR_BOT_TOKEN')
