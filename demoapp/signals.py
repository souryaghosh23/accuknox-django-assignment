import threading
import time
from django.db import connection, connections
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Probe
from .proof_state import state

@receiver(post_save, sender=Probe, weak=False)
def probe_post_save(sender, instance, created, **kwargs):
    print("\n--- SIGNAL RECEIVER START ---")
    print("receiver thread id:", threading.get_ident())
    print("caller thread id   :", state["caller_thread_id"])
    print("same thread?       :", threading.get_ident() == state["caller_thread_id"])

    print("receiver in_atomic_block:", connection.in_atomic_block)
    print("caller   in_atomic_block:", state["caller_in_atomic"])

    if instance.label == "sync-test":
        print("sleeping 2 seconds inside receiver...")
        time.sleep(2)

    try:
        exists_before_commit = Probe.objects.using("observer").filter(pk=instance.pk).exists()
        print("observer sees row before commit?:", exists_before_commit)
    except Exception as e:
        print("observer check failed:", repr(e))

    print("--- SIGNAL RECEIVER END ---\n")