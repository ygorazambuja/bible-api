# Bible API

A comprehensive RESTful API for accessing multiple Bible translations in Portuguese, built with FastAPI.

## Features

- Multiple Bible translations available (NAA, NTLH, ACF, ARA, AS21, JFAA, KJA, KJF, NBV, NVI, NVT, TB)
- Query by book, chapter, and verse
- Flexible verse range selection
- AI-powered Bible search and interpretation

## Prerequisites

- Python 3.12+
- PostgreSQL (or SQLite as fallback)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bible-api.git
   cd bible-api
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Database setup:
   - Option 1: Use PostgreSQL (recommended)
     ```bash
     # Set your database URL environment variable
     export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bibledb
     # Create the database in PostgreSQL
     createdb bibledb
     ```
   - Option 2: Use SQLite (fallback)
     ```bash
     # Set your database URL to use SQLite
     export DATABASE_URL=sqlite:///bible.db
     ```

5. Run the database setup script:
   ```bash
   python populate_db.py
   ```

## Usage

### Running the API Locally

```bash
fastapi run main.py
```

The API will be available at http://localhost:8000

### Using Docker Compose (Recommended)

```bash
# Start the API and PostgreSQL database
docker-compose up -d

# To populate the database (first time only)
docker-compose exec api python populate_db.py
```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc
- Scalar API reference: http://localhost:8000/scalar

## API Endpoints

### Bibles

- `GET /bibles` - Get all available Bible translations
- `GET /bibles/{bible_abbrev}` - Get a specific Bible translation by abbreviation

### Books

- `GET /bibles/{bible_abbrev}/books` - Get all books for a specific Bible translation
- `GET /bibles/{bible_abbrev}/books/{book_abbrev}` - Get a specific book by abbreviation

### Verses

- `GET /bibles/{bible_abbrev}/books/{book_abbrev}/verses` - Get all verses from a book
  - Query parameters: `chapter`, `verse`
- `GET /bibles/{bible_abbrev}/books/{book_abbrev}/chapters/{chapter}` - Get all verses from a chapter
  - Query parameters: `from_verse`, `to_verse`

### AI Features

- `GET /ai/...` - AI-powered Bible search and interpretation features

## Docker Support

### Using Docker Compose (Recommended)

Build and run the API with PostgreSQL in Docker containers:

```bash
docker-compose up -d
```

### Using Docker Only

Build and run the API in a Docker container:

```bash
docker build -t bible-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/bibledb bible-api
```

## Project Structure

- `main.py` - FastAPI application entry point
- `domain/` - Database models and schemas
- `database/` - Database configuration
- `routers/` - API routes and endpoints
- `services/` - Business logic
- `raw_data/` - Source data for Bible translations
- `docker-compose.yml` - Docker Compose configuration for the API and PostgreSQL

## License

MIT

## Contributors

Ygor Azambuja
