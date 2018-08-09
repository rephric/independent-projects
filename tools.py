import click
import nmap
import json
import xmltodict

def nmapScan(tgthost, tgtport, js):
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(0)
    if tgthost and tgtport and not js:
        nm.scan(tgthost, tgtport)
        state = nm[str(tgthost)]['tcp'][int(tgtport)]['state']
        print(" [*] " + tgthost + " tcp/"+tgtport +" " +state)
    if js:
        xml = nm.scan(tgthost, tgtport)
        print(json.dumps(xml))
        with open('nmap_output.xml', 'a+') as outfile:
            json.dump(xml, outfile)


@click.group()
@click.pass_context
def main(self):
    """
    Tools created for a independent study project at Wentworth Institute of Technology.
    """
    pass

@main.command()
@click.option('--nmap', is_flag=True, help='Runs nmap scan')
@click.option('--tgthost', '-h', type=str, help='Target Host(s)', multiple=True)
@click.option('--tgtport', '-p', type=str, help='Target Port(s)', multiple=True)
@click.option('--js', '-j', is_flag=True, help='Outputs to json and creates a file in current directory')
@click.pass_context
def recon(self, nmap, tgthost, tgtport, js):
    """
    Runs an nmap scan on target host(s) and target port(s)
    """
    if nmap:
        if js:
            for tgthost in tgthost:
                for tgtport in tgtport:
                    nmapScan(tgthost,tgtport,js)
        if not js:
            for tgthost in tgthost:
                for tgtport in tgtport:
                    nmapScan(tgthost,tgtport,js)


#@main.command()
#@click.option('')
def bf(self):
    """
    Different Bruteforce mechanisms.
    * Dictionary Attack
    """

if __name__ == '__main__':
    main()
