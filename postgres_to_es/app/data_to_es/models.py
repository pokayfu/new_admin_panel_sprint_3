from pydantic import BaseModel


class Movie(BaseModel):
    id: str
    imdb_rating: float | None
    title: str
    description: str | None
    genres: list[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    class PersonEntity(BaseModel):
        id: str
        name: str
    directors: list[PersonEntity]
    actors: list[PersonEntity]
    writers: list[PersonEntity]


class Settings(BaseModel):
    storage_file_path: str
    elastic_host: str 
    elastic_port: str
    elastic_index: str 
    etl_start_time: str 
    etl_extract_size: int 
    etl_nap_time: float 
    etl_sleep_time: float

class PostgresSettings(BaseModel):
    host: str 
    port: str 
    user: str 
    password: str
    dbname: str 