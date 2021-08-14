from Sources.Internal.DevUrandomRandomSource import DevUrandomRandomSource
import redis

# Redis server informations
REDIS_SERVER = {
    'host': '1.0.0.10',
    'port': 6379
}

if __name__ == '__main__':
    """
    Main method
    """

    # Init local random source
    localRandomSource = DevUrandomRandomSource()
    print(localRandomSource.get_random_bytes(8))

    # Init redis server
    redisClient = redis.Redis(host=REDIS_SERVER['host'], port=REDIS_SERVER['port'], db=0)
    redisClient.set('try', 'this is a try')
    print(redisClient.get('try'))
