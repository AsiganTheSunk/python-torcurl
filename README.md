# python-torcurl
[<img src="https://www.python.org/static/opengraph-icon-200x200.png" title="Python.org"
align="right" width="50">](https://www.python.org/)

## Description

python-torcurl it's a library that gives easy access to use **tor** (`SOCKS5 connections`) with curl in a simple way. This library focuses on giving anonymity to your connections throught the internet. It Offers, some degree of control over tor processes using **stem** and over curl configuration parameters using **pycurl** . Likewise to further hide your identity the user agent will be provided by **fake-useragent**.

Also it offers the chance to use multiple tor instances to alternate the connections beetween, in sequential or random style using the **ProxyRotator** functionalities.

### Features

| SO	| Curl	| Tor	| ProxyChain	| 
|:-------------:|:-------------:|:-----------:|:------------:|
| Linux	| x | x | - |
| Windows	| - | - | - |

### Future

The big TODO's are finishing and polishing the actual code, but in the near future include threading to the module and have a reliable way to test dns leaks in the tor circuits.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development or testing purposes. Hope you enjoy it.


## Index of Contents

1. [Requirements](#requirements)
      * [Dependencies](#dependencies)
   	* [Installation](#installation)
         + [pip](#pip)
         + [source](#source)
   	* [Configuration](#configuration)
         + [tor](#tor)
         + [tor_instance](#tor_instance)
         + [stem](#stem)
2. [Usage](#usage)
      * [Basic](#basic)
         + [setup](#setup)
         + [request](#request)
         + [parameters](#basic_parameters)
         + [tor](basic_tor)
      * [Advanced](#advanced)
         + [proxy_rotator](#proxy_rotator)
         + [tor](#multi_tor)

3. [License](#license)


## Requirements

The basic requirements for pythong-torcurl are [python 2.7.x][python_link]  and [pip-installer][pip-installer_link]. Once you already had installed those requirements then next step it's to 
install the depencies. 


### Dependencies

The following list of libraries are needed to make python-torcurl work.

* [beautifulsoap4][beautifulsoap4_link]
* [fake-useragent][fake-useragent_link]
* [pycurl][pycurl_link]
* [stem][stem_link]

### Installation

#### pip (`soon!`)

```bash

pip install python-torcurl

```

#### source
First clone the repository from git.

```bash

git clone https://github.com/AsiganTheSunk/python-torcurl

```

Once you have cloned the repository, go to the main folder of python-torcurl follow the instructions below. This will download and install all the dependecies found on the requirements.txt, so the sotfware can function properly.

(`soon!`)

```bash
> cd python-torcurl

# Install python dependencies.
# Depending on your setup, one or both of these may require sudo.
 
> pip install -r requirements.txt
> python setup.py install

```

**[Back to index of contents](#index-of-contents)**

### Configuration

#### Tor
To install tor in linux enviroment such as Ubuntu/Debian.

```bash

> apt-get install tor

```

##### Tor_instance
To use multiple tor instances in the ProxyRotator, you need to create a new torrc.n. With 
the following lines you can achive this.

```bash

> tourch /etc/tor/torrc.1

```
Edit the new created file with, in this case socks_port will be 9060 and cntrl_port 9061.

```
SocksPort 9060
ControlPort 9061
DataDirectory /var/lib/tor1
HashedControlPassword 'yourhashedpassword'

```
Finally run force a new instance of tor to run using your configuration file.

```bash

> tor -f /etc/tor/torrc.1

```

##### Stem
In order to make stem work with the library you need to configure the torrc in the (`/etc/tor/torrc`) to use cntrl_port 9051
and socks_port 9050. Furthermore you need to use the following commands to create the hash to be able to authenticate yourself
in the service.

```bash

> tor --hash-password dummypass

```

**[Back to index of contents](#index-of-contents)**

### Usage

Once you have sorted out the basic configuration of the tor instance, the only thing you 
need to worry about now will be the following lines of code to easily use the library.

#### Basic

##### setup

```python

from torcurl.ProxyRotator import ProxyRotator
from torcurl.TorPyCurl import TorPyCurl

# By default the ProxyRotator class will initialize a tor instances with the 
# parameters given by the config.cfg
proxy_rotator = ProxyRotator()
session = TorPyCurl(proxy_rotator)

```

##### request

```python

from torcurl.ProxyRotator import ProxyRotator
from torcurl.TorPyCurl import TorPyCurl

proxy_rotator = ProxyRotator()
session = TorPyCurl(proxy_rotator)
session.get(url='https://www.somewebhere.com')

```

##### response

```python

from torcurl.ProxyRotator import ProxyRotator
from torcurl.TorPyCurl import TorPyCurl

proxy_rotator = ProxyRotator()
session = TorPyCurl(proxy_rotator)
response = session.get(url='https://www.somewebhere.com')
                           
print response.code

print response.data

```

##### basic_parameters

```python

from torcurl.ProxyRotator import ProxyRotator
from torcurl.TorPyCurl import TorPyCurl

proxy_rotator = ProxyRotator()
session = TorPyCurl(proxy_rotator)

# By default you can set headers, attrs in the request plus 
# enable ssl encryption as well as setting a time out
response = session.get(url='https://www.somewebhere.com', headers={}, attrs={}, 
                       ssl=True, timeout=15)
                           
print response.code

print response.data

```

##### basic_tor


```python

soon!

```

#### Advanced

##### proxy_rotator

showing off modes and a little bit of explanation

```python

from torcurl.ProxyRotator import ProxyRotator
from torcurl.TorPyCurl import TorPyCurl

# By default the mode it's set to random
proxy_rotator = ProxyRotator(mode='sequential')

```

##### multi_tor
Using session.validate() will allow you to easy test if your tor connection it's up and running, testing ip leak
and for this example will help you see how the library manages the swap beetween instances.

```python

from torcurl.ProxyRotator import ProxyRotator
from torcurl.TorPyCurl import TorPyCurl

proxy_rotator.add_tor_instance(None, 9060, 9061, None, None)
proxy_rotator.add_tor_instance(None, 9070, 9071, None, None)
session = TorPyCurl(proxy_rotator)

print('SEQUENTIAL TEST')
for i in range(0,4):
   session.validate()
   
```
The output for the *session.validate()* should be something like this.

```bash
> SEQUENTIAL TEST
> TorPyCurl Connection address: 51.15.34.210
> TorPyCurl Status: Connection PASS
> TorPyCurl Connection address: 91.219.237.229
> TorPyCurl Status: Connection PASS
> TorPyCurl Connection address: 51.15.34.210
> TorPyCurl Status: Connection PASS
> TorPyCurl Connection address: 91.219.237.229
> TorPyCurl Status: Connection PASS
> TorPyCurl Connection address: 51.15.34.210
> TorPyCurl Status: Connection PASS
```

**[Back to index of contents](#index-of-contents)**


### License

Copyright 2017 asiganthesunk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

**[Back to index of contents](#index-of-contents)**

[pip-installer_link]: <https://pip.pypa.io/en/stable/installing/>
[python_link]: <https://www.python.org/downloads/>
[tor_link]: <https://www.torproject.org/download/download>

[beautifulsoap4_link]: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
[pycurl_link]: <http://pycurl.io/>
[fake-useragent_link]: <https://pypi.python.org/pypi/fake-useragent>
[stem_link]: <https://stem.torproject.org/>

