from app.indexer import build_all

if __name__ == "__main__":
    with open("data/url_list.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    print("URLs fundet:", urls)

    build_all()