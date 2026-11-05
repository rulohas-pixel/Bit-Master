import sys
from array import array


SCALE = 1_000_000


def parse_scaled(token: bytes) -> int:
    """Convierte un decimal con hasta 6 decimales a entero escalado."""
    negative = False
    if token[:1] == b'-':
        negative = True
        token = token[1:]
    elif token[:1] == b'+':
        token = token[1:]

    parts = token.split(b'.', 1)
    whole = int(parts[0]) if parts[0] else 0
    fraction = 0
    if len(parts) == 2 and parts[1]:
        fraction = int(parts[1].ljust(6, b'0'))
    value = whole * SCALE + fraction
    return -value if negative else value


def next_nonempty_line(stream):
    line = stream.readline()
    while line and not line.strip():
        line = stream.readline()
    return line


def solve():
    stream = sys.stdin.buffer
    first = next_nonempty_line(stream)
    if not first:
        return

    t = int(first)
    output = []

    for _ in range(t):
        header = next_nonempty_line(stream).split()
        n = int(header[0])
        k = parse_scaled(header[1])

        tokens = next_nonempty_line(stream).split()

        # Arreglos compactos: reducen considerablemente el uso de memoria.
        values = array('q', [0]) * n
        min_q = array('i', [0]) * n
        max_q = array('i', [0]) * n

        left = 0
        min_head = min_tail = 0
        max_head = max_tail = 0
        best_len = 0
        best_pos = 1

        for right, token in enumerate(tokens):
            if token != b'?':
                value = parse_scaled(token)
                values[right] = value

                while min_tail > min_head and values[min_q[min_tail - 1]] > value:
                    min_tail -= 1
                min_q[min_tail] = right
                min_tail += 1

                while max_tail > max_head and values[max_q[max_tail - 1]] < value:
                    max_tail -= 1
                max_q[max_tail] = right
                max_tail += 1

            while min_head < min_tail and max_head < max_tail:
                if values[max_q[max_head]] - values[min_q[min_head]] <= k:
                    break

                left += 1
                while min_head < min_tail and min_q[min_head] < left:
                    min_head += 1
                while max_head < max_tail and max_q[max_head] < left:
                    max_head += 1

            length = right - left + 1
            if length > best_len:
                best_len = length
                best_pos = left + 1

        output.append(f"{best_len} {best_pos}")

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()
