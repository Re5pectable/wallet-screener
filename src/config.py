import os

class AppSettings:
    DEBUG: bool = bool(int(os.getenv("DEBUG", "1")))

class DbSettings:
    HOST: str = os.getenv('DB_HOST')
    DATABASE: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USERNAME')
    PASSWORD: str = os.getenv('DB_PASSWORD')
    
    def __init__(self) -> None:
        if not all([
            self.HOST,
            self.DATABASE,
            self.USER,
            self.PASSWORD,
        ]):
            raise ValueError('Invalid settings')

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DATABASE}"
    
app_settings = AppSettings()
db_settings = DbSettings()