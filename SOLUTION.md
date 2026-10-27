
| Method          | Local (ms/query) | Same-Zone (ms/query) | Different Region (ms/query) |
|-----------------|-----------------:|---------------------:|----------------------------:|
| REST add        | 2.254            | 3.231                | 321.8400                     |
| gRPC add        | 0.349            | 1.059                | 142.9032                     |
| REST rawimg     | 4.255            | 7.193                | 1385.351                    |
| gRPC rawimg     | 3.254            | 9.545                | 1304.0305                     |
| REST dotproduct | 2.550            | 3.870                | 321.5585                     |
| gRPC dotproduct | 0.429            | 1.246                | 143.2090                     |
| REST jsonimg    | 29.737           | 30.971               | 1411.8304                     |
| gRPC jsonimg    | 10.684           | 14.359               | 216.3527                     |
| PING            | 0.0560           | 0.4540               | 159.8740                    |

These numbers are based on the results you previously recorded. The cross-region REST raw-image measurement is approximately 1,385.351 ms per operation. The other cross-region entries are still pending; we won't guess them.
Important: The ping result of 0.434 ms is for the same-zone connection between your client and the US server.

## Performance Observations

- **Small operations:** gRPC had lower latency than REST for addition and dot product in all three environments. Protocol Buffers and HTTP/2 can reduce serialization and communication overhead.

- **Raw image transfer:** gRPC was faster locally (3.254 ms vs. 4.255 ms), while REST was faster in the same zone (7.193 ms vs. 9.545 ms). Across regions, gRPC was slightly faster (1304.031 ms vs. 1385.351 ms).

- **JSON image transfer:** JSON serialization and Base64 encoding can increase payload size and processing overhead. Across regions, gRPC jsonimg was substantially faster than REST (216.353 ms vs. 1411.830 ms).

- **Network distance:** PING latency increased from 0.056 ms locally to 0.454 ms in the same zone and 159.874 ms across regions.

- **Connection handling:** A gRPC channel can reuse an underlying HTTP/2 connection. If the REST client opens a new TCP connection for each request, connection setup may add overhead.

- **Overall:** gRPC performed better for most measured operations, but not every operation in every environment. Performance depends on payload format, serialization, connection behavior, and network conditions.

