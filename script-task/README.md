x264 QP Sweep Benchmark Tool

A simple Python utility for benchmarking x264 encoding performance across a range of QP (Quantization Parameter) values.

The script:

Encodes a raw YUV file multiple times using x264
Sweeps through a range of QP values
Measures encoding time and FPS
Records output file sizes
Exports all results to an Excel report (report.xlsx)
Requirements
Software
Python 3.10+
x264 installed and available in PATH

Verify x264 installation:

x264 --version
Python Packages

Install dependencies:

pip install -r requirements.txt
Input Format

The script expects a raw YUV420p input file.

Example:

foreman-cif.yuv

Because raw YUV files do not contain metadata, the input resolution must be provided explicitly.

Usage
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288
Custom QP Range
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288 \
    --qp-start 20 \
    --qp-end 30
Custom Output Directory
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288 \
    --output-dir outputs
Command-Line Arguments
Argument	Required	Default	Description
--input	Yes	-	Path to input .yuv file
--resolution	Yes	-	Input resolution in WIDTHxHEIGHT format
--qp-start	No	1	Starting QP value
--qp-end	No	51	Ending QP value
--output-dir	No	outputs	Directory for encoded bitstreams
Output
Encoded Files

For each QP value, the script generates:

outputs/
├── output_qp_1.264
├── output_qp_2.264
├── output_qp_3.264
...
└── output_qp_51.264
Excel Report

After all encodes complete, the script generates:

report.xlsx

The report contains the following columns:

Encoded filename	QP	Time (s)	FPS	Encoded file size (bytes)
output_qp_1.264	1	12.345	48.7	12345678
output_qp_2.264	2	11.921	50.4	11876543
...	...	...	...	...
How FPS Is Calculated

The script estimates the number of frames from the input file size:

frame_count = file_size / frame_size

For YUV420p input:

frame_size = width × height × 1.5

Encoding FPS is then calculated as:

FPS = total_frames / encoding_time
Example
python3 run_analysis.py \
    --input foreman-cif.yuv \
    --resolution 352x288 \
    --qp-start 22 \
    --qp-end 37 \
    --output-dir results

This will:

Encode the sequence for QP values 22 through 37
Save encoded bitstreams to results/
Measure encoding performance
Generate report.xlsx
Notes
The script assumes the input is YUV420p.
Encoding time includes the complete x264 execution time.
Existing output files with the same names will be overwritten.
Larger QP values generally produce smaller output files and faster encoding.