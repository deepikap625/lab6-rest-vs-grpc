
| Method          | Local (ms/query) | Same-Zone (ms/query) | Different Region (ms/query) |
|-----------------|-----------------:|---------------------:|----------------------------:|
| REST add        | 2.254            | 3.231                | Pending                     |
| gRPC add        | 0.349            | 1.059                | Pending                     |
| REST rawimg     | 4.255            | 7.193                | 1385.351                    |
| gRPC rawimg     | 3.254            | 9.545                | Pending                     |
| REST dotproduct | 2.550            | 3.870                | Pending                     |
| gRPC dotproduct | 0.429            | 1.246                | Pending                     |
| REST jsonimg    | 29.737           | 30.971               | Pending                     |
| gRPC jsonimg    | 10.684           | 14.359               | Pending                     |
| PING            | Not measured     | 0.434                | Not measured                |

These numbers are based on the results you previously recorded. The cross-region REST raw-image measurement is approximately 1,385.351 ms per operation. The other cross-region entries are still pending; we won't guess them.
Important: The ping result of 0.434 ms is for the same-zone connection between your client and the US server.

## Performance Observations

The local and same-zone measurements generally show that gRPC provides lower latency than REST, particularly for lightweight operations such as addition and dot product. This is because gRPC uses Protocol Buffers for compact binary serialization and communicates over HTTP/2, reducing serialization and communication overhead. For image processing, the JSON-image method takes longer than the raw-image method because Base64 encoding increases the payload size and requires additional encoding and decoding. Network latency also affects performance when the client and server are in different regions. In our measurements, the REST raw-image operation took approximately 1,385 ms per query across regions, illustrating the potential impact of network distance. However, the remaining cross-region measurements could not be completed because the Google Cloud billing account was closed. Overall, the available results suggest that gRPC is more efficient for these operations, although performance depends on payload size, network conditions, and implementation details.
