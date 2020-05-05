import discord
from discord.ext import commands

class Commands(commands.Cog):
	def __init__(self, client):
		self._client = client

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, context, amount=1000):
		await context.channel.purge(limit=amount)

	@commands.command()
	async def ping(self, context):
		await context.send(f'Pong! {round(self._client.latency * 1000)} ms')

	@commands.command()
	async def kick(self, context, member: discord.Member, *, reason=None):
		await member.kick(reason=reason)
		await context.send(f'Kicked {member.mention}')

	@commands.command()
	async def ban(self, context, member: discord.Member, *, reason=None):
		await member.ban(reason=reason)
		await context.send(f'Banned {member.mention}')

	@commands.command()
	async def unban(self, context, *, member):
		banned_users = await context.guild.bans()
		member_name, member_discriminator = member.split('#')

		for ban_entry in banned_users:
			user = ban_entry.user

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await context.guild.unban(user)
				await context.send(f'Unbanned {user.mention}')
				return

def setup(client):
	client.add_cog(Commands(client))
