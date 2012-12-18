
from helpers.signals import Signal

def send_signal(sig, sender, kwargs):
    s = Signal(sig)
    s.send(sender=sender, **kwargs)
    
if __name__ == '__main__':
    from optparse import OptionParser
    import sys, yaml

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-f', '--file', dest='file', help='file to read signal data', default='')
        
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])
    if options.file:
        d = yaml.load(open(options.file).read())
        send_signal(d['signal'], d['sender'], d['kwargs'])
        
    