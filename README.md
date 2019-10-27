# ordered online order service

This django based micro service provides an API to obtain orders placed at a location.

## Technology Stack

- Python 3
- Django

## Quickstart

```
$ python3 -m pip install -r requirements.txt
```

Run the server in development mode.
```
$ cd codes
$ docker run -p 6379:6379 -d redis:2.8
$ python3 manage.py migrate
$ python3 manage.py runserver 127.0.0.1:8004
```

Make sure, that the channel layer can commmunicate with the redis service.
```
$ python3 manage.py shell

In [1]: import channels.layers                                                                                    

In [2]: channel_layer = channels.layers.get_channel_layer()                                                       

In [3]: from asgiref.sync import async_to_sync                                                                    

In [4]: async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})                                      

In [5]: async_to_sync(channel_layer.receive)('test_channel')     
                                                 
Out[5]: {'type': 'hello'}
```

## API Endpoints

Following API Endpoints are supported:

`TODO`
