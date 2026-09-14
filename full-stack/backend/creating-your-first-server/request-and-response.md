# Request and Response

## Reading What the Client Sent

```js
const server = createServer((req, res) => {
  console.log(req.method);  // "GET", "POST", "PUT", "DELETE", ...
  console.log(req.url);     // "/products/42?color=blue"
  console.log(req.headers); // { host: "localhost:3000", "user-agent": "...", ... }
});
```

The `req` object — an `http.IncomingMessage` — carries everything the client sent: `req.method`
(which HTTP verb was used), `req.url` (the path, and any query string, as one raw string), and
`req.headers` (an object of every header the client sent, with keys automatically lowercased).

## Reading a Request Body

```js
const server = createServer((req, res) => {
  let body = "";

  req.on("data", (chunk) => {
    body += chunk;
  });

  req.on("end", () => {
    const data = JSON.parse(body);
    console.log(data); // the parsed request body, e.g. { name: "Keyboard" }
    res.end("received");
  });
});
```

Unlike `req.method` or `req.url`, a request's **body** (the actual data sent with a POST or PUT
request) doesn't arrive all at once as a ready value — it arrives as a stream of `data` events,
each carrying one chunk, followed by an `end` event once the whole body has arrived. This
chunk-by-chunk delivery is deliberate: a request body could be very large, and Node hands it to you
incrementally rather than forcing it to be fully buffered in memory before your code can even start
reacting to it.

## Sending a Response

```js
res.writeHead(200, { "Content-Type": "application/json" });
res.end(JSON.stringify({ message: "Success" }));
```

`res.writeHead(statusCode, headers)` sets the response's status code (per
[http-status-codes.md](http-status-codes.md)) and headers — it must be called **before** any
response body is sent. `res.end(data)` sends the final chunk of the response body and signals that
the response is complete; calling it without any argument sends an empty body and simply closes out
the response.

## `Content-Type` Actually Matters

```js
// Plain text
res.writeHead(200, { "Content-Type": "text/plain" });
res.end("Hello");

// JSON — the client needs this header to know how to parse the body correctly
res.writeHead(200, { "Content-Type": "application/json" });
res.end(JSON.stringify({ hello: "world" }));
```

The `Content-Type` header tells the client how to interpret the bytes in the response body. Sending
JSON data without setting `Content-Type: application/json` still technically works in many cases
(the client can often guess), but it's incorrect and can break clients (or tools like Postman) that
rely on it to decide how to parse and display the response correctly.

## Common Mistakes

- Calling `res.writeHead()` *after* already calling `res.end()` (or writing data another way) —
  headers must be set before the body starts, and Node throws an error if this order is violated.
- Forgetting to call `res.end()` at all — the response never completes, and the client's request
  hangs indefinitely waiting for it.
- Treating `req`'s body as immediately available like `req.method` — it arrives as a stream and
  must be collected via `data`/`end` events (or, more conveniently, a framework's built-in body
  parser, covered in [Express.js Fundamentals](../expressjs-fundamentals/)) before it can be used.

## Next

Continue to [routing-basics.md](routing-basics.md) to respond differently depending on which URL
and method a request actually used.
