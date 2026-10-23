def update_extensions(filenames):
    """Change only a final .doc extension to .pdf."""
    return [
        name[:-4] + ".pdf" if name.endswith(".doc") else name
        for name in filenames
    ]


test_cases = [
    ["annual_report.doc"],
    ["document.doc"],
    ["doctor_visit.doc", "doc_holiday.doc"],
]
expected_outputs = [
    ["annual_report.pdf"],
    ["document.pdf"],
    ["doctor_visit.pdf", "doc_holiday.pdf"],
]

for filenames, expected in zip(test_cases, expected_outputs):
    result = update_extensions(filenames)
    print(f"{filenames} -> {result}")
    assert result == expected

assert update_extensions(["draft.doc.backup"]) == ["draft.doc.backup"]