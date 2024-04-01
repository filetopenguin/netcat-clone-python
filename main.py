import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
# Librarys

# execute recieves a command, runs it, and returns the output
# as a string
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    # runs a command shell, returns the output of the comman
    output = subprocess.check_output(shlex.split(cmd), stderr = subprocess.STDOUT)
    return output.decode()

class NetCat:
    # 1. initalizing constructor class, 
    # the parameters are command-line arguement and the buffer
    def __init__ (self,args,buffer=None):
        self.args =args
        self.buffer =buffer
        # 2. create a socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    def run(self):
        if self.args.listen:
            self.listen()
            # 3. if set up listener, call listen method
        else:
            self.send()
            # 4. otherwise call the send method

    def send(self):
        # 1.
        self.socket.connect((self.args.target,self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        # 2.
        try:
            # 3.
            while True:
                recv_len =1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        # 4. 
                        break
                    if response:
                        print(response)
                        buffer = input('> ')
                        buffer += '\n'
                    # 5.
                    self.socket.send(buffer.encode())
        # 6.
        except KeyboardInterrupt:
            print('User Terminated...')
            self.socket.close()
            sys.exit()


if __name__ == '__main__':
    # 1.building a command line interface
    parser = argparse.ArgumentParser(
        description='Python Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # 2. an example
        epilog=textwrap.dedent('''Example: 2
netcat.py -t 192.168.1.108 -p 5555 -l -c #
command shell
netcat.py -t 192.168.1.108 -p 5555 -l -
u=mytest.txt # upload to file
netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat
/etc/passwd\" # execute command
echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135
# echo text to server port 135
netcat.py -t 192.168.1.108 -p 5555 # connect to
server
'''))
    # 3. add six arguements for program behaviour
    # 'c' - interactive shell setup (listen)
    # 'e' - executes specific command (listen)
    # 'p' - specify communication port (target)
    # 't' - specify target IP (target)
    # 'u' - specify name of file to upload (listen)
    parser.add_argument('-c', '--command',
                        action='store_true', help='command shell')
    parser.add_argument('-e','--execute',help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true',
                        help='listen')
    parser.add_argument('-p','--port',type=int,default=5555, help='specified port')
    parser.add_argument('-t','--target',default='192.168.1.203',
                        help ='specified IP')
    parser.add_argument('-u','--upload', help='upload file')
    args = parser.parse_args()

    # 4. if setting up a listener, invoke with empty buffer
    if args.listen:
        buffer = ''
    # othewise send buffer content from stdin..
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args,buffer.encode())
    nc.run()
    