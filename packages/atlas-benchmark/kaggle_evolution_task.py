"""Separate public development task; never overwrites the v0.1 leaderboard."""
import json
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import kaggle_benchmarks as kbench
from evolution import evaluate
from pilot import parse_response

@kbench.task(name='Atlas evidence evolution v0.2')
def atlas_evolution(llm) -> float:
    """Twelve public stage decisions; context-isolated cases; no frontier claim."""
    result=evaluate(llm.prompt,kbench.chats.new,parse_response,repetitions=1)
    try:
        result['sdk_version']=version('kaggle-benchmarks')
    except PackageNotFoundError:
        result['sdk_version']=None
    result['model_identity']='See Kaggle task run metadata; no guessed model identifier'
    result['adapter_policy']='one run, fixed public corpus, no automatic provider retry'
    path=Path('atlas-evolution-v0.2-results.json')
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ('stage_count','completed_count','failed_count','pass_rate','mean_brier_completed_only')},indent=2))
    return float(result['pass_rate'])

# Run explicitly in the separate task notebook:
# atlas_evolution.run(llm=kbench.llm)
