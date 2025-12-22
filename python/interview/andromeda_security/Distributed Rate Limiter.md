Distributed Rate Limiter


- per user, per API key, per tenant, per endpoint
- P99 should be in ms
- Single API key can be used globally
- Lowest granularity for rate limiting is per second

Architectural characteristics:
- Reliability
- Availability
- Performance
- Elasticity (burstiness)
- Scalability


Workflow:
- Track incoming requests
- Request identification (user cookies, http headers)
- Rate limiting decision 
  - 503
  - Request processing



High Level Components:

-> Regional front Server 
  -> API Server
-> In-Memory System (Redis/Memcached)
  -> Datastore (SQL)


Redis (KV Store):
- (API Key, /path/:id) -> (avg. limit, burst limit, RequestData { Dict: time stamp based map tracking time and count with TTL set in})


R1 - (abc, /users/:id) -> { 20, 100, { 100: 1, 101: 21, 102: 100, 103: 100 }}

R2 - (abc, /users/:id)-> { 20, 100, { 100: 0, 101: 2, 102: 0, 103: 0 }}

Datastore (Auditability)
- User, Session, Timestamp, Origin etc.
- Async tracking with message queue for compliance

