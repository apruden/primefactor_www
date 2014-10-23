class ApplyHandler(object):

	def __init__(self, request, response):
		self.request = request
		self.response = response

	def handle(self):
		if self.request.method == 'POST':
			return self.post()
		elif self.request.method == 'GET':
			return self.get()

	def post(self):
		data = json.loads(self.request.body)
		entry = DataEntry(id='application:%s' % data['email'], type='application', data=self.request.body)
		entry.put()
		self._send_notification_email(data['email'])

	def _send_notification_email(self, email):
		logging.info('received application from %s. sending notification.' % (email,))
		message = mail.EmailMessage(sender=settings.sender,
				to=settings.webadmin,
				subject='New job application')

		message.body= """
		A new job application was received at http://www.primefactor.solutions/api/apply?email=%s
		""" % (email,)

		message.send()

	def get(self):
		email = self.request.get('email')

		if not email:
			return

		entry = ndb.Key(DataEntry, 'application:%s' % email).get()
		doc = JINJA_SITE_ENVIRONMENT.get_template('/templates/application').render(json.loads(entry.data))
		self.response.write(doc)


ApplyHandler(request, response).handle()
