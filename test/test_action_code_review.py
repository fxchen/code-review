from action_code_review import extract_filenames_from_diff

def test_extract_filenames_from_diff():
    diff_text = """
    diff --git a/file1.txt b/file1.txt
    index 7c4658f..5a5d634 100644
    --- a/file1.txt
    +++ b/file1.txt
    @@ -1 +1 @@
    -Old line
    +New line
    """
    assert extract_filenames_from_diff(diff_text) == ['file1.txt']

    diff_text = """
    diff --git a/file1.txt b/file1.txt
    index 7c4658f..5a5d634 100644
    --- a/file1.txt
    +++ b/file1.txt
    @@ -1 +1 @@
    -Old line
    +New line
    diff --git a/file2.txt b/file2.txt
    index 6dcd4cf..7c4658f 100644
    --- a/file2.txt
    +++ b/file2.txt
    @@ -1 +1 @@
    -Another old line
    +Another new line
    """
    assert extract_filenames_from_diff(diff_text) == ['file1.txt', 'file2.txt']

    # Test with empty input
    diff_text = ""
    assert extract_filenames_from_diff(diff_text) == []

test_extract_filenames_from_diff()
