from pathlib import Path

from run_progress import RunProgress


def main():
    path = Path("./data/case_study.yaml")

    run_progress = RunProgress(path)

    run_progress.main_process()


if __name__ == "__main__":
    main()