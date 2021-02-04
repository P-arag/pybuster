#!/usr/bin/python3

import requests
from colors import color
import click
import time
import os
import socket
from urllib.parse import urlparse
import pyfiglet
import threading
from tqdm import tqdm


@click.command()
@click.option('--url', '-u', help="For help visit https://github.com/P-arag/pybuster")
@click.option('--wordlist', '-w')
@click.option('-ip/-np', default=False)
@click.option('--save', '-s')
@click.option('-f/-nf', default=True)
@click.option('-v/-nv', default=False)
@click.option("--extensions", '-x')
@click.option("--threads", "-t", default=30)
def main(url, wordlist, ip, save, f, v, extensions, threads):
    header = color.GREEN+'''
########################################################
{}
    '''.format(pyfiglet.figlet_format("PyBuster", font='slant').strip("\n") + " By: P-arag@github.com")

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

    if threads > 100:
        print(color.BLUE + "WARNING!!!!!! You have selected the nuber of threads to be greater than 100, it might DOS (Denial of Service) the server you are brute-forcing, do it at your own risk")

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

    try:
        threads = int(threads)
    except Exception as threadIntException:
        print(color.RED + "--threads must have an int value !!")
        exit()

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

    header += f'''
## Threads   ## {threads}    
    '''

    print(header)
    time.sleep(3)
    print(color.BLUE+"PyBuster is starting......")
    time.sleep(2)

    print("Getting wordslist...")
    wordsArr = []
    with open(wordlist, "r") as wordsFile:
        temp = []
        for line in wordsFile.readlines():
            temp.append(line.strip("\n"))
            if len(temp) % threads == 0:
                wordsArr.append(temp)
                temp = []

        for words in tqdm(wordsArr):
            all_threads = []
            for word in words:
                wordThread = threading.Thread(
                    target=buster, args=[url, word, save, f, v, extensionsArr])
                wordThread.start()
                all_threads.append(wordThread)

            for each_thread in all_threads:
                each_thread.join()


def buster(url, word, save, fails, verbose, xtensions):
    for xtension in xtensions:
        xtension = xtension.strip()
        try:
            URL = url + word
            newPage = requests.get(URL+xtension)
            setSave = False
            if verbose and newPage.status_code == 404:
                print(color.GREEN+"Got endpoint /"+word+xtension +
                      f" Status code:- {newPage.status_code}", end='  ')
                print(color.PINK+"Looks sus, might not be a proper endpoint (404)")
                setSave = True

            elif newPage.status_code != 404:
                print(color.GREEN+"Got endpoint /" +
                      word+xtension +
                      f" Status code:- {newPage.status_code}")
                setSave = True

            # print(newPage.content)
            if save is not None and setSave:
                endpointFile = open(save, 'a')
                endpointFile.write(URL+xtension+"\n")
                endpointFile.close()
            # print(url+line.strip("\n"))
        except KeyboardInterrupt:
            break
        except Exception as e:
            if fails:
                print(color.RED+"/"+word+xtension + " Failed")


if __name__ == "__main__":
    main()
