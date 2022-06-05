import pathlib

CWD = pathlib.Path.cwd()
TESTS_ROOT = pathlib.Path(__file__).parent
DATA_DIR = TESTS_ROOT / "data"

# relative path strings for all test CSV files
TEST_CSVS = [str(path.relative_to(CWD)) for path in DATA_DIR.glob("*.csv")]
