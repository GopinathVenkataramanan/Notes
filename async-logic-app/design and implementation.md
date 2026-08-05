# Azure Async Service Orchestration Design

## Logic Apps Standard + API Management + Service Bus + Cosmos DB

## 1. Overview

This document describes the design and implementation approach for an asynchronous service orchestration pattern using:

* Azure Logic Apps Standard
* Azure API Management (APIM)
* Azure Service Bus
* Azure Cosmos DB
* Downstream transaction processing systems

The solution enables:

1. A caller workflow to initiate a long-running asynchronous transaction.
2. Immediate acknowledgement with a correlation reference.
3. Downstream processing through Service Bus.
4. Completion notification through a response queue.
5. Resumption of the original Logic App workflow using a webhook callback mechanism.

---

# 2. Solution Architecture

```
                           Request
                              |
                              v

+------------------------------------------------+
| Logic App Standard Workflow 1                  |
| Orchestrator                                   |
|                                                |
| HTTP Webhook Action                            |
| - Sends async request                          |
| - Generates callback URL                       |
| - Waits for completion callback                |
+------------------------------------------------+
                              |
                              |
                              v

+------------------------------------------------+
| Azure API Management                           |
|                                                |
| - Authentication                               |
| - Validation                                   |
| - Routing                                      |
+------------------------------------------------+
                              |
                              v

+------------------------------------------------+
| Logic App Standard Workflow 2                  |
| Publisher                                      |
|                                                |
| 1. Receive request                             |
| 2. Generate Reference ID                       |
| 3. Store callback URL in Cosmos DB             |
| 4. Publish message to Service Bus Out Queue    |
+------------------------------------------------+
                              |
                              v

              Service Bus Out Queue

                              |
                              v

+------------------------------------------------+
| Downstream Processing System                   |
|                                                |
| - Consume transaction message                  |
| - Execute business processing                  |
+------------------------------------------------+

                              |
                              v

              Service Bus In Queue

                              |
                              v

+------------------------------------------------+
| Logic App Standard Workflow 3                  |
| Subscriber                                     |
|                                                |
| 1. Receive completion message                  |
| 2. Read callback URL from Cosmos DB            |
| 3. Invoke Logic App Workflow 1 callback        |
+------------------------------------------------+

                              |
                              v

+------------------------------------------------+
| Logic App Workflow 1                           |
|                                                |
| Webhook resumes                                |
| Continue orchestration                         |
+------------------------------------------------+
```

---

# 3. Workflow Components

## Workflow 1 - Async Orchestrator

### Purpose

Responsible for:

* Receiving the original business request.
* Calling the publisher workflow.
* Waiting asynchronously.
* Continuing after completion callback.

---

## Trigger

Example:

```
HTTP Request Trigger
```

Input:

```json
{
    "customerId": "12345",
    "transactionType": "Order",
    "payload": {
        "amount":100
    }
}
```

---

## Webhook Action

Workflow 1 uses:

```
HTTP Webhook Action
```

The webhook action generates a callback URL.

Example:

```
https://logicapp.azure.com/workflows/.../callback?sig=xxxxx
```

The workflow remains suspended until the callback URL is invoked.

---

# 4. Workflow 2 - Publisher Logic App

## Purpose

Responsible for:

* Receiving async request.
* Creating correlation reference.
* Persisting callback information.
* Publishing work item.

---

## Trigger

```
When HTTP Request is Received
```

Request:

```json
{
    "requestId":"REQ-10001",
    "callbackUrl":"https://logicapp.callback.url",
    "transactionType":"Order",
    "payload":{
        "orderId":"ORD123"
    }
}
```

---

# 5. Reference ID Generation

Generate unique identifier:

Example:

```
referenceId = UUID
```

Example:

```
7a1d9f02-33d4-4db2-a12f
```

This identifier becomes the correlation key across:

* Cosmos DB
* Service Bus messages
* Downstream processing
* Completion events

---

# 6. Cosmos DB Data Model

## Database

```
AsyncProcessing
```

## Container

```
TransactionCallbacks
```

## Partition Key

Recommended:

```
/id
```

---

## Document Example

```json
{
    "id":"7a1d9f02-33d4-4db2-a12f",
    "requestId":"REQ-10001",
    "callbackUrl":"https://logicapp.callback.url",
    "transactionType":"Order",
    "status":"Submitted",
    "createdDate":"2026-08-05T01:00:00Z",
    "expiryDate":"2026-08-06T01:00:00Z"
}
```

---

# 7. Service Bus Out Queue

## Queue Name

Example:

```
transaction-request-out
```

---

## Message

```json
{
    "referenceId":"7a1d9f02-33d4-4db2-a12f",
    "requestId":"REQ-10001",
    "transactionType":"Order",
    "payload":{
        "orderId":"ORD123"
    }
}
```

---

## Recommended Message Properties

| Property      | Value            |
| ------------- | ---------------- |
| MessageId     | referenceId      |
| CorrelationId | requestId        |
| Subject       | transaction type |
| TTL           | Business timeout |

---

# 8. Downstream Processing

The downstream application:

1. Reads messages from:

```
transaction-request-out
```

2. Processes the transaction.

3. Publishes completion message to:

```
transaction-response-in
```

---

# 9. Completion Message

Example:

```json
{
    "referenceId":"7a1d9f02-33d4-4db2-a12f",
    "status":"Completed",
    "transactionId":"TX123456",
    "result":{
        "orderStatus":"Approved"
    }
}
```

---

# 10. Workflow 3 - Subscriber Logic App

## Trigger

Azure Service Bus Trigger:

```
When a message is received in a queue
```

Queue:

```
transaction-response-in
```

---

## Processing Steps

### Step 1

Read:

```
referenceId
```

Example:

```
7a1d9f02-33d4-4db2-a12f
```

---

### Step 2

Query Cosmos DB:

```sql
SELECT *
FROM c
WHERE c.id='7a1d9f02-33d4-4db2-a12f'
```

Retrieve:

```json
{
    "callbackUrl":"https://logicapp.callback.url"
}
```

---

### Step 3

Invoke Callback

HTTP POST:

```
callbackUrl
```

Payload:

```json
{
    "referenceId":"7a1d9f02-33d4-4db2-a12f",
    "status":"Completed",
    "transactionId":"TX123456"
}
```

---

# 11. Error Handling

## Transaction State Model

```
Submitted
    |
Processing
    |
Completed
    |
Failed
    |
TimedOut
```

---

## Cosmos Status Update Example

```json
{
    "id":"7a1d9f02",
    "status":"Failed",
    "errorMessage":"Validation failed"
}
```

---

# 12. Security Design

## Authentication

Recommended:

* Managed Identity
* Azure RBAC
* APIM OAuth/JWT validation

Avoid:

* Stored connection strings
* Hardcoded secrets

---

## Callback URL Protection

Callback URLs contain authentication signatures.

Recommended:

* Encrypt sensitive fields.
* Apply Cosmos TTL.
* Remove completed records after retention period.

---

# 13. Cosmos TTL Strategy

Example:

```
TTL = 86400 seconds
```

Records automatically expire after completion timeout.

---

# 14. Service Bus Reliability

Enable:

## Duplicate Detection

Use:

```
MessageId = referenceId
```

Prevents duplicate processing.

---

## Dead Letter Queue

Configure:

* Maximum delivery attempts
* Monitoring alerts
* Retry policies

---

# 15. Monitoring

Recommended Azure Monitor metrics:

## Logic Apps

Monitor:

* Failed runs
* Suspended runs
* Callback timeout

## Service Bus

Monitor:

* Queue length
* Dead letters
* Incoming/outgoing messages

## Cosmos DB

Monitor:

* RU consumption
* Query latency
* Storage growth

---

# 16. APIM Responsibilities

APIM provides:

* API security
* Authentication
* Rate limiting
* Request validation
* Version management
* Logging

Example API:

```
POST /transactions
```

Backend:

```
Logic App Workflow 2 HTTP Trigger
```

---

# 17. Deployment Components

Azure resources:

| Resource              | Purpose             |
| --------------------- | ------------------- |
| Logic App Standard    | Workflow hosting    |
| API Management        | API gateway         |
| Service Bus Namespace | Messaging           |
| Service Bus Queues    | Async communication |
| Cosmos DB Account     | Callback state      |
| Application Insights  | Monitoring          |
| Azure Monitor         | Alerts              |

---

# 18. End-to-End Sequence

```
1. Client calls Workflow 1

2. Workflow 1 generates webhook callback

3. Workflow 1 calls APIM

4. APIM invokes Workflow 2

5. Workflow 2:
      - Creates referenceId
      - Stores callback URL
      - Sends Service Bus message

6. Downstream consumes message

7. Downstream completes transaction

8. Downstream sends completion event

9. Workflow 3 receives event

10. Workflow 3 retrieves callback URL

11. Workflow 3 invokes callback

12. Workflow 1 resumes execution
```

---

# 19. Benefits of This Design

* Fully asynchronous processing
* Loose coupling between systems
* Durable orchestration
* Reliable message delivery
* Scalable downstream processing
* Transaction correlation
* Fault isolation
* Enterprise integration pattern alignment

---

# 20. Recommended Enhancements

Future improvements:

* Add Azure Durable Functions for complex state management.
* Add Event Grid for event-driven notifications.
* Add compensation workflows for failed transactions.
* Add API versioning in APIM.
* Add distributed tracing using Application Insights correlation IDs.

---

## Conclusion

This architecture provides a robust asynchronous orchestration framework using Azure managed services. Logic Apps provide workflow durability, Service Bus provides reliable messaging, Cosmos DB provides correlation state storage, and APIM provides enterprise API governance.
