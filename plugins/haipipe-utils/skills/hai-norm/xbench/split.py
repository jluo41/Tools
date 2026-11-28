"""
The train/test split. Hash, so it is stable across reruns and stores no seed.

SPLIT ON THE PATIENT, NEVER ON THE ROW. One patient logs the same meal string,
the same walk, the same prescription many times over. A row-level split puts
identical text on both sides and the benchmark grades memorisation instead of
resolution. This is not a food fact; it is true of every noun on the board.
"""
import hashlib

TEST_FRACTION = 0.30


def split_of(patient_id, test_fraction: float = TEST_FRACTION) -> str:
    """PatientID -> "train" | "test". Deterministic, seedless, noun-agnostic."""
    h = hashlib.sha256(str(patient_id).encode()).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < test_fraction * 1000 else "train"
