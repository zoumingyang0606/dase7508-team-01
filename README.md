# DASE7508 Spam Filtering Evaluation

This repository import records the defensive evaluation from the revised Enron1 project. A uses word TF-IDF and logistic regression. B adds inference-time normalization before the same word model. C uses character TF-IDF and logistic regression. The shareable materials include a clean-input replay for A and C, the frozen clean counts for A/B/C, pooled results from the supplied paired evaluation, and tests for the two miss-rate formulas.

## Run the checks

On Windows, use Python 3.11 or 3.12 from the project directory.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Get the Enron1 archive from the source in [the data notes](docs/DATA_SOURCE.md). The replay checks the archive fingerprint, retrains both baselines on the original stratified split, and checks their confusion counts against the frozen output.

```powershell
.\.venv\Scripts\python.exe -X utf8 run.py --data 'C:\path\to\enron1.tar.gz'
```

Results are written to `results/clean_reproduced.json`. The full local package and human-rating sheets are retained by the team for course review. This checkout reproduces the clean A/C evaluation. The B row and the paired rows are archived aggregate results from the supplied local package.

## Reading the results

- [Clean results](results/clean_metrics.csv) report three models on the same 952 messages.
- [Pooled paired results](results/pooled_pair_metrics.csv) report statistics pooled across 45 spam-targeted primary conditions per model. The totals count message-condition observations, so the same original can contribute multiple times. Do not interpret them as independent messages or as a mean of equally weighted condition rates.
- Overall variant miss rate is the number of missed variants divided by all spam observations. Conditional bypass is the number newly missed divided by the number originally blocked by that same model.
- [Review status](docs/REVIEW_STATUS.md) records the current state of manual readability and independent teammate review.

The clean and paired evidence comes from the supplied revised Enron1 package. Codex assisted with the original work and this import. Teammates should record actual reproduction and review results on the pull request.
