from utils.serialization import load_config
from website.zlibrary import ZLibrary

if __name__ == "__main__":
    theme = "红岩"
    file_type = "pdf"
    search_type = "book"
    config = load_config()
    zlib = ZLibrary(config)
    zlib.open_page()
    zlib.login()
    zlib.search(theme, search_type)
    zlib.find_book(theme, file_type)
    zlib.download(theme, file_type)
    zlib.close_page()
