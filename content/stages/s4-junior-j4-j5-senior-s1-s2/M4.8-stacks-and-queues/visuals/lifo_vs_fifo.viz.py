import vizrec as vz

rec = vz.Recorder()
values = rec.stdin.split()

stack = []
queue = []

for v in values:
    stack.append(v)
    queue.append(v)
    rec.step(
        f"Push '{v}' onto the stack and add '{v}' to the back of the queue. "
        f"Stack: {stack}. Queue: {queue}.",
        stack=vz.stack([(x, "done") for x in stack]),
        queue=vz.queue([(x, "done") for x in queue]),
    )

stack_order = []
queue_order = []

while stack:
    popped = stack.pop()
    stack_order.append(popped)
    served = queue.pop(0)
    queue_order.append(served)
    rec.step(
        f"Pop '{popped}' from the top of the stack; serve '{served}' from the front of the queue. "
        f"Stack has given back {stack_order}. Queue has given back {queue_order}.",
        stack=vz.stack([(x, "done") for x in stack]),
        queue=vz.queue([(x, "done") for x in queue]),
    )

rec.output(f"stack: {' '.join(stack_order)}\nqueue: {' '.join(queue_order)}\n")
