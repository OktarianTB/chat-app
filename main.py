from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# docker build -t flask-test .
# docker run -p 56733:80 flask-test
