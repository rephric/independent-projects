import click
import nmap
import json
import xmltodict

def nmapScan(tgthost, tgtport, json, file):
    if tgthost and tgtport:
        nmap = nmap.PortScanner()
        nmap.scan(tgthost, tgtport)
    pass

def xmltoJson():
    pass

@click.group()
@click.pass_context
def main(self):
    """
    Tools created for a independent study project at Wentworth Institute of Technology.
    """
    pass

@main.command()
@click.option('--tgthost', '-h', type=str, help='Target Host(s)', multiple=True)
@click.option('--tgtport', '-p', type=str, help='Target Port(s)', multiple=True)
@click.option('--json', '-j', is_flag=True, help='Outputs to json')
@click.option('--file', '-f', is_flag=True, help='Creates a file with the output')
@click.pass_context
def nmap(self, tgthost, tgtport, json, file):
    print(tgtport)
    if not json and file:
        for tgthost in tgthost:
            for tgtport in tgtport:
                nmapScan(tgthost,tgtport, file)
    if json and file:
        for tgthost in tgthost:
            for tgtport in tgtport:
                nmapScan(tgthost,tgtport,json,file)
        nmap = nmap.PortScanner()
        nmap.scan(tgtHost,tgtPort)
        state = scan[tgthost]['tcp'][int(tgtPort)]['state']


#@main.command()
#@click.option('')
def bf(self):
    """
    Different Bruteforce mechanisms.
    * Dictionary Attack
    """

if __name__ == '__main__':
    main()
