# Incident review workflow

Interview design notes for a synthetic laboratory. This is not a description of a system I operated in a bank.

## Requirements

Incident review workflow must produce a decision or a report a person can act on, with a definition of the entity, the time, and the label.

## Scale assumptions

State them. A credit application path is not an authorization path. If you do not know the rate, say the number you are designing for and what breaks if you are off by 10x.

## Data ingestion

Events land once, with a key and an event time. Late events are corrected in the offline store. The online path does not wait for perfection.

## Storage

Raw events are durable. Features are derived. The decision log is immutable. Training reads snapshots, not the live mutable row.

## Processing

Batch builds seasoned training sets. Stream or service logic builds only what the live decision needs.

## Features

Every feature has a definition, a window, and a timestamp. Point-in-time correctness is a test, not a slogan.

## Model

A baseline sits next to the model. The model is versioned. The policy that uses the score is a separate object.

## Serving

A latency budget, a timeout, and a fallback. The fallback is a rule the business has agreed to.

## Monitoring

Inputs, scores, decisions, and matured outcomes. Alerts have volume floors and owners.

## Failure handling

Fail to the fallback, log the failure, and do not train on a broken day as if it were normal.

## Security

Minimum permissions, encrypted transport, and restricted identifiers. This note is not a legal or compliance attestation.

## Trade-offs

For Incident review workflow, name what you are giving up: latency versus freshness, approval versus loss, or simplicity versus a second model. Pick a side and say what evidence would change it.
