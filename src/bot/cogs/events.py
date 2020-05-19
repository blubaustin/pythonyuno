import discord
from discord.ext import commands, tasks
from src.bot.utils.message_handler import MessageHandler

##class provides (on_ready, on_message)
class Events(commands.Cog):
	def __init__(self, client):
		self._client = client
		self._message_handler = MessageHandler()

	@commands.Cog.listener()
	async def on_ready(self):
		print(f'We have logged in as {self._client.user}')
		print('Ready!')
		return await self._client.change_presence(
			activity=discord.Activity(type=3, name='for Levels')
		)
	# @todo message limit
	@commands.Cog.listener()
	async def on_message(self, context):
		author = context.author.name
		author_id = context.author.id

		self._message_handler.append(context.content, author)
		if self._message_handler.check_if_author_is_spamming(author):
			if (len(self._message_handler.find_spammer_author_in_list(author)) > 1):
				pass
			user = await self._client.fetch_user(author_id)
			await context.channel.send(f'{user.mention} look #rules 13')

def setup(client):
	client.add_cog(Events(client))
