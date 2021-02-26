from fluent import sender
import argparse
import redis
import json


def main():
    parser = argparse.ArgumentParser(
        description="test fluent"
    )
    parser.add_argument(
        "--prefix",
        required=True,
        default="app",
        help="fluentd match prefix"
    )
    args = parser.parse_args()
    if args.prefix == "app":
        logger = sender.FluentSender('app', host='localhost', port=24224)
        logger.emit('follow', {'from': 'user1', 'to': 'user2'})
    elif args.prefix == "mongo_app":
        logger = sender.FluentSender('mongo_app', host='localhost', port=24224)
        logger.emit('follow', {'from': 'user2', 'to': 'user1'})
    elif args.prefix == "redis_app":
        logger = sender.FluentSender('redis_app', host='localhost', port=24224)
        logger.emit('follow', {'from': 'userC', 'to': 'userD'})
    elif args.prefix == "get_redis":
        r = redis.Redis(host="localhost", port=6379)
        print([json.loads(item) for item in r.zrange("fluent", 0, -1)] )
    print("done.")
    

if __name__ == "__main__":
    main()
