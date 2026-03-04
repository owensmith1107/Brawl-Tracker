from ingestion.api_client import format_tag

def test_format_tag_removes_hash():
    assert format_tag("#GQCP0YJ") == "GQCP0YJ"

def test_format_tag_handles_no_hash():
    assert format_tag("GQCP0YJ") == "GQCP0YJ"

def test_format_tag_strips_whitespace():
    assert format_tag("  #GQCP0YJ  ") == "GQCP0YJ"