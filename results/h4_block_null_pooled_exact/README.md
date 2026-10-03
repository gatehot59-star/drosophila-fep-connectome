# Exact pooled distribution

The canonical pooled null distribution is the concatenation of `part-01.b64`, `part-02.b64`, and `part-03.b64`, decoded as little-endian IEEE-754 binary64 values.

```sh
cat part-*.b64 | base64 -d > scores.bin
sha256sum scores.bin
# 74eb80de8891a01660284e26fba0b4c4e3138d632359d0d34c836faf12a8f01f
python3 -S -c 'import struct; raw=open("scores.bin","rb").read(); scores=struct.unpack("<"+"d"*(len(raw)//8),raw); assert len(scores)==999; print(scores[0],scores[-1])'
```

The manifest contains the aggregate statistic and provenance. The f64 payload is exact, not rounded. The earlier human-readable transport shards under `results/h4_block_null_co2_off_8_trials_pooled_distribution.json.part-*` are superseded; use this directory.
