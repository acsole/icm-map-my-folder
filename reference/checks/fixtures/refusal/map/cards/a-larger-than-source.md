# 01 · The Sentinel (broken: larger than its source)

**Type + State:** MARKER · LIVE — fixture; this card exists to fail gate A.
**What it is:** a two-line file whose second line the machinery reads. The card is longer than the
file it describes, which means it restates instead of pointing — the reader would have been better
off opening the file.
**Why it is shaped that way:** it is not; it is broken on purpose.
**Source path:** `small.txt`
**Hits:** whatever branches on it, at read time.
**Does not hit:** the pricing framework, which never reads this value.
**Done when:** you have opened `small.txt` instead of this card. Stop there.
