# Accuknox Django Trainee Assignment

## Overview

This repository contains solutions for the Django Trainee assignment.

The assignment contains two parts:

1. Django Signals
2. Custom Classes in Python

---

# Part 1: Django Signals

The objective was to determine:

1. Whether Django signals execute synchronously or asynchronously by default.
2. Whether Django signals execute in the same thread as the caller.
3. Whether Django signals execute within the same database transaction as the caller.

The implementation was done using a small Django project and experiments were performed to verify each behavior.

---

## Question 1

### By default are Django signals executed synchronously or asynchronously?

### Answer

By default, Django signals execute **synchronously**.

Signal receivers are executed immediately when a signal is sent, and the caller waits until all receivers complete execution.

### Proof

A delay was intentionally introduced in the signal receiver:

```python
if instance.label == "sync-test":
    time.sleep(2)
```

The object creation call:

```python
Probe.objects.create(label="sync-test")
```

produced the following output:

```text
sleeping 2 seconds inside receiver...

Time taken for create(): 2.02 seconds
```

### Explanation

Execution flow:

```text
Probe.objects.create()
        ↓
post_save signal triggered
        ↓
receiver executes
        ↓
sleep(2)
        ↓
receiver completes
        ↓
create() returns
```

Since the caller waits for receiver execution to finish, Django signals execute synchronously by default.

---

## Question 2

### Do Django signals run in the same thread as the caller?

### Answer

Yes.

By default, Django signals execute in the same thread as the caller.

### Proof

Thread IDs were printed both in the caller and inside the signal receiver.

Output:

```text
receiver thread id: 8248
caller thread id: 8248
same thread?: True
```

### Explanation

Execution flow:

```text
Caller Thread
        ↓
Probe.objects.create()
        ↓
post_save.send()
        ↓
Signal Receiver
```

The receiver thread ID matched the caller thread ID.

No additional thread was created.

Therefore, Django signals run in the same thread as the caller.

---

## Question 3

### Do Django signals run in the same database transaction as the caller?

### Answer

Yes.

By default, Django signals execute within the same database transaction as the caller.

### Proof

The following transaction block was used:

```python
with transaction.atomic():
    Probe.objects.create(label="transaction-test")
```

Output:

```text
receiver in_atomic_block: True
caller in_atomic_block: True
```

Additional verification:

Before transaction commit:

```text
observer sees row before commit?: False
```

After commit:

```text
on_commit: observer sees row after commit? True
```

### Explanation

Execution flow:

```text
BEGIN TRANSACTION
        ↓
Probe.objects.create()
        ↓
Signal receiver executes
        ↓
COMMIT
```

The receiver executed before the transaction committed.

The second database connection could not see the inserted row until after the commit occurred.

Therefore, Django signals execute within the same database transaction as the caller by default.

---

## How to Run

Create and activate virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Run the signal experiments:

```bash
python manage.py demo_signals
```

Run the custom class demonstration:

```bash
python manage.py demo_rectangle
```

---

# Part 2: Custom Classes in Python

## Requirement

Create a Rectangle class that:

- Accepts length:int and width:int during initialization
- Can be iterated
- Returns:

```text
{'length': value}
{'width': value}
```

## Implementation

```python
class Rectangle:

    def __init__(self,length:int,width:int):
        self.length=length
        self.width=width

    def __iter__(self):

        yield {"length":self.length}
        yield {"width":self.width}
```

## Example

```python
r=Rectangle(10,5)

for item in r:
    print(item)
```

Output:

```text
{'length':10}
{'width':5}
```

## Explanation

The `__iter__()` method makes the class iterable.

When iteration begins:

```python
for item in rectangle:
```

Python internally calls:

```python
rectangle.__iter__()
```

The `yield` keyword returns values one at a time, creating an iterator object automatically.

## Project Structure

```text
accuknox_assignment/
│
├── config/
├── demoapp/
│   ├── models.py
│   ├── signals.py
│   ├── rectangle.py
│   ├── proof_state.py
│   └── management/
│       └── commands/
│           ├── demo_signals.py
│           └── demo_rectangle.py
│
├── manage.py
├── requirements.txt
└── README.md
```

