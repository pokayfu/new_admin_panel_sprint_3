from backoff import backoff
from elasticsearch import Elasticsearch
import json
from es_index import movie_index_conf


class ElasticLoader:
    def __init__(self, service_host: str, service_port: str, index: str) -> None:
        self.client = Elasticsearch(f'{service_host}:{service_port}')
        self.index_name = index
        
    @backoff()
    def upload(self, movies: list):
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name, body=movie_index_conf)
        content = []
        for movie in movies:
            content.append(json.dumps({
                'index': {
                    '_index': self.index_name,
                    '_id': movie.id
                }
            }))
            content.append(movie.model_dump_json())
        content = '\n'.join(content) + '\n'
        self.client.bulk(body=content, index=self.index_name)
