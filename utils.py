#!/usr/bin python

def get_fields(line):
    fields = dict()
    segs = line.strip().split('|#|')
    for seg in segs:
        key, value = seg.split(':', 1)
        fields[key] = value
    return fields
