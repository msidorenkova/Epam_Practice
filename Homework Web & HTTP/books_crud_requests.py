import requests

# Get information about all books
response = requests.get('http://localhost:5000/api/books/')
print(response.json())

# Get information about one book
response = requests.get('http://localhost:5000/api/books/'+ '2')
print(response.json())

# Add a new book
new_b = {
    'author': "'Franz Kafka'",
    'title': "'The Metamorphosis'"
}

response = requests.post('http://localhost:5000/api/books/', json=new_b)
print(response.reason)
print(response.json())

# Cannot add the same book twice
response = requests.post('http://localhost:5000/api/books/', json=new_b)
print(response.reason)

# Cannot add a book if some fields are not completed
response = requests.post('http://localhost:5000/api/books/', json={'title': 'Inception'})
print(response.reason)

# Update information about a book
upd_book = {
    'author': "'Franz Kafka'",
    'title': "'Die Verwandlung'"
}

response = requests.put('http://localhost:5000/api/books/'+ '5', json=upd_book)
print(response.reason)
print(response.json())

response = requests.get('http://localhost:5000/api/books/')
print(response.json())

#Delete a book
response = requests.delete('http://localhost:5000/api/books/'+'5')
print(response.reason)

response = requests.get('http://localhost:5000/api/books/')
print(response.json())
