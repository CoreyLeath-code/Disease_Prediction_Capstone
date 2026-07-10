"""Latency guardrails for the educational orchestration workflow."""

from __future__ import annotations

import math


class DiagnosticDeadlineException(RuntimeError):
    """Raised when the configured demonstration latency budget is exceeded."""


class DiagnosticCircuitBreaker:
    """Track a bounded latency budget without claiming clinical guarantees.

    This guard is a software-resilience demonstration. It is not a medical-device
    safety mechanism and must not be used to make clinical decisions.
    """

    def __init__(self, hard_deadline_ms: float = 50.0) -> None:
        if not math.isfinite(hard_deadline_ms) or hard_deadline_ms <= 0.0:
            raise ValueError("hard_deadline_ms must be a finite positive number.")
        self.hard_deadline_ms = float(hard_deadline_ms)
        self.breaker_status = "CLOSED"

    def evaluate_execution_timing(self, elapsed_ms: float) -> None:
        """Open the demonstration breaker when execution exceeds the budget."""

        if not math.isfinite(elapsed_ms) or elapsed_ms < 0.0:
            raise ValueError("elapsed_ms must be a finite non-negative number.")

        if elapsed_ms > self.hard_deadline_ms:
            self.breaker_status = "OPEN"
            raise DiagnosticDeadlineException(
                "Demonstration latency budget exceeded: "
                f"{elapsed_ms:.2f} ms > {self.hard_deadline_ms:.2f} ms."
            )

    def reset(self) -> None:
        """Close the breaker for the next independent request."""

        self.breaker_status = "CLOSED"
