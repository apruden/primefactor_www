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
        import datetime
        uploaded = self.request.POST['file']
        entry = DataEntry(id='application:%s' % self.request.POST['email'],
            file=self.request.get('file'),
            message=str(self.request.POST['message']),
            sent=datetime.datetime.now(),
            filename=str(uploaded.filename))
        entry.put()
        self._send_notification_email(self.request.POST['email'])
        return webapp2.redirect('/send_success')

    def _send_notification_email(self, email):
        logging.info('received application from %s. sending notification.' % (email,))
        message = mail.EmailMessage(sender=settings.sender,
                to=settings.webadmin,
                subject='New job application')

        message.body= """
        %s sent a new job application at http://www.primefactorsolutions.com/intra/applications
        """ % (email,)

        message.send()

    def get(self):
        import json
        
        id = self.request.get('id')
        download = self.request.get('download')

        if not id: # list all
            res = [dict(id=entry.key.id(),
                email=entry.key.id(),
                message=entry.message,
                filename=entry.filename) for entry in DataEntry.query() if entry.key.id().startswith('application:')]
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(res))
            return

        entry = ndb.Key(DataEntry, id).get()

        if download:
            self.response.headers['Content-Disposition'] = 'attachment; filename=%s;' % (entry.filename,)
            self.response.write(entry.file)
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(dict(id=entry.key.id(),
                email=entry.key.id(),
                message=entry.message,
                filename=entry.filename)))

def handle():
    return ApplyHandler(request, response).handle()