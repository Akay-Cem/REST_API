from app import create_app  # Import after initializing database
from app.db import initialize_database

if __name__ == '__main__':
    app = create_app()
    initialize_database()  # Run the database initialization
    app.run(host="0.0.0.0", port=5000, debug=True)
