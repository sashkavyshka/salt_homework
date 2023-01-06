from src.main import app
import time

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    print("Closing server in 60 seconds")
    time.sleep(60)
    app.stop()