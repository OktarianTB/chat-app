from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Running flask app!")
    app.run()
