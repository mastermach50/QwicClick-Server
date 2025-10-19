import server
import database as db
import os

PORT = int(os.getenv("PORT", 3300))
ADDRESS = "0.0.0.0"

def main():
    db.connect()
    # database.initialize()
    print("Connected and initialized db")

    server.serve(PORT, ADDRESS)

if __name__ == "__main__":
    main()
