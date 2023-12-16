# Tyres Shop

A simple e-commerce application in ___Django Web Framework___.  
The following technologies are used in the project:
- Django
- Redis
- Docker
- Nginx

The application has an integrated payment system [___Stripe___](https://stripe.com/).  

## Quickstart

Preparation steps:
1. Install [__Git__](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on your system.
2. Also install [__Docker__](https://docs.docker.com/engine/install/).

Clone the repository:
```
git clone https://github.com/DBU-coder/tyres_shop.git
```
Create `.env` file with your settings using `.env.example`. Add your domain or ip to ALLOWED_HOSTS in `.env`

Now we need to change permissions on file `entrypoint.sh`

```
chmod +x ./entrypoint.sh
```

In project root folder, start the application with following command:
```
docker compose up
```
Use `-d` flag to start the application in detached mode.
Wait for the docker containers to start...

Enter http://your-domain:8000/shop into your browser.

### Production mode

You can also launch the application using [__Nginx__](https://nginx.org/en/docs/) server.
To do this, create a file `.env.prod` with your production settings.
Change permissions on file `ep.prod.sh`.
```
chmod +x ./ep.prod.sh
```
In project root folder, start the application with following command:
```
docker compose -f docker-compose.prod.yml up
```
Now the app using Nginx server on :80 port. 