from test_unstructured.partition.test_constants import EXPECTED_TABLE, EXPECTED_TEXT
from unstructured.cleaners.core import clean_extra_whitespace
from unstructured.documents.elements import Table
from unstructured.partition.tsv import partition_tsv

EXPECTED_FILETYPE = "text/tsv"


def test_partition_tsv_from_filename(filename="example-docs/stanley-cups.tsv"):
    elements = partition_tsv(filename=filename)

    assert clean_extra_whitespace(elements[0].text) == EXPECTED_TEXT
    assert elements[0].metadata.text_as_html == EXPECTED_TABLE
    assert elements[0].metadata.filetype == EXPECTED_FILETYPE
    for element in elements:
        assert element.metadata.filename == "stanley-cups.tsv"


def test_partition_tsv_from_filename_with_metadata_filename(
    filename="example-docs/stanley-cups.tsv",
):
    elements = partition_tsv(filename=filename, metadata_filename="test")

    assert clean_extra_whitespace(elements[0].text) == EXPECTED_TEXT
    for element in elements:
        assert element.metadata.filename == "test"


def test_partition_tsv_from_file(filename="example-docs/stanley-cups.tsv"):
    with open(filename, "rb") as f:
        elements = partition_tsv(file=f)

    assert clean_extra_whitespace(elements[0].text) == EXPECTED_TEXT
    assert isinstance(elements[0], Table)
    assert elements[0].metadata.text_as_html == EXPECTED_TABLE
    assert elements[0].metadata.filetype == EXPECTED_FILETYPE
    for element in elements:
        assert element.metadata.filename is None


def test_partition_tsv_from_file_with_metadata_filename(
    filename="example-docs/stanley-cups.tsv",
):
    with open(filename, "rb") as f:
        elements = partition_tsv(file=f, metadata_filename="test")

    assert clean_extra_whitespace(elements[0].text) == EXPECTED_TEXT
    for element in elements:
        assert element.metadata.filename == "test"


def test_partition_tsv_filename_exclude_metadata(
    filename="example-docs/stanley-cups.tsv",
):
    elements = partition_tsv(filename=filename, include_metadata=False)

    assert clean_extra_whitespace(elements[0].text) == EXPECTED_TEXT
    assert isinstance(elements[0], Table)
    assert elements[0].metadata.text_as_html is None
    assert elements[0].metadata.filetype is None
    for element in elements:
        assert element.metadata.filename is None


def test_partition_tsv_from_file_exclude_metadata(
    filename="example-docs/stanley-cups.tsv",
):
    with open(filename, "rb") as f:
        elements = partition_tsv(file=f, include_metadata=False)

    for i in range(len(elements)):
        assert elements[i].metadata.to_dict() == {}


def test_partition_tsv_metadata_date(
    mocker,
    filename="example-docs/stanley-cups.tsv",
):
    mocked_last_modification_date = "2029-07-05T09:24:28"

    mocker.patch(
        "unstructured.partition.tsv.get_last_modified_date",
        return_value=mocked_last_modification_date,
    )

    elements = partition_tsv(
        filename=filename,
    )

    assert elements[0].metadata.last_modified == mocked_last_modification_date


def test_partition_tsv_with_custom_metadata_date(
    mocker,
    filename="example-docs/stanley-cups.tsv",
):
    mocked_last_modification_date = "2029-07-05T09:24:28"
    expected_last_modification_date = "2020-07-05T09:24:28"

    mocker.patch(
        "unstructured.partition.tsv.get_last_modified_date",
        return_value=mocked_last_modification_date,
    )

    elements = partition_tsv(
        filename=filename,
        metadata_last_modified=expected_last_modification_date,
    )

    assert elements[0].metadata.last_modified == expected_last_modification_date


def test_partition_tsv_from_file_metadata_date(
    mocker,
    filename="example-docs/stanley-cups.tsv",
):
    mocked_last_modification_date = "2029-07-05T09:24:28"

    mocker.patch(
        "unstructured.partition.tsv.get_last_modified_date_from_file",
        return_value=mocked_last_modification_date,
    )

    with open(filename, "rb") as f:
        elements = partition_tsv(
            file=f,
        )

    assert elements[0].metadata.last_modified == mocked_last_modification_date


def test_partition_tsv_from_file_with_custom_metadata_date(
    mocker,
    filename="example-docs/stanley-cups.tsv",
):
    mocked_last_modification_date = "2029-07-05T09:24:28"
    expected_last_modification_date = "2020-07-05T09:24:28"

    mocker.patch(
        "unstructured.partition.tsv.get_last_modified_date_from_file",
        return_value=mocked_last_modification_date,
    )

    with open(filename, "rb") as f:
        elements = partition_tsv(file=f, metadata_last_modified=expected_last_modification_date)

    assert elements[0].metadata.last_modified == expected_last_modification_date
