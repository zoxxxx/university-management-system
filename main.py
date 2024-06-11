import frontend
import database
import frontend.home
def main() -> None:
    frontend.home.show()
    database.connect()

if __name__ == "__main__":
    main()