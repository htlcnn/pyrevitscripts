class HTLAddin():
    def __init__(self, name):
        self.name = name

    def check_license(self, key):
        import urllib2
        res = urllib2.urlopen('http://101.99.13.191/license?addin=XXX&hdd=ABC&key=XYZ')
        msg = res.read().strip()
        if self.name == 'OK':
            return True
        else:
            return False

    def execute(self):
        if self.check_license('fdjsklj'):
            print('pass')
        else:
            print('fail')

