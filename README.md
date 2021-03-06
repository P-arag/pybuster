# PyBuster

## It's gobuster but in python

### Why did I make it??

### Because I **can**

---

![](https://raw.githubusercontent.com/P-arag/pybuster/main/screenshots/pybuster1.jpg)
![](https://raw.githubusercontent.com/P-arag/pybuster/main/screenshots/pybuster2.jpg)

**_PyBuster at work :fire: :fire: :point_up:_**

---

## Installation instructions:

```terminal
git clone https://github.com/P-arag/pybuster
unzip pybuster
cd pybuster
pip install -r requirements.txt
```

---

## Usage Instructions

| Option          | Description                                                                           | Usage                           | Default                             |
| --------------- | ------------------------------------------------------------------------------------- | ------------------------------- | ----------------------------------- |
| --url/-u        | Specifies the url of the site                                                         | -u <.url>                       | None (Necessary)                    |
| --wordslist/-w  | Specifies the wordslist used in brute-forcing                                         | -w <.valid .txt file_path>      | ./wordslists/common.txt (Necessary) |
| -ip or -np      | -ip: Show the ip address of the website -np:Do not Show the ip                        | -ip or -np (no values required) | -np                                 |
| --save/-s       | Specifies the files to which the endpoints will ne appended                           | -s <.valid file_path>           | None                                |
| -f or -nf       | -f : Show the failed requests -nf : Do not show the failed requests                   | -f or -nf (no values required)  | -f                                  |
| -v or -nv       | -v: Show verbose output (Sometimes Kinda annoying tho) -nv: Don't show verbose output | -v or -nv (no values required)  | No values required                  |
| --extensions/-x | Specifies the extension of the particular endpoint                                    | -x ".php, .txt, .etc"           | Empty string ""                     |
| --threads/-t    | Specifies the number of concurrent threads to be run at once                          | -t <.positive integer>          | 30                                  |

## Example
### PS: Plz do not do something illegal with it....., try it on the test website that I have provided
```terminal
python pybuster.py -u http://127.0.0.1 -w ./wordslists/big.txt -ip -s ./endpoints.txt -nf -x ".php,.html, .txt" -t 40
```
