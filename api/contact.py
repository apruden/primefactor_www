class ContactHandler(object):

    def __init__(self, request, response):
        self.request = request
        self.response = response

    def handle(self):
        if self.request.method == 'POST':
            return self.post()
        elif self.request.method == 'GET':
            return self.get()

    def post(self):
        self._send_notification_email(self.request.POST)
        return webapp2.redirect('/send_success')

    def _send_notification_email(self, data):
        logging.info('received contact message from %s. sending notification.' % (data['email'],))
        message = mail.EmailMessage(sender=settings.sender,
                to=settings.webadmin,
                subject='New contact message')

        message.body= """
        %(name)s [%(email)s] [%(phone)s]

        %(message)s
        """ % data
        message.send()


def handle():
    return ContactHandler(request, response).handle()
