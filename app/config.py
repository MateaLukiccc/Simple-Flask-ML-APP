from pydantic import BaseSettings

class Settings(BaseSettings):
    config_path: str   
    weights_path: str     
    to_open_classes_path: str
    upload_folder: str
    secret_key: str
    
    class Config:
        env_file = "../.env"
        
settings = Settings()