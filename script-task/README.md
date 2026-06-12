# x264 QP Sweep Benchmark

A Python utility that benchmarks x264 encoding across different QP values and generates an Excel report with encoding time, FPS, and output file size metrics.

## Requirements

- Python 3.10+
- x264 available in PATH

Install dependencies:

```bash
pip install -r requirements.txt
```
## Input

The script expects a `.yuv` input file.
The input path may be absolute or relative to the current working directory.

## Usage

Basic usage:

```bash
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288
```

Custom QP range:

```bash
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288 \
    --qp-start 20 \
    --qp-end 30
```

Custom output directory:

```bash
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288 \
    --output-dir outputs
```

## Arguments

- `--input` — path to the input `.yuv` file (**required**)
- `--resolution` — input resolution in `WIDTHxHEIGHT` format (**required**)
- `--qp-start` — starting QP value (default: `1`)
- `--qp-end` — ending QP value (default: `51`)
- `--output-dir` — output directory for encoded files (default: `outputs`)
## Output

The script generates:

- Encoded bitstreams in the output directory
- An Excel report (`report.xlsx`)

The report contains:

- Encoded filename
- QP
- Encoding time (s)
- FPS
- Encoded file size (bytes)