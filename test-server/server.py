from src.main import app
import time

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    print("Stopping, stopping, really stopping")
    app.stop()