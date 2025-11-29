# Microservices Load Test - Combined Data Summary
**Test Date:** 2025-11-29

## Overall Performance

| Metric | Value |
|--------|-------|
| Total Requests | 47,273 |
| Total Failures | 14,799 (31.3%) |
| Average Response Time | 117 ms |
| Min Response Time | 0 ms |
| Max Response Time | 9,857 ms |
| Requests per Second | 78.7 |
| Failures per Second | 24.6 |

### Response Time Percentiles

| Percentile | Response Time (ms) |
|------------|-------------------|
| 50th | 13 |
| 75th | 21 |
| 90th | 210 |
| 95th | 580 |
| 99th | 2,400 |
| 99.9th | 9,900 |

## CPU Statistics by Service

### ORDER_SERVICE

| Metric | Value |
|--------|-------|
| Samples | 93 |
| Min CPU | 0.02% |
| Max CPU | 45.22% |
| Average CPU | 4.46% |
| Median CPU | 1.14% |
| P95 CPU | 22.33% |
| P99 CPU | 45.22% |

### PRODUCT_SERVICE

| Metric | Value |
|--------|-------|
| Samples | 93 |
| Min CPU | 0.01% |
| Max CPU | 56.64% |
| Average CPU | 25.75% |
| Median CPU | 25.89% |
| P95 CPU | 42.47% |
| P99 CPU | 56.64% |

### USER_SERVICE

| Metric | Value |
|--------|-------|
| Samples | 93 |
| Min CPU | 0.07% |
| Max CPU | 108.55% |
| Average CPU | 98.19% |
| Median CPU | 100.10% |
| P95 CPU | 103.20% |
| P99 CPU | 108.55% |

## Key Observations

1. **High Failure Rate**: 31.3% failure rate indicates significant issues
2. **User Service Bottleneck**: User service shows high CPU utilization
3. **Response Time Variability**: Max response time (9.8s) vs average (117ms) shows inconsistency
4. **Throughput**: 78.7 RPS with 3 separate services

