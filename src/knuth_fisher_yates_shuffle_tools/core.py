"""Core implementation of the Fisher-Yates shuffle."""

from typing import MutableSequence, TypeVar, Callable, Optional
import random

T = TypeVar('T')


def shuffle(
    seq: MutableSequence[T],
    rand: Optional[Callable[[int], int]] = None,
) -> None:
    """Shuffle the mutable sequence *seq* in place using the Fisher-Yates algorithm.

    The algorithm iterates from the last index down to 1, selecting a random
    index ``j`` in ``[0, i]`` and swapping ``seq[i]`` with ``seq[j]``.  This
    yields each permutation with equal probability, provided the random source
    is uniform.

    Parameters
    ----------
    seq : MutableSequence
        The sequence to shuffle.  It must support ``len()``, indexing, and
        assignment to indices.
    rand : callable, optional
        A function that takes a single integer ``n`` and returns an integer in
        the half-open interval ``[0, n)``.  If omitted, ``random.randrange`` is
        used.  Supplying a custom source makes the shuffle deterministic and
        testable.

    Raises
    ------
    TypeError
        If *seq* is not a mutable sequence (e.g., a tuple or string).
    ValueError
        If *rand* returns an index outside ``[0, n)``.
    """
    if rand is None:
        rand = random.randrange

    # Check mutability early so we fail before making partial changes.
    if not hasattr(seq, '__setitem__'):
        raise TypeError(
            f"shuffle requires a mutable sequence, got {type(seq).__name__}"
        )

    n = len(seq)
    for i in range(n - 1, 0, -1):
        j = rand(i + 1)
        if not (0 <= j <= i):
            raise ValueError(
                f"random source returned {j}, expected an integer in [0, {i}]"
            )
        seq[i], seq[j] = seq[j], seq[i]
