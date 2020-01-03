# ordered online order service

This django based micro service provides an API to obtain orders placed at a location.

## Code Idea and Schematic Layout

![order panel scheme](assets/order-panel-scheme.png)

The core idea of this service is to allow order placement. Here is the workflow:

1. The location representative authenticates himself and opens the order panel. The order panel contains `OrderSessions`, which each have a state: `open` and `closed` (see layout).
2. In the order panel, the location representative creates an order session with an identifier (e.g. "Table 2"). The order session is now `open`. The order session automatically obtains a (qr renderable) code from the `codes` service. In the UI of the location representative, a WebSocket ist opened, which connects to the endpoint for the order session and therefore receives all messages, which are related to this order session (i.e., orders themselves).
3. Clicking the order session in the leftmost column triggers a modal to be presented, which contains the QR code.
4. User scans this QR code. The user connects to the same WebSocket channel by the obtained code, so that user and location representative are connected with each other from now on.
5. The user can order products (these products are inferred by the `products` service) and those orders are pushed to the corresponding WebSocket channel, so that they are displayable by the location representative's UI.
6. The location representative can see all orders of a session in a modal, which is presented, when clicking on the corresponding session.
7. The location representative can close the order session. This posts a message to the user's WebSocket connection and triggers a UI change on the user side, which indicates, that the session was closed.

## Technology Stack

- Python 3
- Django
- WebSockets
- Redis as the backend for Django Channels

## Quickstart

```
$ python3 -m pip install -r requirements.txt
```

Run the server in development mode.

```
$ cd orders
$ docker run -p 6379:6379 -d redis:2.8
$ python3 manage.py migrate
$ python3 manage.py runserver 127.0.0.1:8004
```

Make sure, that the channel layer can communicate with the redis service.

```
$ python3 manage.py shell

In [1]: import channels.layers

In [2]: channel_layer = channels.layers.get_channel_layer()

In [3]: from asgiref.sync import async_to_sync

In [4]: async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})

In [5]: async_to_sync(channel_layer.receive)('test_channel')

Out[5]: {'type': 'hello'}
```

In the debug configuration, we need:

- The `verification` service (by default on `127.0.0.1:8000`)
- The `locations` service (by default on `127.0.0.1:8001`)
- The `products` service (by default on `127.0.0.1:8002`)
- The `codes` service (by default on `127.0.0.1:8003`)
- The `orders` service itself on any arbitrary port other than 8000...8003, we use `127.0.0.1:8004` for this developer documentation
