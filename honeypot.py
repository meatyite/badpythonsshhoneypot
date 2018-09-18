# -*- coding: utf-8 -*-

from twisted.conch import avatar, recvline
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import factory, keys, session
from twisted.conch.insults import insults
from twisted.cred import portal, checkers
from twisted.internet import reactor
from zope.interface import implements


class SSHDemoProtocol(recvline.HistoricRecvLine):
    def __init__(self, user):
       self.user = user

    def connectionMade(self):
        recvline.HistoricRecvLine.connectionMade(self)
        self.terminal.nextLine()
        self.terminal.write("Linux server 4.13.0-32-generic #35~16.04.1-Ubuntu SMP Thu Jan 25 10:13:43 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux\n\nUbuntu 16.04.1\n\nWelcome to Ubuntu!\n* Documentation:  https://help.ubuntu.com/\n\n")
        self.terminal.nextLine()
        self.showPrompt()

    def showPrompt(self):
        self.terminal.write("root@server:~# ")

    def getCommandFunc(self, cmd):
        return getattr(self, 'do_' + cmd, None)

    def lineReceived(self, line):
        line = line.strip()
        if line:
            print line
            f = open('logfile.log', 'w')
            f.write(line + '\n')
            f.close
            cmdAndArgs = line.split()
            cmd = cmdAndArgs[0]
            args = cmdAndArgs[1:]
            func = self.getCommandFunc(cmd)
            if func:
                try:
                    func(*args)
                except Exception, e:
                    self.terminal.write("Error: %s" % e)
                    self.terminal.nextLine()
            else:
                self.terminal.write(cmd + ": command not found")
                self.terminal.nextLine()
        self.showPrompt()

    def do_echo(self, *args):
        self.terminal.write(" ".join(args))
        self.terminal.nextLine()

    def do_whoami(self):
        self.terminal.write("root")
        self.terminal.nextLine()

    def do_exit(self):
        self.terminal.loseConnection()


    def do_uname(self, *args):
        if not(args):
            self.terminal.write("Linux")
            self.terminal.nextLine()
        elif args[0].lower().startswith("-a") or args[0].lower().startswith("--all"):
            self.terminal.write("Linux server 4.13.0-32-generic #35~16.04.1-Ubuntu SMP Thu Jan 25 10:13:43 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux")
            self.terminal.nextLine()
        else:
            self.terminal.write("uname: invalid option -- " + args[0] + "\nTry 'uname --help' for more information.")
            self.terminal.nextLine()

    def do_cat(self, *args):
        if args:
            if args[0] == "/proc/version":
                self.terminal.write("Linux version 4.13.0-32-generic (buildd@lgw01-amd64-004) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.5)) #35~16.04.1-Ubuntu SMP Thu Jan 25 10:13:43 UTC 2018")
                self.terminal.nextLine()
            elif args[0] == "/proc" or args[0] == "/proc/" or args[0] == "/etc" or args[0] == "/etc/" or args[0] == "/":
                self.terminal.write("cat: " + args[0] + ": Is a directory")
                self.terminal.nextLine()
            else:
                self.terminal.write("cat: " + args[0] + ": No such file or directory")
                self.terminal.nextLine()

    def do_w(self):
        self.terminal.write(" 17:22:40 up 22:38,  1 user,  load average: 0.77, 0.93, 0.86\nUSER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT\nroot     tty7     :0               א'18   10:14m 10:16   0.66s /usr/lib/gnome-session/gnome-session-binary --session=pantheon\nroot     tty7     :0               א'18   10:14m 10:16   0.66s w")
        self.terminal.nextLine()
class SSHDemoAvatar(avatar.ConchUser):
    implements(ISession)


    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})


    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(SSHDemoProtocol, self)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))


    def getPty(self, terminal, windowSize, attrs):
        return None


    def execCommand(self, protocol, cmd):
        raise NotImplementedError()


    def closed(self):
        pass


class SSHDemoRealm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser in interfaces:
            return interfaces[0], SSHDemoAvatar(avatarId), lambda: None
        else:
            raise NotImplementedError("No supported interfaces found.")
def getRSAKeys():


    with open('id_rsa') as privateBlobFile:
        privateBlob = privateBlobFile.read()
        privateKey = keys.Key.fromString(data=privateBlob)


    with open('id_rsa.pub') as publicBlobFile:
        publicBlob = publicBlobFile.read()
        publicKey = keys.Key.fromString(data=publicBlob)


    return publicKey, privateKey


if __name__ == "__main__":
    sshFactory = factory.SSHFactory()
    sshFactory.portal = portal.Portal(SSHDemoRealm())


users = {'root': 'password'}
sshFactory.portal.registerChecker(
    checkers.InMemoryUsernamePasswordDatabaseDontUse(**users))
pubKey, privKey = getRSAKeys()
sshFactory.publicKeys = {'ssh-rsa': pubKey}
sshFactory.privateKeys = {'ssh-rsa': privKey}
reactor.listenTCP(2222, sshFactory)
reactor.run()
