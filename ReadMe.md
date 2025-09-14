# Data Lake Formats - Exploring Apache Hudi – Merge-on-Read vs Copy-on-Write

## Overview
The modern data lakehouse ecosystem is dominated by three open table formats: **Apache Hudi**, **Delta Lake**, and **Apache Iceberg**. While they share common goals — ACID transactions, schema evolution, and time travel — each has distinct design choices, strengths, and trade-offs.

This repository explores **Apache Hudi** as a storage layer for building reliable and scalable Data Lakes. Instead of a basic tutorial, the focus here is on **architectural trade-offs** and **decision-making** when choosing between Hudi’s two core table types:

- **Copy-on-Write (COW)** – Optimized for read performance.
- **Merge-on-Read (MOR)** – Optimized for write performance.

The notebooks and documentation here showcase **capabilities**, including **upserts/deletes, time travel queries, schema evolution, indexing, and incremental pulls**.


## Why This Matters
Modern data platforms must constantly balance **latency, freshness, and operational complexity**:
- Do you prioritize **fast queries on immutable snapshots**?
- Or do you prioritize **low-latency ingestion with near real-time availability**?

This repo demonstrates both modes, highlighting real-world **trade-offs, workload patterns, and decision frameworks**.


## Capabilities Explored
Across both COW and MOR notebooks, the following are demonstrated:
- **Upserts and Deletes** – Using `MERGE INTO` or DataFrame upsert for efficient mutations.
- **Table Types** – Comparing COW (better for reads) vs MOR (better for writes).
- **Time Travel Queries** – Querying with `AS OF TIMESTAMP`.
- **Schema Evolution** – Supporting schema updates during ingestion.
- **Indexing** – Using Bloom Filter indexes for faster lookups.
- **Incremental Pulls** – Fetching changes since a given commit.

## Copy-on-Write (COW)
**Characteristics:**
- Write Amplification: Rewrites entire files, slower for frequent updates.
- Read Performance: Reads are fast and consistent (compacted files).
- Use Case: Ideal for read-heavy workloads, periodic batch updates, and BI/reporting.

**Best Scenarios:**
- Batch processing and analytics (nightly ETL into reporting layer).
- Read-heavy applications (dashboards, ML inference).
- Immutable or slowly changing data.
- Teams prioritizing **simplicity and predictable performance**.

**Example:** Retail company updating sales data nightly; BI analysts need fast queries.

## Merge-on-Read (MOR)
**Characteristics:**
- Writes: Appends logs (low latency, streaming-friendly).
- Reads: Merge base + delta on the fly (slower until compaction).
- Use Case: Ideal for real-time ingestion, high-frequency updates, and CDC pipelines.

**Best Scenarios:**
- Real-time streaming data (IoT sensors, clickstreams).
- CDC from OLTP systems into the data lake.
- Write-heavy workloads (social media events, transactions).
- Event-driven applications where low write latency is critical.

**Example:** Ride-sharing platform ingesting driver location updates in near real-time.

## Decision Matrix
| Dimension             | Copy-on-Write (COW) | Merge-on-Read (MOR) |
|-----------------------|---------------------|----------------------|
| **Write Latency**     | Higher (rewrites)   | Lower (append-only) |
| **Read Latency**      | Lower (fast reads)  | Higher (depends on compaction) |
| **Freshness**         | Batch-oriented      | Near real-time      |
| **Operational Overhead** | Lower            | Higher (manage compactions) |
| **Best Use Case**     | BI/Analytics, Warehousing | Streaming, CDC, Real-time Insights |

## Architecture Diagram


## Sample Project: Trip Data with COW & MOR
This project manages **trip records** (UUID, rider, driver, fare, city, timestamp):
- **COW Table** – Optimized for batch queries, periodic updates.
- **MOR Table** – Optimized for real-time updates, compaction-enabled.

The notebooks walk through ingestion, updates, deletes, incremental pulls, and time-travel queries.

## Decision-Making Guide
- Choose **COW** if:
  - Read performance is critical.
  - Updates are infrequent or batched.
  - Operational simplicity is key.

- Choose **MOR** if:
  - Writes are frequent, streaming, or CDC-based.
  - Low-latency ingestion is required.
  - You can manage compaction overhead.

---
Use this repo to benchmark both approaches, understand trade-offs, and inform **architectural decisions** for your Data Lakehouse design.

