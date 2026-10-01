import vizrec as vz

rec = vz.Recorder()
period = int(rec.readline())
offset = int(rec.readline())
days = int(rec.readline())

if days <= offset:
    frame = vz.line(0, max(days, 1))
    rec.step(
        f"The full range here is day 0 up to day {days - 1} ({days} days). "
        f"The event's first occurrence is day {offset}, outside that range.",
        line=frame,
    )
    rec.step(
        f"No event lands inside day 0 to day {days - 1}, so the count is 0.",
        line=frame,
    )
    count = 0
else:
    start_frame = vz.line(0, days, points=[(offset, str(offset), "current")])
    rec.step(
        f"The first event is day {offset}. It repeats every {period} days.",
        line=start_frame,
    )

    span = days - offset
    span_frame = vz.line(
        0,
        days,
        points=[(offset, str(offset), "current")],
        intervals=[(offset, days - 1, f"span {span}", "queued", 0)],
    )
    rec.step(
        f"That leaves days {offset} to {days - 1} to check: {days} - {offset} = {span} days.",
        line=span_frame,
    )

    full_cycles = span // period
    cycle_points = [
        (offset + k * period, str(offset + k * period), "done") for k in range(full_cycles)
    ]
    rec.step(
        f"{span} // {period} = {full_cycles} full cycles fit in that span, each with one event: "
        f"day {', day '.join(str(offset + k * period) for k in range(full_cycles))}.",
        line=vz.line(0, days, points=cycle_points),
    )

    remainder = span % period
    if remainder:
        extra_day = offset + full_cycles * period
        rec.step(
            f"The remainder is {span} % {period} = {remainder}, big enough to fit one more event "
            f"on day {extra_day} before the range ends. That is the plus one.",
            line=vz.line(0, days, points=cycle_points + [(extra_day, str(extra_day), "compare")]),
        )
        count = full_cycles + 1
    else:
        rec.step(
            f"The remainder is {span} % {period} = 0, so no partial cycle is left over.",
            line=vz.line(0, days, points=cycle_points),
        )
        count = full_cycles

    rec.step(
        f"{full_cycles} full cycles plus {1 if remainder else 0} from the remainder: "
        f"the event happens {count} {'time' if count == 1 else 'times'} in this range.",
        line=vz.line(0, days, points=cycle_points + ([(extra_day, str(extra_day), "compare")] if remainder else [])),
    )

rec.output(f"{count}\n")
