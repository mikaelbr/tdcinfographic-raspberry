tdcinfographic-raspberry
========================

Server component to the tdcinfographic application. Connecting to
the tdcinfographic Node.js app through WebSockets.

This is a server ment to run on a linux platform connected to a
Dymo M5 scale through USB and a receiving client/server through
WebSockets using Socket.IO.

While running, this application will continuously emit the read
weight (in grams) from a Dymo M5 weight through WebSockets to
the given server.

## Usage

To emit data, we need to connect to a WebSocket server. This
server is defined using the following arguments:

```
$ python server.py [host=localhost] [port=3000]
```

Where port is dependent on server.

### Examples

If your Socket.IO server is on http://localhost:5000

```
$ python server.py localhost 5000
```
---

If your Socket.IO server is on http://localhost:3000

```
$ python server.py localhost 3000
```

---

If your Socket.IO server is on http://something.herokuapp.com

```
$ python server.py something.herokuapp.com 80
```

## Configuration

This server has two modes: Development and Production. This setting
is set by using enviroment variables:

```
export PYTHON_ENV="development"
```

or (default)

```
export PYTHON_ENV="production"
```

If the `PYTHON_ENV` variable is set to development, a stubbed
version of the USB scale is used. This means there is no need
to be connected to the actual USB device.


## Got another Dymo device?

If you got another Dymo device, you can define the product id
by setting the following variable:

```
PRODUCT_ID = 0x8005
```

E.g., The M25 device has the ID `8004`.