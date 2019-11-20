import requests


def print_book(book):
    print("Book {")
    for key in book.keys():
        attr = str(key)
        val = str(book[key])
        print("\t" + attr + ":" + val)

    print("}")


def get_book(id):
    r = requests.get("http://127.0.0.1:8000/games/" + str(id))
    book = r.json()
    print("Get status Code:" + str(r.status_code))
    if r.ok:
        print_book(book)
        return book
    else:
        print('Error:' + book['message'])


if __name__ == '__main__':

    print("***** Book information before update *****")
    book = get_book(1)

