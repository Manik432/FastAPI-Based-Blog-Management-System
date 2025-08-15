# the config file is for the development environment, in the production it needs to be set on the machine environment.
# the .env file never gets uploaded to github.


from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()