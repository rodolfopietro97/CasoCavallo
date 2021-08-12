from Sources.Internal.DevUrandomRandomSource import DevUrandomRandomSource

if __name__ == '__main__':
    randomSource = DevUrandomRandomSource()
    print(randomSource.get_random_bytes(4))
