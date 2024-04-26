# Bahea Calendar 🇺🇸

Bahea Calendar is a project that adds the standings of your favorite soccer team games to your google calendar!

## How to run

To run the Bahea Calendar, follow these steps:

**1. Make sure you have Python3 and pip installed on your machine.**

**2. Acess the Google Calendar API.**

To acess the Google Calendar API, you must create a project. You can create a project by going to the [Developer Console](https://console.developers.google.com/)

- Enable the Google Calendar API;

- Create a client ID;

- Under _Authorized JavaScript origins_ configure this URI:

```
http://localhost:800
```

- Under _Authorized redirect URIs_ configure this URI:

```
http://localhost:8000/calendar/redirect
```

- Create a _secret.json_ file in the _webapp_ folder and insert the credentials you downloaded previously, as show in the following example:

```
{
    "dev/google/calendar": {YOUR GOOGLE CREDENTIALS}
}
```

**3. Clone this repository to your local environment.**

```
git clone https://github.com/gogixweb/bahea-cal.git
```

**4. Install `virtualenv` if you haven't already installed it:**

```
pip install virtualenv
```

**5. Create a virtual environment in the project folder:**

```
virtualenv env
```

**6. Activate the virtual environment:**

- On Windows:

```
env\Scripts\activate
```

- Ond macOS and Linux:

```
source env/bin/activate
```

**7. Install the project dependencies from the file `requirements-dev.txt`:**

```
pip install -r requirements-dev.txt
```

**8. Create a .env file in the project root**

**9. Insert the environment variables into the .env file and edit them according to your needs:**

```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY="anyonestring"
DJANGO_ALLOWED_HOSTS="*"
DJANGO_BASE_URL="http://localhost:8000"
DJANGO_DATABASES__default__ENGINE="django.db.backends.sqlite3"
DJANGO_DATABASES__default__NAME="/path/to/your/project/bahea-cal/db.sqlite3"
DJANGO_ENVIRONMENT="dev"
DJANGO_CALENDAR_NAME_PREFIX="(dev) "
```

**10. Apply database migrations:**

```
python manage.py migrate
```

**11. Collect static files:**

```
python manage.py collectstatic
```

**12. Execute the project:**

```
python manage.py runserver
```

# Bahea Calendar 🇧🇷

O Bahea Calendar é um projeto que permite adicionar a agenda de jogos do seu time do coração ao seu calendário do Google!

## Como rodar o projeto

Para executar o Bahea Calendar, siga estas etapas:

**1. Certifique-se de ter o Python3 e o pip instalados na sua máquina.**

**2. Acesse a API do Google Calendar.**

É preciso criar um projeto para acessar a API do google calendar. Você pode criar acessando o [Console de Desenvolvedores](https://console.developers.google.com/)

- Ative a API do Google Calendar

- Crie uma client ID

- Em _Origens JavaScript autorizada_ configure a seguinte URI:

  ```
  http://localhost:8000
  ```

- Em _URIs de redirecionamento autorizados_ configure a seguinte URI:

  ```
  http://localhost:8000/calendar/redirect
  ```

- Navegue até a Tela de permissão OAuth e adicione um usuário de teste.

- Faça o download do arquivo JSON das suas credenciais

- Crie um arquivo _secrets.json_ na pasta _webapp_ e insira as credenciais que você baixou anteriormente, conforme o exemplo a seguir:

  ```
  {
  "dev/google/calendar": {SUAS CREDENCIAIS GOOGLE}
  }
  ```

**3. Clone este repositório para o seu ambiente local.**

```
git clone https://github.com/gogixweb/bahea-cal.git
```

**4. Instale o `virtualenv` se ainda não o tiver instalado:**

```
pip install virtualenv
```

**5. Crie um ambiente virtual na pasta do projeto:**

```
virtualenv env
```

**6. Ative o ambiente virtual:**

- No Windows:

```
env\Scripts\activate
```

- No macOS e Linux:

```
source env/bin/activate
```

**7. Instale as dependências do projeto do arquivo `requirements-dev.txt`:**

```
pip install -r requirements-dev.txt
```

**8. Crie um arquivo `.env` na pasta raiz do projeto.**

**9. Insira as variáveis de ambiente no arquivo `.env` e personalize conforme sua necessidade:**

```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY="qualquerstring"
DJANGO_ALLOWED_HOSTS="*"
DJANGO_BASE_URL="http://localhost:8000"
DJANGO_DATABASES__default__ENGINE="django.db.backends.sqlite3"
DJANGO_DATABASES__default__NAME="/caminho/para/o/projeto/bahea-cal/db.sqlite3"
DJANGO_ENVIRONMENT="dev"
DJANGO_CALENDAR_NAME_PREFIX="(dev) "
```

**10. Aplique as migrações do banco de dados:**

```
python manage.py migrate
```

**11. Colete os arquivos estáticos:**

```
python manage.py collectstatic
```

**12. Execute o projeto:**

```
python manage.py runserver
```
