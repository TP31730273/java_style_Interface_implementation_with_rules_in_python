# Generic Interface Enforcement in Python

A reusable, Java-inspired interface enforcement system for Python using `ABC`, `abstractmethod`, `Generic`, `TypeVar`, and `__init_subclass__`.

## Overview

This implementation provides a strict base `Interface` class that can be reused across application domains to enforce contracts on concrete implementations.

It demonstrates how Python can provide stronger interface-level guarantees while retaining Python's flexibility.

## Features

* **Generic Interfaces**

  * Uses `Generic`, `TypeVar`, `TRequest`, and `TResponse` to define strongly typed request/response contracts.

* **Abstract Method Enforcement**

  * Uses `ABC` and `@abstractmethod` to define methods that every concrete implementation must provide.

* **Class Naming Enforcement**

  * Uses `__init_subclass__` to enforce naming conventions.
  * For example, all `Gateway` implementations must end with `Gateway`:

    * `StripeGateway` ✅
    * `RazorpayGateway` ✅
    * `Stripe` ❌

* **Fail-Fast Validation**

  * Invalid implementations are rejected during class creation rather than allowing architectural violations to propagate into application runtime.

* **Reusable Interface Foundation**

  * The `Interface` class is designed as a common foundation that can be extended for other domains such as:

    * Payment gateways
    * Notification providers
    * Storage adapters
    * Authentication providers
    * Message brokers
    * External API clients

## Example Architecture

```text
Interface[TRequest, TResponse]
            │
            ▼
        Gateway
            │
     ┌──────┼────────┐
     ▼      ▼        ▼
 Stripe   Razorpay  PayPal
 Gateway   Gateway  Gateway
```

The `Gateway` interface defines the required contract:

```python
charge(request)
refund(request)
```

Every concrete gateway implementation must satisfy that contract.

## Example

```python
class Gateway(Interface[dict, dict]):

    interface_suffix = "Gateway"

    @abstractmethod
    def charge(self, request: dict) -> dict:
        ...

    @abstractmethod
    def refund(self, request: dict) -> dict:
        ...
```

A valid implementation:

```python
class StripeGateway(Gateway):

    def charge(self, request: dict) -> dict:
        ...

    def refund(self, request: dict) -> dict:
        ...
```

An invalid implementation:

```python
class Stripe(Gateway):
    ...
```

fails because it violates the naming convention.

Likewise:

```python
class RazorpayGateway(Gateway):

    def charge(self, request: dict) -> dict:
        ...
```

fails because `refund()` has not been implemented.

## Why `__init_subclass__`?

`__init_subclass__` provides a convenient hook for validating subclasses when they are created.

One important implementation detail is that `ABCMeta` populates `__abstractmethods__` after `__init_subclass__` executes. Therefore, this implementation does not directly depend on `cls.__abstractmethods__` during subclass initialization. Instead, it inspects the inherited abstract methods and validates the subclass explicitly.

## Design Goal

The goal is not to make Python behave exactly like Java. Instead, this implementation combines Python's native mechanisms to provide:

```text
Generics
   +
Abstract Interfaces
   +
Naming Conventions
   +
Contract Enforcement
   +
Fail-Fast Validation
```

This creates a predictable architecture for large Python applications while keeping the implementation explicit and reusable.
