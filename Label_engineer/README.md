# Label engineer

This tool executes the MATLAB code stored in benchmark JSONL files and updates
the objective-value labels. It requires MATLAB, MATPOWER, and the MATLAB
Python Engine.

Run a single sample first:

```bash
python3 Label_engineer/label_engineer.py \
  --input ProOPF_B/level1_with_labels.jsonl \
  --output /tmp/level1_labeled.jsonl \
  --case-dir base_system \
  --start 1 --end 1
```

Level 1 and Level 3 scripts are executed directly. Level 2 and Level 4
functions are called twice, using `parameter_value_strategy1` and
`parameter_value_strategy2`; both result objects are updated.

For direction-only parameters that do not provide an explicit strategy value,
the driver derives a deterministic value from the loaded case: Increase uses
`1.1 * current`, Decrease uses `0.9 * current`, and Set zero uses `0`.

The source file is not overwritten unless `--in-place` is supplied. MATLAB
errors are stored in `error_message`, and the process continues to the next
sample unless `--stop-on-error` is used.
