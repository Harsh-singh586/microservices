# MICROSERVICES ARCHITECTURE - COMBINED LOAD TEST DATA

**Test Date:** 2025-11-28
**Test Duration:** 10 minutes (600 seconds)
**Max Concurrent Users:** 600

---

## LOAD TEST RESULTS (Locust)

### Overall Performance

| Metric | Value |
|--------|-------|
| Total Requests | 52,103 |
| Total Failures | 11,976 (22.99%) |
| Average Response Time | 270 ms |
| Min Response Time | 0 ms |
| Max Response Time | 10,002 ms |
| Requests per Second | 86.70 |
| Failures per Second | 19.90 |

### Service Breakdown

#### User Service
- **Total Requests:** 21,425
- **Total Failures:** 11,976 (55.90%)

| Method | Endpoint | Requests | Failures | Fail % | Avg (ms) | Min (ms) | Max (ms) |
|--------|----------|----------|----------|--------|----------|----------|----------|
| GET | [USER_SERVICE] /users/ | 14,262 | 8,270 | 57.99% | 621 | 0 | 10,001 |
| GET | [USER_SERVICE] /users/{id}/ | 4,364 | 2,042 | 46.79% | 787 | 0 | 10,002 |
| POST | [USER_SERVICE] /users/ [CREATE] | 2,799 | 1,664 | 59.45% | 599 | 0 | 9,995 |

#### Product Service
- **Total Requests:** 23,899
- **Total Failures:** 0 (0.00%)

| Method | Endpoint | Requests | Failures | Fail % | Avg (ms) | Min (ms) | Max (ms) |
|--------|----------|----------|----------|--------|----------|----------|----------|
| GET | [PRODUCT_SERVICE] /products/ | 15,034 | 0 | 0.00% | 4 | 1 | 133 |
| GET | [PRODUCT_SERVICE] /categories/ | 5,866 | 0 | 0.00% | 4 | 1 | 85 |
| GET | [PRODUCT_SERVICE] /products/?search= | 2,999 | 0 | 0.00% | 4 | 1 | 97 |

#### Order Service
- **Total Requests:** 6,779
- **Total Failures:** 0 (0.00%)

| Method | Endpoint | Requests | Failures | Fail % | Avg (ms) | Min (ms) | Max (ms) |
|--------|----------|----------|----------|--------|----------|----------|----------|
| GET | [ORDER_SERVICE] /orders/?user_id= | 6,779 | 0 | 0.00% | 4 | 1 | 257 |

---

## CONTAINER RESOURCE USAGE (Docker Monitoring)

### Monitoring Summary

| Metric | Value |
|--------|-------|
| Monitoring Duration | 837 seconds (~13 minutes) |
| Total Samples | 279 |
| Sampling Interval | ~3 seconds |
| Containers Monitored | 3 |

### CPU Usage by Container

| Container | Samples | Min % | Max % | Avg % | Median % | P95 % | Spikes >100% |
|-----------|---------|-------|-------|-------|----------|-------|--------------|
| order_service_app | 93 | 0.01 | 43.52 | 2.03 | 1.48 | 2.94 | 0 |
| user_service_app | 94 | 0.01 | 104.04 | 88.17 | 99.63 | 101.87 | 36 |
| product_service_app | 92 | 0.01 | 11.05 | 5.61 | 5.71 | 9.41 | 0 |

### Combined CPU Statistics (All Containers)

| Metric | Value | Notes |
|--------|-------|-------|
| Minimum CPU | 0.01% | Lowest observed across all containers |
| Maximum CPU | 104.04% | Peak usage across all containers |
| Average CPU | 32.23% | Mean across all samples |
| Median CPU | 5.64% | 50th percentile |
| P95 CPU | 101.39% | 95th percentile |

---

## RESOURCE CONFIGURATION

### Application Containers

| Service | CPU Limit | Memory Limit | Workers | Timeout |
|---------|-----------|--------------|---------|---------|
| user_service_app | 1.0 core | 1024 MB | 2 | 10s |
| product_service_app | 1.0 core | 1024 MB | 2 | 10s |
| order_service_app | 1.0 core | 1024 MB | 2 | 10s |
| **TOTAL** | **3.0 cores** | **3072 MB (3 GB)** | **6** | - |

### Database Containers

| Database | CPU Limit | Memory Limit | Max Connections | Shared Buffers |
|----------|-----------|--------------|-----------------|----------------|
| user_service_db | 0.33 core | 683 MB | 200 | 171 MB |
| product_service_db | 0.33 core | 683 MB | 200 | 171 MB |
| order_service_db | 0.34 core | 683 MB | 200 | 171 MB |
| **TOTAL** | **1.0 core** | **2049 MB (~2 GB)** | **600** | **513 MB** |

---

## KEY DATA OBSERVATIONS

### Load Test Observations

1. **Request Volume:** 52,103 total requests over 10 minutes
2. **Throughput:** 86.70 requests/second
3. **Failure Rate:** 22.99% (11,976 failures)
4. **Response Time Range:** 0 ms (min) to 10,002 ms (max)
5. **Average Response Time:** 270 ms

### Service Performance Observations

1. **User Service Failure Rate:** 55.90%
2. **Product Service Failure Rate:** 0.00%
3. **Order Service Failure Rate:** 0.00%
4. **Slowest Endpoint:** GET [USER_SERVICE] /users/{id}/ (avg 787 ms)
5. **Most Requested Endpoint:** GET [PRODUCT_SERVICE] /products/ (15,034 requests)

### CPU Usage Observations

1. **Average CPU Usage:** 32.23% across all containers
2. **Peak CPU Usage:** 104.04%
3. **P95 CPU Usage:** 101.39% (95% of time below this)
4. **order_service_app Average CPU:** 2.03% (max: 43.52%)
5. **user_service_app Average CPU:** 88.17% (max: 104.04%)
6. **product_service_app Average CPU:** 5.61% (max: 11.05%)

### Load Pattern Observations

1. **User Ramp:** 120 → 240 → 420 → 600 users over 10 minutes
2. **Traffic Distribution:** Service weights 33:34:33 (User:Product:Order)
3. **Peak Concurrent Users:** 600 at minutes 7-10

---

## DATA SUMMARY

### Performance Metrics

| Category | Metric | Value |
|----------|--------|-------|
| Throughput | Requests/sec | 86.70 |
| Reliability | Failure Rate | 22.99% |
| Latency | Avg Response | 270 ms |
| Latency | Max Response | 10,002 ms |
| Resource | Avg CPU | 32.23% |
| Resource | Max CPU | 104.04% |

### Endpoint Performance Ranking (by avg response time)

| Rank | Endpoint | Avg Response (ms) | Requests | Failures |
|------|----------|-------------------|----------|----------|
| 1 | GET [USER_SERVICE] /users/{id}/ | 787 | 4,364 | 2,042 |
| 2 | GET [USER_SERVICE] /users/ | 621 | 14,262 | 8,270 |
| 3 | POST [USER_SERVICE] /users/ [CREATE] | 599 | 2,799 | 1,664 |
| 4 | GET [ORDER_SERVICE] /orders/?user_id= | 4 | 6,779 | 0 |
| 5 | GET [PRODUCT_SERVICE] /categories/ | 4 | 5,866 | 0 |
| 6 | GET [PRODUCT_SERVICE] /products/ | 4 | 15,034 | 0 |
| 7 | GET [PRODUCT_SERVICE] /products/?search= | 4 | 2,999 | 0 |
