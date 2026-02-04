import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

from book_managment.routers import api_key
from module_18.filterong_data import selected_author

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

api_key_input = st.text_input("Enter API Key", type="password")

def validate_key(api_key):
    headers = {"api-key": api_key}
    response = requests.get(f"{BASE_URL}/validate_key", headers=headers)
    return response.status_code == 200

def get_authors():
    response = requests.get(f"{BASE_URL}/authors")
    return response.json() if response.status_code == 200 else None

def add_author(api_key, name):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/authors", json={"name": name}, headers=headers)
    return response.status_code == 200

def update_author(api_key, author_id, name):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/authors/{author_id}", json={"name": name}, headers=headers)
    return response.status_code == 200

def delete_author(api_key, author_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/authors/{author_id}", headers=headers)
    return response.status_code == 200

def get_books():
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch books")
        return []

def add_book(api_key, book_data):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/books", json=book_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Book added '{book_data['title']}' added successfully")
    else:
        st.error(f"Failed to add book: {response.json().get('detail', 'unknown error')}")

def update_book(api_key, book_data, book_id):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=book_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Book '{book_data['title']}' updated successfully")
    else:
        st.error(f"Failed to update book: {response.json().get('detail', 'unknown error')}")

def delete_book(api_key, book_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/books/{book_id}", headers=headers)
    if response.status_code == 200:
        st.success(f"Book '{book_id}' deleted successfully")
    else:
        st.error(f"Failed to delete book: {response.json().get('detail', 'unknown error')}")


def dashboard_authors(api_key):
    st.title("Author Managment Dashboard")
    st.subheader("existing authors")
    authors = get_authors()
    df_authors = pd.DataFrame(authors)
    st.dataframe(df_authors,use_container_width=True)

    st.subheader("add new author")
    new_author_name = st.text_input('Author Name')

    if st.button("Add Author"):
        if new_author_name.strip():
            add_author(api_key, new_author_name)
        else:
            st.error("Author name cannot be empty")

    action = st.radio('Select Action',options=['Update Author','Delete Author'])

    if action == 'Update Author':
        selected_author = st.selectbox('Select Author to update',options=[author['name'] for author in authors])
        new_name = st.text_input('New Author Name', value=selected_author)

        if st.button("Update Author"):
            author_id = next((author['id']for author in authors if author['name'] == selected_author), None)
            update_author(api_key, author_id, new_name)

    elif action == 'Delete Author':
        author_to_delete = st.selectbox('Select Author to Delete',options=[author['name'] for author in authors])
        if st.button("Delete Author"):
            author_id = next((author['id'] for author in authors if author['name'] == author_to_delete), None)
            delete_author(api_key, author_id)


st.subheader("Existing Books")
books = get_books()
author = get_authors()

author_id_to_name = {author['id']: author['name'] for author in author}

for book in books:
    book['author']
    book['author_name'] = author_id_to_name[book['author'], 'Uknown author']
    book['genres'] = ','.join(book['genres'])
    del book['author_id']

df_books = pd.DataFrame(books)
st.dataframe(df_books,use_container_width=True)

st.subheader('Add new Book')
new_book_title = st.text_input('New Book Title')
selected_author = st.selectbox('Select Author',options=[author['name'] for author in author],key="select_author_add")
new_book_average = st.number_input('Average Rating',min_value=0.0, max_value=5.0, step=0.1)
new_book_genres = st.text_input('Genres (comma seperated)')
new_book_year = st.number_input('Publication Year',min_value=1440, max_value=datetime.today().year , step=1)

if st.button("Add Book"):
    if new_book_title.strip() and new_book_title.strip():
        genres_list = [g.strip() for g in new_book_genres.split(',')if g.strip()]
        selected_author_id = next((author['id']for author in author if author['name'] == selected_author), None)

        book_data = {
            'title': new_book_title,
            "author_id": selected_author_id,
            "book_link":"",
            "average_rating": new_book_average,
            "genres": genres_list,
            "publication_year": new_book_year,
        }
        add_book(api_key, book_data)
    else:
        st.error("Book title and genres cannot be empty")

action = st.radio('Select Action',options=['Update Book','Delete Book'],key='book_action')

if action == "Update Book":
    selected_book = st.selectbox('Select Book',options=[book['title'] for book in books],key="select_book_update")

    if selected_book:
        book = next((book for book in books if book['title'] == selected_book), None)
        new_book_title = st.text_input('New Book Title', value=book['title'])
        selected_author_name = st.selectbox('Select Author',options=[author['name'] for author in author],index=[author['name']for author in author if author['name'] == selected_author],key="select_author_add")
        new_book_average_rating = st.number_input('Average Rating',min_value=0.0, max_value=5.0, step=0.1,value=book['average_rating'])
        new_book_genres = st.text_input('Genres (comma seperated)',value=book['genres'])
        new_book_year = st.number_input("Publication Year",min_value=1440, max_value=datetime.today().year , step=1,value=book['publication_year'])
        book_id = book['id']