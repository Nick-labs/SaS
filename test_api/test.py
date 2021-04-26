from requests import get, post, delete

print(str(get('http://localhost:5000/api/jobs').json()).replace("'", '"'))

print(post('http://localhost:5000/api/jobs').json())

print(post('http://localhost:5000/api/jobs',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:5000/api/jobs',
           json={'title': 'Название',
                 'salary': 100000,
                 'content': 'Описание работы',
                 'contacts': '+71231231231',
                 'user_id': 1}).json())

print(delete('http://localhost:5000/api/jobs/999').json())

print(delete('http://localhost:5000/api/jobs/48').json())
