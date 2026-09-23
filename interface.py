from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class Interface(ABC, Generic[TRequest, TResponse]):
    """
    Base class for all interfaces.

    Rules:
    1. Implementations must follow the configured class-name suffix.
    2. Implementations must implement all abstract methods.
    """

    interface_suffix: str | None = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # ---------------------------------------------------------
        # 1. Class-name validation
        # ---------------------------------------------------------

        if cls.interface_suffix is not None:

            if not cls.__name__.endswith(cls.interface_suffix):

                raise TypeError(
                    f"{cls.__name__} must end with "
                    f"'{cls.interface_suffix}'"
                )

        # ---------------------------------------------------------
        # 2. Find abstract methods from parent interfaces
        # ---------------------------------------------------------

        abstract_methods = set()

        for base in cls.__mro__[1:]:
            for name, value in base.__dict__.items():

                if getattr(value, "__isabstractmethod__", False):
                    abstract_methods.add(name)

        # ---------------------------------------------------------
        # 3. Remove methods implemented by the child
        # ---------------------------------------------------------

        for name in list(abstract_methods):

            if name in cls.__dict__:

                value = cls.__dict__[name]

                if not getattr(
                    value,
                    "__isabstractmethod__",
                    False
                ):
                    abstract_methods.remove(name)

        # ---------------------------------------------------------
        # 4. Fail if methods are missing
        # ---------------------------------------------------------

        if abstract_methods:

            raise TypeError(
                f"{cls.__name__} must implement: "
                f"{', '.join(sorted(abstract_methods))}"
            )


# ================================================================
# Gateway Interface
# ================================================================

class Gateway(
    Interface[dict, dict]
):

    interface_suffix = "Gateway"

    @abstractmethod
    def charge(
        self,
        request: dict
    ) -> dict:
        ...

    @abstractmethod
    def refund(
        self,
        request: dict
    ) -> dict:
        ...


# ================================================================
# Valid implementation
# ================================================================

class StripeGateway(Gateway):

    def charge(
        self,
        request: dict
    ) -> dict:

        return {
            "success": True,
            "gateway": "stripe",
            "amount": request["amount"],
        }

    # Below code will encounter runtime error ❌❌❌ cause the methodd has to be implementated. uncomment it

    # def refund(
    #     self,
    #     request: dict
    # ) -> dict:

    #     return {
    #         "success": True,
    #         "gateway": "stripe",
    #         "transaction_id": request["transaction_id"],
    #     }
  

# ================================================================
# Test
# ================================================================

stripe = StripeGateway()

print(
    stripe.charge(
        {
            "amount": 1000
        }
    )
)

print(
    stripe.refund(
        {
            "transaction_id": "txn_123"
        }
    )
)
