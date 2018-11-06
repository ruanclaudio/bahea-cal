# Bahea Calendar :us:

Bahea Calendar is a project that will add to your google calendar the schedule of your favorite soccer team games!

## How to run

You must have Python3 and pip installed on your computer.

Also, you need to create a project to access the google calendar API. You can do it accessing the google's [developers console](https://console.developers.google.com/). When it's done, download the JSON file with your credentials and rename it with `credentials.json`

After that, clone this repository and follow these steps:

- `pip install virtualenv`
- `virtualenv env`
- `source env/bin/activate`
- `pip install -r requirements-dev.txt`
- ```TOKEN_NAME="token.json" CREDENTIALS_JSON="credentials.json" TOKEN_JSON=`cat token.json` python fetch.py```



# Bahea Calendar 🇧🇷

O Bahea Calendar é um projeto que adicionará ao seu calendário google a agenda de jogos do seu time do coração!

## Como rodar o projeto

É necessário ter Python3 e o pip instalados na sua máquina. 

Além disso, é preciso criar um projeto para acessar a API do google calendar. Você pode criar acessando o [console de desenvolvedores](https://console.developers.google.com/) do google. Depois de criado, baixe o arquivo JSON das suas credenciais e salve no mesmo diretório do projeto com o nome `credentials.json`

A partir disso, clone este repositório e siga os passos seguintes:

- `pip install virtualenv`
- `virtualenv env`
- `source env/bin/activate`
- `pip install -r requirements-dev.txt`
- ```TOKEN_NAME="token.json" CREDENTIALS_JSON="credentials.json" TOKEN_JSON=`cat token.json` python fetch.py```

