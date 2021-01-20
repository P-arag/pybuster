#!/usr/bin/python3

import requests
import threading
from bs4 import BeautifulSoup
from colors import color
import click
import time
import os
import socket
from urllib.parse import urlparse
import pyfiglet

words = []


@click.command()
@click.option('--url', '-u')
@click.option('--wordlist', '-w')
@click.option('-ip/-np', default=False)
@click.option('--save', '-s')
@click.option('-f/--nf', default=True)
@click.option('-v/-nv', default=False)
def main(url, wordlist, ip, save, f, v):
    header = color.GREEN+f'''
########################################################
{pyfiglet.figlet_format("PyBuster", font='slant')}
    '''

    if url[-1] != "/":
        url = url + "/"

    try:
        page = requests.get(url)
        header = header+f"""
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

    header = header + f'''
## Wordslist ## {wordlist}
    '''

    if ip:
        try:
            ipUrl = urlparse(url)
            ip = socket.gethostbyname(ipUrl.netloc)
        except Exception as err:
            ip = err

    header = header + f'''
## IP        ## {ip}   
    '''

    if save is not None and not os.path.exists(save):
        print(color.RED+"Invalid saving location !!")
        exit()

    elif save is not None and os.path.exists(save):
        header = header + f'''
## Save      ## {save}
        '''

    print(header)
    time.sleep(3)
    print(color.BLUE+"PyBuster is starting......")
    time.sleep(2)
    buster(url, wordlist, save, f, verbose=v)


def buster(url, wordslist, save, fails, verbose):
    GOT = 0
    SUS = 0
    FAILED = 0

    with open(wordslist) as f:
        print("Getting wordslist\n#############################################################")
        for line in f.readlines():
            try:
                newPage = requests.get(url+line.strip("\n"))
                if verbose and newPage.status_code == 200:
                    print(color.GREEN+"Got endpoint /"+line.strip("\n") +
                          f" Status code:- {newPage.status_code}", end='  ')
                    print(color.PINK+"BUT it looks like a 404 page tho")
                    SUS += 1
                elif verbose and str(newPage.content).count("404") > 0:
                    print(color.GREEN+"Got endpoint /"+line.strip("\n") +
                          f" Status code:- {newPage.status_code}", end='  ')
                    print(color.PINK+"Looks sus, my not be a proper endpoint")
                    SUS += 1

                else:
                    print(color.GREEN+"Got endpoint /"+line.strip("\n"))
                    GOT += 1
                # print(newPage.content)
                if save is not None:
                    endpointFile = open(save, 'a')
                    endpointFile.write(url+line)
                    endpointFile.close()
                # print(url+line.strip("\n"))
            except KeyboardInterrupt:
                break
            except Exception as e:
                if fails:
                    # print(e)
                    print(color.RED+line.strip("\n") + "  Failed")
                    FAILED += 1
    print(color.BLUE(f"Output: \n Got: {GOT}\n Sus: {SUS}\n Failed: {FAILED}"))     


if __name__ == "__main__":
    main()

# url = input(color.GREEN+"Enter a valid url:- ")
# recursive = True


# #
# #http://13.126.7.62/
