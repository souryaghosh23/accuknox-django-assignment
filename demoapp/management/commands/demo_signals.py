import threading
import time

from django.core.management.base import BaseCommand
from django.db import connection, transaction, connections

from demoapp.models import Probe
from demoapp.proof_state import state


class Command(BaseCommand):
    help = "Run experiments proving Django signal behavior"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting signal experiments..."))

        self.test_sync_behavior()
        self.test_same_thread_behavior()
        self.test_transaction_behavior()

    def test_sync_behavior(self):
        self.stdout.write("\n=== TEST 1: Sync behavior ===")

        state["caller_thread_id"] = threading.get_ident()
        state["caller_in_atomic"] = connection.in_atomic_block

        start=time.perf_counter()

        Probe.objects.create(label="sync-test")

        elapsed=time.perf_counter()-start

        self.stdout.write(
            f"Time taken for create(): {elapsed:.2f} seconds"
        )

    def test_same_thread_behavior(self):
        self.stdout.write("\n=== TEST 2: Same thread behavior ===")

        state["caller_thread_id"] = threading.get_ident()
        state["caller_in_atomic"] = connection.in_atomic_block

        Probe.objects.create(label="thread-test")

        self.stdout.write(f"caller thread id stored: {state['caller_thread_id']}")
        self.stdout.write("Receiver printed its own thread id.")
        self.stdout.write("If both ids match, the receiver ran in the same thread.")

    def test_transaction_behavior(self):
        self.stdout.write("\n=== TEST 3: Transaction behavior ===")

        with transaction.atomic():
            state["caller_thread_id"] = threading.get_ident()
            state["caller_in_atomic"] = connection.in_atomic_block

            self.stdout.write(f"caller in_atomic_block inside atomic(): {connection.in_atomic_block}")

            obj = Probe.objects.create(label="transaction-test")

            # Register a callback after commit
            transaction.on_commit(
                lambda: self.stdout.write(
                    f"on_commit: observer sees row after commit? "
                    f"{Probe.objects.using('observer').filter(pk=obj.pk).exists()}"
                )
            )

            self.stdout.write(
                f"Inside atomic before commit, observer sees row? "
                f"{Probe.objects.using('observer').filter(pk=obj.pk).exists()}"
            )

        self.stdout.write("Exited atomic block; commit has happened.")