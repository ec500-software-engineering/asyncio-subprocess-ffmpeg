#!/usr/bin/env python3
"""
~ 4x speedup over ffprobe_sync
"""
import time
from argparse import ArgumentParser

import asyncioffmpeg.ffprobe as probe
from asyncioffmpeg.runner import runner


if __name__ == "__main__":
    p = ArgumentParser(description="Get media metadata asynchronously with FFprobe")
    p.add_argument("path", help="directory where media files are kept")
    p.add_argument(
        "-suffix", help="file suffixes of desired media file types", nargs="+",
    )
    P = p.parse_args()

    tic = time.monotonic()
    # %% emits results as each future is completed
    runner(probe.get_meta, P.path, P.suffix)
    print(f"ffprobe asyncio.as_completed: {time.monotonic() - tic:.3f} seconds")

    # %% approximately same wallclock time, but only gives results when all futures complete
    tic = time.monotonic()
    runner(probe.get_meta_gather, P.path, P.suffix)
    print(f"ffprobe asyncio.gather: {time.monotonic() - tic:.3f} seconds")
