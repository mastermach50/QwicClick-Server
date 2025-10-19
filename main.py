import server
import database
import os

PORT = int(os.getenv("PORT", 3300))
ADDRESS = "0.0.0.0"

def main():
    database.connect()
    # database.initialize()
    print("Connected and initialized db")

    server.serve(PORT, ADDRESS)

if __name__ == "__main__":
    main()
