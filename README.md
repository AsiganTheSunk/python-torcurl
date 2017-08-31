# python-torcurl
[<img src="https://www.python.org/static/opengraph-icon-200x200.png" title="Python.org"
align="right" width="50">](https://www.python.org/)

## Description

python-torcurl it's a library that gives easy access to use **tor** (`SOCKS5 connections`) with curl in a simple way. This library focuses on giving anonymity to your connections throught the internet. It Offers, some degree of control over tor processes using **stem** and over curl configuration parameters using **pycurl**. Likewise to further hide your identity the user agent will be provided by **fakeuseragent** and also use multiple tor instances to alternate the connections beetween them using the ProxyRotator included in this library.

### Features

| SO	| Curl	| Tor	| ProxyChain	| 
|:-------------:|:-------------:|:-----------:|:------------:|
| Linux| x | x | - |
| Windows - | - | - |


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development or testing purposes. 


## Index of Contents

1. [Requirements](#requirements)
   * [Dependencies](#dependencies)
   * [Installation](#installation)
   * [Configuration](#configuration)
2. [Usage](#usage)
3. [License](#license)


## Requirements

The basic requirements for pythong-torcurl are [python 2.7.x][python_download_link]  and [pip installer][pip_installer_link]. Once you already had installed those requirements then next step it's to 
install the depencies. 


### Dependencies

The following list of libraries are needed to make python-torcurl work.

* [beautifulsoap4][beautifulsoap4_link]
* [fakeuseragent][fakeuseragent_link]
* [pycurl][pycurl_link]

### Installation

Go to the main folder of python-torcurl and run setup.py. This will download and install all the dependecies found on the requirements.txt, so the sotfware can function properly.

```
beautifulsoup4==4.5.3
fakeuseragent==
pycurl==

```

### Configuration

#### Tor



### Usage

Once you have sorted out the basic configuration of the tor instance, the only thing you need to worry about now will be the following lines of code to easily use the library.

```python

from TorCurl import ProxyRotator
from TorCurl import TorPyCurl

proxy_rotator = ProxyRotator()
session = TorPyCurl(proxy_rotator)
response = session.get(url='https://www.somewebhere.com')

print response.code
print response.data

```

**[Back to index of contents](#index-of-contents)**


### License

**[Back to index of contents](#index-of-contents)**

[pip_installer_link]: <https://pip.pypa.io/en/stable/installing/>
[python_download_link]: <https://www.python.org/downloads/>

[beautifulsoap4_link]: <https://dummy_link.com>
[pycurl_link]: <https://dummy_link.com>
[fakeuseragent_link]: <https://dummy_link.com>

