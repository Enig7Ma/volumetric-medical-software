"""Static tag definitions used by the Streamlit UI.

Tags are split into imaging modality tags and other medical categories.
"""

IMAGING_TAGS = [
    "CT",
    "MRI",
    "Ultrasound",
    "X-ray",
]

OTHER_TAGS = [
    "Cardiology",
    "Dermatology",
    "Emergency",
    "Neurology",
    "Pathology",
    "Pediatrics",
]

TAGS = [*IMAGING_TAGS, *OTHER_TAGS]
