class MessageHandler:
	def __init__(self):
		self._all_channel_messages = []
		self._spammer_authors = []

	def append(
		self,
	   	channel_message,
	   	channel_author
   	):
		self._all_channel_messages.append({
			'author': channel_author,
			'message': channel_message
		})

	@property
	def spammer_authors(self):
		return self._spammer_authors

	def _author_is_spamming(self, author):
		if (len(self._all_channel_messages) >= 4):
			last_four_messages = self._all_channel_messages[-4:]
			author_messages = filter(
				lambda item: item['author'] == author,
				last_four_messages
			)

			return len(list(author_messages)) >= 4

	def check_if_author_is_spamming(self, author):
		if self._author_is_spamming(author):
			self._spammer_authors.append(author)
			return True
		return False

	def find_spammer_author_in_list(self, author):
		spammer = filter(
			lambda spammer_author: spammer_author == author,
			self._spammer_authors
		)
		return list(spammer)