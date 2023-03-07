from NMtcpdump import *
from NMdhcpserver import *
from NMsnmp import *
from NMgithub import *

def main():
    run_NMsnmp()
    run_NMtcpdump()
    run_NMgithub()
    run_NMdhcpserver()

if __name__ == '__main__':
    main()