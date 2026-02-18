### Fraud Detection on Streaming Data using Kafka

## Overview

This project implements a real-time fraud detection system using Kafka and Redis.

Transactions are streamed into Kafka.
A consumer processes transactions within a time window and detects suspicious activity.
Fraud alerts are published to a separate Kafka topic.

The system demonstrates:

Event-driven architecture

Kafka producer/consumer fundamentals

Manual offset management

Redis-based sliding window detection

Idempotent and configurable processing

