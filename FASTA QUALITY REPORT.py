
from pathlib import Path
import csv

# Find the FASTA file in the same folder
folder = Path(__file__).resolve().parent
fasta_file = folder / "sample_data.fasta"

if not fasta_file.exists():
    print("ERROR: FASTA file not found.")
    print("Expected location:", fasta_file)

else:
    sequences = []
    sequence_name = ""
    dna_parts = []

    # Read FASTA sequences
    with open(fasta_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if sequence_name:
                    sequences.append(
                        (sequence_name, "".join(dna_parts))
                    )

                sequence_name = line[1:].strip()
                dna_parts = []

            else:
                dna_parts.append(line.upper())

        if sequence_name:
            sequences.append(
                (sequence_name, "".join(dna_parts))
            )

    report = []
    valid_bases = set("ATGC")

    print("\nFASTA QUALITY CONTROL REPORT")
    print("=" * 40)

    for name, dna in sequences:
        length = len(dna)
        invalid_bases = sorted(set(dna) - valid_bases)

        if length > 0:
            gc_percent = (
                (dna.count("G") + dna.count("C")) / length
            ) * 100
        else:
            gc_percent = 0.0

        if length == 0:
            status = "INVALID - Empty sequence"
        elif invalid_bases:
            status = "INVALID - Unexpected characters"
        else:
            status = "VALID"

        print(f"\nSequence: {name}")
        print(f"DNA: {dna}")
        print(f"Length: {length}")
        print(f"GC Content: {gc_percent:.2f}%")
        print(f"Status: {status}")

        if invalid_bases:
            print("Unexpected characters:", ", ".join(invalid_bases))

        report.append({
            "Sequence_Name": name,
            "Length": length,
            "GC_Percent": round(gc_percent, 2),
            "Invalid_Characters": ", ".join(invalid_bases),
            "Status": status
        })

    # Save the report as a CSV file
    output_file = folder / "sequence_report.csv"

    columns = [
        "Sequence_Name",
        "Length",
        "GC_Percent",
        "Invalid_Characters",
        "Status"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(report)

    print("\n" + "=" * 40)
    print("Total sequences:", len(sequences))
    print("CSV report saved:", output_file)
