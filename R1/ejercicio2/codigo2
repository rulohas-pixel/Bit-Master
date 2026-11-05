import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    first = input().strip()
    if not first:
        return

    q = int(first)
    # id -> [priority, original_arrival_order, version]
    pending = {}
    heap = []
    arrival = 0
    output = []

    for _ in range(q):
        parts = input().split()
        if not parts:
            continue

        op = parts[0]

        if op == b'ADD':
            job_id = int(parts[1])
            priority = int(parts[2])
            arrival += 1
            version = 0
            pending[job_id] = [priority, arrival, version]
            heapq.heappush(heap, (-priority, arrival, job_id, version))

        elif op == b'BOOST':
            job_id = int(parts[1])
            increment = int(parts[2])
            job = pending.get(job_id)

            if job is None:
                output.append("NO")
            else:
                job[0] += increment
                job[2] += 1
                # Candidate policy: BOOST changes priority but preserves
                # the job's original ADD order for priority ties.
                heapq.heappush(
                    heap, (-job[0], job[1], job_id, job[2])
                )
                output.append("OK")

        elif op == b'CANCEL':
            job_id = int(parts[1])
            if job_id in pending:
                del pending[job_id]
                output.append("OK")
            else:
                output.append("NO")

        elif op == b'PRINT':
            k = int(parts[1])
            printed = []

            while heap and len(printed) < k:
                neg_priority, order, job_id, version = heapq.heappop(heap)
                job = pending.get(job_id)

                # Discard entries made obsolete by BOOST or CANCEL.
                if job is None:
                    continue
                if job[2] != version or job[0] != -neg_priority:
                    continue

                del pending[job_id]
                printed.append(str(job_id))

            output.append(" ".join(printed) if printed else "VACIA")

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()
