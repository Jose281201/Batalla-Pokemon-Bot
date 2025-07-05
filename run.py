from app import main
from app.applog import LoggerConfig

LoggerConfig().setup_logging()


if __name__ == "__main__":
    main()
    