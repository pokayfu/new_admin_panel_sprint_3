from models import Movie


class Transformer:
    def __init__(self) -> None:
        self.model = Movie

    def transform(self, data: list[dict]):
        result = []
        for part in data:
            trans_data = self.transorm_persons(part['persons'])
            data = self.model(
                id=part['id'],
                imdb_rating=part['rating'],
                title=part['title'],
                description=part['description'],
                genres=part['genres'],
                directors_names=trans_data['directors_names'],
                actors_names=trans_data['actors_names'],
                writers_names=trans_data['writers_names'],
                actors=trans_data['actors'],
                directors=trans_data['directors'],
                writers=trans_data['writers']
            )
            result.append(data)
        return result
    
    def transorm_persons(self, persons: list[dict]):
        persons_ids = []
        result = {
            'directors_names': [],
            'actors_names': [],
            'writers_names': [],
            'directors': [],
            'actors': [],
            'writers': []
        }
        for person in persons:
            if person['person_id'] not in persons_ids:
                if person['person_role'] == 'actor':
                    result['actors'].append({
                        'id': person['person_id'],
                        'name': person['person_full_name']
                    })
                    result['actors_names'].append(person['person_full_name'])
                if person['person_role'] == 'director':
                    result['directors'].append({
                        'id': person['person_id'],
                        'name': person['person_full_name']
                    })
                    result['directors_names'].append(person['person_full_name'])
                if person['person_role'] == 'writer':
                    result['writers'].append({
                        'id': person['person_id'],
                        'name': person['person_full_name']
                    })
                    result['writers_names'].append(person['person_full_name'])
                persons_ids.append(person['person_id'])
        return result
