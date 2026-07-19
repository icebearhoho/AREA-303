import requests
import json

r = requests.get(
    'http://localhost:8000/api/v1/personal-shopper/products',
    params={'query': 'Son môi tự nhiên cho da ngăm', 'top_k': 4}
)
with open('test_result.json', 'w', encoding='utf-8') as f:
    json.dump(r.json(), f, indent=2, ensure_ascii=False)
print("Done")
