#!/usr/bin/python3

import requests
from colors import color
import click
import time
import os
import socket
from urllib.parse import urlparse
import pyfiglet


@click.command()
@click.option('--url', '-u')
@click.option('--wordlist', '-w')
@click.option('-ip/-np', default=False)
@click.option('--save', '-s')
@click.option('-f/-nf', default=True)
@click.option('-v/-nv', default=False)
@click.option("--extensions", '-x')
def main(url, wordlist, ip, save, f, v, extensions):
    header = color.GREEN+f'''
########################################################
{pyfiglet.figlet_format("PyBuster", font='slant')}
    '''

    if url[-1] != "/":
        url = url + "/"

    try:
        page = requests.get(url)
        header += f"""
########################################################
## Url       ## {url}
        """
    except:
        print(color.RED+"Invalid Url !!")
        exit()

    if wordlist is None:
        try:
            print(
                color.BLUE+"No wordlist Specified !!, going with default, for custom, try -w <file path>")
            wordlist = "./wordlists/big.txt"

        except Exception as e:
            print(color.RED+e)

    if not wordlist.endswith('.txt'):
        print(color.RED+"A words list must have .txt extension")
        exit()

    if not os.path.exists(wordlist):
        print(color.RED+"Invalid wordlist location")
        exit()

    header += f'''
## Wordslist ## {wordlist}
    '''

    if ip:
        try:
            ipUrl = urlparse(url)
            ip = socket.gethostbyname(ipUrl.netloc)
        except Exception as err:
            ip = err

    header += f'''
## IP        ## {ip}   
    '''

    if save is not None and not os.path.exists(save):
        print(color.RED+"Invalid saving location !!")
        exit()

    elif save is not None and os.path.exists(save):
        header += f'''
## Save      ## {save}
        '''

    if extensions is not None:
        if extensions.count(",") > 0:
            extensionsArr = extensions.split(",")
            extensionsArr.append("")
    else:
        extensionsArr = [""]

    header += f"""
## Xtensions ## {extensionsArr}    
    """

    if v:
        header += f'''
## Verbose   ## {v}    
        '''

    if f:
        header += f'''
## Fails     ## {f}        
        '''

    print(header)
    time.sleep(3)
    print(color.BLUE+"PyBuster is starting......")
    time.sleep(2)
    buster(url, wordlist, save, f, v, xtensions=extensionsArr)


def buster(url, wordslist, save, fails, verbose, xtensions):
    GOT = 0
    SUS = 0
    FAILED = 0
    setBreak= False
    with open(wordslist) as f:
        print("Getting wordslist\n#############################################################")

        for line in f.readlines():
            for xtension in xtensions:
                xtension = xtension.strip()
                try:
                    URL = url + line.strip("\n")
                    newPage = requests.get(URL+xtension)
                    if verbose and str(newPage.content).count("404") > 0:
                        print(color.GREEN+"Got endpoint /"+line.strip("\n")+xtension +
                              f" Status code:- {newPage.status_code}", end='  ')
                        print(color.PINK+"Looks sus, might not be a proper endpoint (404)")
                        SUS += 1

                    else:
                        print(color.GREEN+"Got endpoint /" +
                              line.strip("\n")+xtension)
                        GOT += 1
                    # print(newPage.content)
                    if save is not None:
                        endpointFile = open(save, 'a')
                        endpointFile.write(URL+xtension+"\n")
                        endpointFile.close()
                    # print(url+line.strip("\n"))
                except KeyboardInterrupt:
                    setBreak = True
                    break
                except Exception as e:
                    if fails:
                        # print(e)
                        print(color.RED+line.strip("\n")+xtension + " Failed")
                        FAILED += 1
            if setBreak:
                break            

    print(color.BLUE+f"Output: \n Got: {GOT}\n Sus: {SUS}\n Failed: {FAILED}")


if __name__ == "__main__":
    main()
