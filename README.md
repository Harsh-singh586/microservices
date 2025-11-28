# E-commerce Microservices

## Architecture

```
┌─────────────────┐                    ┌──────────────────┐
│   User Service  │                    │  Product Service │
│   Port: 8000    │                    │   Port: 8001     │
│                 │    NO DIRECT       │                  │
│   - Users       │    COMMUNICATION   │   - Products     │
│   - Profiles    │                    │   - Inventory    │
└─────────────────┘                    └──────────────────┘
         ▲                                        ▲
         │                                        │
         │ HTTP/JSON                   HTTP/JSON  │
         │ (User Info)              (Stock Check) │
         │                           (Inventory)  │
         ▼                                        ▼
┌─────────────────────────────────────────────────────────┐
│               Order Service (Port: 8002)                │
│                                                         │
│  🔄 Orchestrates business operations:                   │
│  • Validates users via User Service                    │
│  • Checks stock via Product Service                    │
│  • Updates inventory via Product Service               │
│  • Coordinates order creation with transactions        │
└─────────────────────────────────────────────────────────┘
```

**Communication Pattern:** Hub-and-Spoke Architecture with synchronous HTTP/JSON

## Quick Start

```bash
# Start all services
docker-compose up --build

# Load sample data (in a new terminal)
python create_sample_data.py
```

## Resource Allocation

### Services

| Service          | CPU Limit | Memory Limit | Replicas |
|------------------|-----------|--------------|----------|
| User Service     | 1.0       | 1024MB       | 1        |
| Product Service  | 1.0       | 1024MB       | 1        |
| Order Service    | 1.0       | 1024MB       | 1        |
| **Total**        | **3.0**   | **3072MB**   | **3**    |

### Databases

| Database         | CPU Limit | Memory Limit | Replicas |
|------------------|-----------|--------------|----------|
| User DB          | 0.33      | 683MB        | 1        |
| Product DB       | 0.33      | 683MB        | 1        |
| Order DB         | 0.34      | 683MB        | 1        |
| **Total**        | **1.0**   | **2049MB**   | **3**    |
