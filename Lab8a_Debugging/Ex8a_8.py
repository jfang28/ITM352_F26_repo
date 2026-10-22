def ai_update_extensions(filenames):
    """Original AI solution."""
    return [name.replace(".doc", ".pdf") for name in filenames]


def update_extensions(filenames):
    """Change a final .doc extension to .pdf."""
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
    original_result = ai_update_extensions(filenames)
    fixed_result = update_extensions(filenames)
    print(f"{filenames} -> original: {original_result}; fixed: {fixed_result}")
    assert original_result == expected
    assert fixed_result == expected

# .replace() changes every matching ".doc" substring, not only the final extension.
# However, it does not fail on the three test cases above: ".doc" only occurs
# as their extension. For example, it changes "notes.doc.backup" unexpectedly.
assert ai_update_extensions(["notes.doc.backup"]) == ["notes.pdf.backup"]
assert update_extensions(["notes.doc.backup"]) == ["notes.doc.backup"]


# Targeted prompt:
# "Update this function so it changes only a filename's final, lowercase .doc
# extension to .pdf. Leave any filename without that final extension unchanged.
# Verify it with the three test cases above, including document.doc and
# doctor_visit.doc, and explain whether the original code actually fails them."