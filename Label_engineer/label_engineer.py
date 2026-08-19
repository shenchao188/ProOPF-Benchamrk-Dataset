#!/usr/bin/env python3
"""Run benchmark ground-truth MATLAB code and write objective-value labels.

Examples
--------
python Label_engineer/label_engineer.py \
    --input ProOPF_B/level1_with_labels.jsonl \
    --output /tmp/level1_labeled.jsonl \
    --case-dir base_system

For Level 2/4 files, both strategy values are evaluated automatically.  Use
``--in-place`` only after checking the generated output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


def matlab_number(value: Any) -> str:
    """Format a JSON scalar as a MATLAB scalar literal."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    raise TypeError(f"MATLAB parameter must be numeric, got {value!r}")


def function_signature(code: str) -> Tuple[str, List[str]]:
    """Return MATLAB function name and input argument names."""
    pattern = re.compile(
        r"^\s*function\s+(?:\[[^]]+\]|[A-Za-z_]\w*)\s*=\s*"
        r"([A-Za-z_]\w*)\s*(?:\(([^)]*)\))?",
        re.MULTILINE,
    )
    match = pattern.search(code)
    if not match:
        raise ValueError("matpower_code does not contain a supported MATLAB function signature")
    args = [item.strip() for item in (match.group(2) or "").split(",") if item.strip()]
    return match.group(1), args


def parameter_specs(
    sample: Dict[str, Any], strategy: int
) -> Dict[str, Tuple[Any, Dict[str, Any]]]:
    """Build function-argument specs, including direction-only parameters."""
    result: Dict[str, Tuple[Any, Dict[str, Any]]] = {}
    value_key = f"parameter_value_strategy{strategy}"
    for modification in sample.get("model_specification", {}).get("parameter_modifications", []):
        component = modification["component"]
        target = modification["target_parameter"]
        if component in ("bus", "gen"):
            name = f"{component}_{target}_{modification['bus_id']}"
        elif component == "branch":
            name = (
                f"branch_{target}_{modification['fbus']}_{modification['tbus']}"
            )
        else:
            raise ValueError(f"Unsupported parameter component: {component}")
        result[name] = (modification.get(value_key), modification)
    return result


def expected_parameter_names(sample: Dict[str, Any], strategy: int) -> Dict[str, Any]:
    """Backward-compatible name/value view of :func:`parameter_specs`."""
    return {name: spec[0] for name, spec in parameter_specs(sample, strategy).items()}


def matlab_scalar(engine: Any, expression: str) -> Any:
    """Evaluate a scalar expression while tolerating MATLAB logical values."""
    return engine.eval(expression, nargout=1)


class LabelEngineer:
    def __init__(self, case_dir: Path, verbose: bool = True):
        try:
            import matlab.engine  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "MATLAB Python Engine is not installed. Install it from "
                "<MATLAB>/extern/engines/python before running this script."
            ) from exc

        self.case_dir = case_dir.resolve()
        self.verbose = verbose
        self.engine = matlab.engine.start_matlab("-nodesktop -nosplash")
        self.engine.addpath(str(self.case_dir), nargout=0)

    def close(self) -> None:
        if self.engine is not None:
            self.engine.quit()
            self.engine = None

    def _read_results(self) -> Tuple[float, bool]:
        objective = float(matlab_scalar(self.engine, "results.f"))
        # runopf uses success in some custom Level 3/4 formulations and
        # converged in standard MATPOWER output.
        converged = True
        try:
            converged = bool(matlab_scalar(self.engine, "results.success"))
        except Exception:
            try:
                converged = bool(matlab_scalar(self.engine, "results.converged"))
            except Exception:
                pass
        return objective, converged

    def _run_file(self, directory: Path, stem: str) -> Tuple[float, bool]:
        self.engine.addpath(str(directory), nargout=0)
        self.engine.eval(f"clear results; {stem};", nargout=0)
        return self._read_results()

    def run_script(self, code: str, sample_id: int) -> Tuple[float, bool]:
        with tempfile.TemporaryDirectory(prefix=f"opf_label_{sample_id}_") as tmp:
            directory = Path(tmp)
            stem = f"label_script_{sample_id}"
            (directory / f"{stem}.m").write_text(code, encoding="utf-8")
            return self._run_file(directory, stem)

    def run_function(
        self, code: str, sample: Dict[str, Any], strategy: int, sample_id: int
    ) -> Tuple[float, bool]:
        function_name, arguments = function_signature(code)
        specs = parameter_specs(sample, strategy)
        unknown = [name for name in arguments if name not in specs]
        missing = [name for name in specs if name not in arguments]
        if unknown or missing:
            raise ValueError(
                f"Function parameter mismatch (unknown={unknown}, missing={missing})"
            )

        with tempfile.TemporaryDirectory(prefix=f"opf_label_{sample_id}_s{strategy}_") as tmp:
            directory = Path(tmp)
            (directory / f"{function_name}.m").write_text(code, encoding="utf-8")
            driver = f"label_driver_{sample_id}_s{strategy}"
            assignments = [
                self._driver_assignment(name, specs[name][0], specs[name][1], sample, i)
                for i, name in enumerate(arguments, 1)
            ]
            call = ", ".join(arguments)
            driver_code = (
                "define_constants;\n"
                f"mpc = loadcase('{sample['model_specification']['base_system']}');\n"
                + "\n".join(assignments)
                + f"\nclear results; results = {function_name}({call});\n"
            )
            (directory / f"{driver}.m").write_text(driver_code, encoding="utf-8")
            return self._run_file(directory, driver)

    @staticmethod
    def _driver_assignment(
        name: str,
        value: Any,
        modification: Dict[str, Any],
        sample: Dict[str, Any],
        index: int,
    ) -> str:
        if value is not None:
            return f"{name} = {matlab_number(value)};"

        direction = modification.get("direction", "").lower()
        if direction == "increase":
            factor = "1.1"
        elif direction == "decrease":
            factor = "0.9"
        elif direction == "set zero":
            return f"{name} = 0;"
        else:
            raise ValueError(
                f"No strategy value or supported direction for {name}: {direction!r}"
            )

        component = modification["component"]
        target = modification["target_parameter"]
        idx = f"label_idx_{index}"
        if component == "bus":
            selector = f"find(mpc.bus(:, BUS_I) == {modification['bus_id']})"
            expression = f"mpc.bus({idx}, {target}) * {factor}"
            return f"{idx} = {selector}; {name} = {expression};"
        if component == "gen":
            selector = f"find(mpc.gen(:, GEN_BUS) == {modification['bus_id']})"
            expression = f"mpc.gen({idx}, {target}) * {factor}"
            return f"{idx} = {selector}; {name} = {expression};"
        if component == "branch":
            fbus, tbus = modification["fbus"], modification["tbus"]
            selector = (
                f"find((mpc.branch(:, F_BUS) == {fbus} & "
                f"mpc.branch(:, T_BUS) == {tbus}) | "
                f"(mpc.branch(:, F_BUS) == {tbus} & "
                f"mpc.branch(:, T_BUS) == {fbus}))"
            )
            expression = f"mpc.branch({idx}, {target}) * {factor}"
            return f"{idx} = {selector}; {name} = {expression};"
        raise ValueError(f"Unsupported component: {component}")

    def label_sample(self, sample: Dict[str, Any], sample_id: int) -> Dict[str, Any]:
        code = sample.get("matpower_code")
        if not code:
            raise ValueError("sample has no matpower_code")
        started = time.perf_counter()
        is_function = "results_strategy1" in sample or "results_strategy2" in sample
        if is_function:
            for strategy in (1, 2):
                key = f"results_strategy{strategy}"
                if key not in sample:
                    continue
                objective, converged = self.run_function(
                    code, sample, strategy, sample_id
                )
                sample[key]["objective_value"] = objective
                sample[key]["converged"] = converged
                sample[key]["execution_time"] = time.perf_counter() - started
                sample[key]["error_message"] = None
        else:
            objective, converged = self.run_script(code, sample_id)
            result = sample.setdefault("results", {})
            result["objective_value"] = objective
            result["converged"] = converged
            result["execution_time"] = time.perf_counter() - started
            result["error_message"] = None
        return sample


def iter_samples(path: Path, start: int | None, end: int | None) -> Iterable[Tuple[int, Dict[str, Any]]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if start is not None and line_number < start:
                continue
            if end is not None and line_number > end:
                break
            if line.strip():
                yield line_number, json.loads(line)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input JSONL file")
    parser.add_argument("--output", type=Path, help="Output JSONL file")
    parser.add_argument("--case-dir", type=Path, default=Path("base_system"))
    parser.add_argument("--start", type=int, help="1-based first line to label")
    parser.add_argument("--end", type=int, help="1-based last line to label")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input file")
    parser.add_argument("--stop-on-error", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.in_place and args.output:
        parser.error("--in-place and --output cannot be used together")
    if not args.in_place and not args.output:
        args.output = args.input.with_name(args.input.stem + "_labeled.jsonl")
    return args


def main() -> int:
    args = parse_args()
    output = args.input if args.in_place else args.output
    assert output is not None
    output.parent.mkdir(parents=True, exist_ok=True)
    engineer = LabelEngineer(args.case_dir, verbose=not args.quiet)
    try:
        selected = {
            line_number: sample
            for line_number, sample in iter_samples(args.input, args.start, args.end)
        }
        # Preserve every input line and only replace selected records.
        original_lines = args.input.read_text(encoding="utf-8").splitlines()
        labeled = 0
        errors = 0
        for line_number, sample in selected.items():
            try:
                selected[line_number] = engineer.label_sample(sample, line_number)
                labeled += 1
                if not args.quiet:
                    print(f"[OK] line {line_number}")
            except Exception as exc:  # keep a machine-readable failure in the label
                errors += 1
                message = str(exc)
                if "results_strategy1" in sample or "results_strategy2" in sample:
                    for key in ("results_strategy1", "results_strategy2"):
                        if key in sample:
                            sample[key]["error_message"] = message
                            sample[key]["converged"] = False
                            sample[key]["objective_value"] = None
                else:
                    result = sample.setdefault("results", {})
                    result["error_message"] = message
                    result["converged"] = False
                    result["objective_value"] = None
                selected[line_number] = sample
                print(f"[ERROR] line {line_number}: {message}")
                if args.stop_on_error:
                    raise

        output_lines = []
        for line_number, line in enumerate(original_lines, 1):
            output_lines.append(
                json.dumps(selected[line_number], ensure_ascii=False)
                if line_number in selected
                else line
            )
        output.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
        print(f"Labeled {labeled} samples; {errors} errors; output: {output}")
        return 1 if errors else 0
    finally:
        engineer.close()


if __name__ == "__main__":
    raise SystemExit(main())
