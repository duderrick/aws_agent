"""Debugging messages"""
def message_output(response):
	"""For debugging purposes to display the response from the invoked msg."""
	for message in response['messages']:
		if isinstance(message.content, list):
			for msg in message.content:
				print('\t\t', msg)
		else:
			print('\t', message)