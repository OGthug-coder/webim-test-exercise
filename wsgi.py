from app import app, db

# Запуск приложения
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)