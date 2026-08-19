# OOD evaluation case files

The cross-system Level 1 OOD benchmark calls the following MATPOWER case
files directly with `loadcase()`. They are included under `base_system/` so
that this evaluation can be reproduced without relying on a particular
MATPOWER distribution.

| Case | File | SHA-256 |
| --- | --- | --- |
| Australian 59-bus system | `base_system/case59.m` | `a12a1dbc9ade6b31000a47f00f99550015e6fcf773e7689fbb4d4090ef59799c` |
| IEEE 68-bus system | `base_system/case68.m` | `a0993ed620aa9529338658447d6ac7e68ea815f43eb0e89c23e004fb8fd612a5` |
| Iceland 189-bus system | `base_system/case189.m` | `abda97f21cc645cc638d01ba3f95bb29b25c8a8ef433a206a2dcbd028fb2ef1d` |

## Provenance and preprocessing

- **case59** is based on the IEEE PES Technical Report 18 Australian
  14-generator system. Its file header identifies the input as
  `LF_Case01_R4_S.raw` from `AU14GenModelData_Ver04.zip` and documents the
  conversion assumptions.
- **case68** was converted with MATPOWER 6.0's `cdf2mpc` on 2020-06-15 from
  the PSAT archive file `d_IEEE68bus.cf`. The conversion warnings and source
  details are retained in the case-file header.
- **case189** is the Iceland network received from Paddy McNab (Durham
  University) on 2011-01-21. It originated in PSAT format and was converted
  to MATPOWER format; the source and conversion notes are retained in the
  case-file header.

ProOPF applies no preprocessing to these files. Each benchmark sample loads
the named case directly and applies only the parameter modifications recorded
in that sample's JSONL record.

`case189.m` deliberately exposes its primary function as `case189`, matching
the filename and the benchmark's `loadcase('case189')` calls.
