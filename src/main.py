import server
import database as db
import os

PORT = int(os.getenv("PORT", 3300))
ADDRESS = "0.0.0.0"

def main():
    db.initialize()
    db.connect()
    print("Connected and initialized db")

    try:
        server.serve(PORT, ADDRESS)
    except KeyboardInterrupt:
        db.disconnect()
        print("\nDisconnected from db")
        print("Shutting down")

if __name__ == "__main__":
    main()
