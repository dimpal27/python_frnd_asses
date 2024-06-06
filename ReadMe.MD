
This is a Django project that implements a friend request system. Users can send, accept, reject friend requests, search for users, and list friends.

## Features

- User Signup
- User Login
- Search Users
- Send Friend Request
- Accept Friend Request
- Reject Friend Request
- List Friends
- List Pending Friend Requests

Steps to Run the Project:
1. Clone the repository:
    git clone https://github.com/yourusername/your-repo-name.git
2. Create and activate a virtual environment:
   cd your-repo-name
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
3. Install dependencies:
   pip install -r requirements.txt
4. Run database migrations:
      python manage.py makemigrations
      python manage.py migrate
5. Run the development server:
 python manage.py runserver