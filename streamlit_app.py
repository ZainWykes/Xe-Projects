
import streamlit as st
from storage import LibraryStorage

# Initialize storage
storage = LibraryStorage("./data")

st.set_page_config(page_title="Library Management System", layout="centered")

st.title("📚 Library Management System")

menu = ["View Books", "Add Book", "Borrow Book", "Return Book", "View Members"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "View Books":
    books = storage.get_all_books()
    if books:
        st.subheader("All Books")
        for book in books:
            st.markdown(f"**{book['title']}** by *{book['author']}* (ID: {book['id']})")
    else:
        st.info("No books found.")

elif choice == "Add Book":
    st.subheader("Add New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    if st.button("Add Book"):
        if title and author:
            storage.add_book({"title": title, "author": author})
            st.success("Book added successfully.")
        else:
            st.error("Please provide both title and author.")

elif choice == "Borrow Book":
    st.subheader("Borrow Book")
    member_id = st.text_input("Member ID")
    book_id = st.text_input("Book ID")
    if st.button("Borrow"):
        success = storage.borrow_book(member_id, book_id)
        if success:
            st.success("Book borrowed successfully.")
        else:
            st.error("Failed to borrow book. Check if it's available or already borrowed.")

elif choice == "Return Book":
    st.subheader("Return Book")
    member_id = st.text_input("Member ID")
    book_id = st.text_input("Book ID")
    if st.button("Return"):
        success = storage.return_book(member_id, book_id)
        if success:
            st.success("Book returned successfully.")
        else:
            st.error("Failed to return book. Make sure it was borrowed by this member.")

elif choice == "View Members":
    members = storage.get_all_members()
    if members:
        st.subheader("All Members")
        for member in members:
            st.markdown(f"- **{member['id']}**: {member['name']}")
    else:
        st.info("No members found.")
