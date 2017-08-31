import os
import sys

class ExitRelay():
    def __init__(self, exit_relay='', exit_address='', exit_fingerprint='', exit_nickname='', exit_locale=''):
        self.exit_relay = exit_relay
        self.exit_address = exit_address
        self.exit_fingerprint = exit_fingerprint
        self.exit_nickname = exit_nickname
        self.exit_locale = exit_locale

    def __str__(self):
        return('\nExit relay for our connection to %s' % (self.exit_relay) +
                '\n address: %s' % (self.exit_address) +
                '\n fingerprint: %s' % (self.exit_fingerprint) +
                '\n nickname: %s' % (self.exit_nickname) +
                '\n locale: %s' % (self.exit_locale))


    def save(self):
        try:
            test = '/home/asigan/torcurl2/torcurl2/cache/exit_relay.info'
            # source = os.getcwd()
            #f = open((source + str('/main/cache/exit_relay.info')), "wb")
            f = open(test, 'wb')
            f.write('Exit relay for our connection to %s' % (self.exit_relay))
            f.write('\n address: %s' % (self.exit_address))
            f.write('\n fingerprint: %s' % (self.exit_fingerprint) )
            f.write('\n nickname: %s' % (self.exit_nickname))
            f.write('\n locale: %s' % (self.exit_locale))
            print('TorPyCurl Status: Information Succcessfully Retrieved')
        except:
            print('Something went wrong while trying to save the ExitRelay information...')
        finally:

            f.close()


