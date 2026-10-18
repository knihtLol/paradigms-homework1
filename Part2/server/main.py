
import sys
from http.server import HTTPServer

from http_layer import Handler


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    if len(sys.argv) > 2:
        Handler.wsdl_path = sys.argv[2]
    print(f'ChatRoom server on port {port}; '
          f'serving contract {Handler.wsdl_path} at /?wsdl')
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()


if __name__ == '__main__':
    main()