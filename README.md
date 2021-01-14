# moments-app
Django web application for creating and sharing your favorite photos with others

This project relies on the virtual environment and package management library,
[Pipenv](https://pipenv.pypa.io/en/latest/). 

## Setup
### Virtual Environment - Pipenv
    pipenv shell
    pipenv sync --dev

### Database
Create a PostgreSQL database called `moments`

    psql -c "CREATE DATABASE moments"

Run database migrations

    cd moments_app
    python manage.py migrate

## Testing

    python manage.py test
    

## Troubleshooting
### Problem: Can't install `psycopg2` during `pipenv sync` on Mac OS X
1. Make sure XCode is installed
        
        xcode-select --install

2. Make sure openssl is installed (shown below using Homebrew)

        brew install openssl

3. Manually link openssl and pip and re-run

       env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pipenv sync --dev