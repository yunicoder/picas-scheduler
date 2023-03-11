from pathlib import Path

from run_progress import RunProgress


def main():
    input_path = Path("./data/case_study.yaml")
    output_dir = Path("./data/output/")

    run_progress = RunProgress(input_path, output_dir)

    run_progress.main_process()


if __name__ == "__main__":
    main()