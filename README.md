# deluge-tdameritrade
TD Ameritrade tools


# interesting projects

https://github.com/timkpaine/tdameritrade  (452 stars)

pandas built in, several contributors, python notebook


https://github.com/alexgolec/tda-api (202 stars)

https://github.com/areed1192/python-trading-robot  (298 stars)


# TD Ameritrade docs

[Docs](https://developer.tdameritrade.com/account-access/apis)

[Terms and conditions](https://developer.tdameritrade.com/legal)

[Authentication](https://developer.tdameritrade.com/content/authentication-faq)


# Setup

`conda create --name deluge`

`conda activate deluge`


# Authentication

[Via tdameritrade python package](https://tdameritrade.readthedocs.io/en/latest/index.html#authentication)

via python3 prompt

`import tdameritrade`

`tdameritrade.auth.authentication(client_id='AFRODITXXXXXXXXXXXXXXXXXXXXXXXX', redirect_uri='https://localhost')`


Or Load this in a browser to prompt to user & pass and get code back 

`https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=https%3A%2F%2Flocalhost&client_id=AFRODITXXXXXXXXXXXXXXXXXXXXXXXX%40AMER.OAUTHAP`

