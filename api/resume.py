class ResumeHandler(object):

    def __init__(self, request, response):
        self.request = request
        self.response = response

    def handle(self):
        if self.request.method == 'POST':
            return self.post()
        elif self.request.method == 'GET':
            return self.get()

    def post(self):
        import datetime
        data = json.loads(self.request.body)
        entry = DataEntry(id='resume:%s' % data['email'], type='resume', data=self.request.body)
        entry.put()
        self._send_notification_email(data['email'])
        return webapp2.redirect('/send_success')

    def _send_notification_email(self, email):
        logging.info('received resume from %s. sending notification.' % (email,))
        message = mail.EmailMessage(sender=settings.sender,
                to=settings.webadmin,
                subject='New resume')

        message.body= """
        %s sent a resume at http://www.primefactorsolutions.com/intra/resumes
        """ % (email,)

        message.send()

    def get(self):
        import json
        email = self.request.get('email')
        if email:
            entry = ndb.Key(DataEntry, 'resume:%s' % email).get()
            doc = JINJA_SITE_ENVIRONMENT.get_template('/templates/resume.html').render(json.loads(entry.data))
            self.response.write(doc)
        else:
            res = [dict(id=entry.key.id()) for entry in DataEntry.query() if entry.key.id().startswith('resume:')]
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(res))


def handle():
    return ResumeHandler(request, response).handle()

