# Base-system MATPOWER cases

This directory contains the exact MATPOWER case files used by ProOPF. Benchmark
records load these files directly with `loadcase()`, then apply only the
modifications recorded in their JSONL entries. No additional ProOPF
preprocessing is applied.

| Case | Source / conversion notes | SHA-256 |
| --- | --- | --- |
| `case14.m` | IEEE 14-bus case; converted from IEEE Common Data Format by `cdf2matp` (2014-10-15). | `2ffc4e1b734ae6c5e92dbe68b4e36010ed695a4bbcc4d065c74c4fbc39fcf3c1` |
| `case30.m` | MATPOWER 30-bus case based on Alsac & Stott (1974), with the modifications documented in its header. | `3d9030311259b553be85d02336b7e1bcb24ec04775bee6671bdb62d18e4e2137` |
| `case39.m` | MATPOWER New England 39-bus case; source and modifications are documented in its header. | `440833f998d1d8768c620477dacb6afd4e03f25f394bb0d200524513ad3fdc3c` |
| `case57.m` | IEEE 57-bus case; converted from IEEE Common Data Format by `cdf2matp` (2014-10-15). | `2218325a6e8fe6c7b8b28202f523670459268075a6fd41b4959d66f17d47d28b` |
| `case59.m` | Australian 14-generator system, based on `LF_Case01_R4_S.raw` from `AU14GenModelData_Ver04.zip`; see the header for conversion assumptions. | `a12a1dbc9ade6b31000a47f00f99550015e6fcf773e7689fbb4d4090ef59799c` |
| `case68.m` | IEEE 68-bus PSAT archive case; converted using MATPOWER 6.0 `cdf2mpc` on 2020-06-15 from `d_IEEE68bus.cf`. | `a0993ed620aa9529338658447d6ac7e68ea815f43eb0e89c23e004fb8fd612a5` |
| `case189.m` | Iceland 189-bus network received from Paddy McNab (2011-01-21), converted from PSAT to MATPOWER; see the header for assumptions. | `abda97f21cc645cc638d01ba3f95bb29b25c8a8ef433a206a2dcbd028fb2ef1d` |
| `case300.m` | IEEE 300-bus case converted from IEEE Common Data Format; see the header for the 2025 transformer-tap modification. | `69a90280e999ef533d94656e0fbc08311f1347c962dd2753ff2005ff5e3f9ac5` |

Please retain the provenance information in each case-file header and comply
with the applicable upstream data and software terms when redistributing or
using these cases.
