# Bahea Calendar 🇺🇸

Bahea Calendar is a project that adds the standings of your favorite soccer team games to your google calendar!

## How to run

To run the Bahea Calendar, follow these steps:

**1. Make sure you have Python3 and pip installed on your machine.**

**2. Clone this repository to your local environment.**

```
git clone https://github.com/gogixweb/bahea-cal.git
```

**3. Install `virtualenv` if you haven't already installed it:**

```
pip install virtualenv
```

**4. Create a virtual environment in the project folder:**

```
virtualenv env
```

**5. Activate the virtual environment:**

- On Windows:

```
env\Scripts\activate
```

- Ond macOS and Linux:

```
source env/bin/activate
```

**6. Install the project dependencies from the file `requirements-dev.txt`:**

```
pip install -r requirements-dev.txt`
```

**7. Create a .env file in the project root**

**8. Insert the environment variables into the .env file and edit them according to your needs:**

```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY="qualquerstring"
DJANGO_ALLOWED_HOSTS="*"
DJANGO_BASE_URL="http://localhost:8889"
DJANGO_DATABASES__default__ENGINE="django.db.backends.sqlite3"
DJANGO_DATABASES__default__NAME="/caminho/para/o/projeto/bahea-cal/db.sqlite3"
DJANGO_ENVIRONMENT="dev"
DJANGO_CALENDAR_NAME_PREFIX="(dev) "
```

**9. Execute the project:**

```
python manage.py runserver
```

# Bahea Calendar 🇧🇷

O Bahea Calendar é um projeto que permite adicionar a agenda de jogos do seu time do coração ao seu calendário do Google!

## Como rodar o projeto

Para executar o Bahea Calendar, siga estas etapas:

**1. Certifique-se de ter o Python3 e o pip instalados na sua máquina.**

**2. Clone este repositório para o seu ambiente local.**

```
git clone https://github.com/gogixweb/bahea-cal.git
```

**3. Instale o `virtualenv` se ainda não o tiver instalado:**

```
pip install virtualenv
```

**4. Crie um ambiente virtual na pasta do projeto:**

```
virtualenv env
```

**5. Ative o ambiente virtual:**

- No Windows:

```
env\Scripts\activate
```

- No macOS e Linux:

```
source env/bin/activate
```

**6. Instale as dependências do projeto do arquivo `requirements-dev.txt`:**

```
pip install -r requirements-dev.txt`
```

**7. Crie um arquivo `.env` na pasta raiz do projeto.**

**8. Insira as variáveis de ambiente no arquivo `.env` e personalize conforme sua necessidade:**

```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY="qualquerstring"
DJANGO_ALLOWED_HOSTS="*"
DJANGO_BASE_URL="http://localhost:8889"
DJANGO_DATABASES__default__ENGINE="django.db.backends.sqlite3"
DJANGO_DATABASES__default__NAME="/caminho/para/o/projeto/bahea-cal/db.sqlite3"
DJANGO_ENVIRONMENT="dev"
DJANGO_CALENDAR_NAME_PREFIX="(dev) "
```

**9. Execute o projeto:**

```
python manage.py runserver
```
