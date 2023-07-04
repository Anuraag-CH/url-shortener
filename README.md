# URL Shortening Service

A simple URL shortening service built with Python,FastAPI and Mongodb

# Installation

1. Clone the repository: git clone https://github.com/Anuraag-CH/url_shortener
2. Navigate to the project directory: cd url_shortener  
3. Install the dependencies: pip install -r requirements.txt
4. Default Mongodb connection is  `mongodb://localhost:27017/Url`.
5. Run the application using the following command.Use another port if necessary.
   uvicorn main:app --reload --port 8000
6. Access the endpoints using localhost:8000/docs or use other port used in the above command if necessary.
7. Generate the short_url locally by passing an url as POST request as mentioned in the documentation above.
8. You can access the short url locally through localhost:8000/{short_url}.Please give your short url instead of short_url

# Deployment 
The service is deployed at https://shortyurl.up.railway.app/
