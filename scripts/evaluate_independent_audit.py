"""Compare pre-recorded labels against full, hash-verified live descriptions."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from france_tech_jobs.connectors import _json, _plain, _employment
from france_tech_jobs.classify import classify
from evaluate_holdout import select


def main():
    frame = json.loads((ROOT / 'evaluation/independent_audit_frame.json').read_text(encoding='utf8'))
    labels = json.loads((ROOT / 'evaluation/independent_audit_queue.json').read_text(encoding='utf8'))
    keys = lambda rows: {(r['source_id'], r['job_id']) for r in rows}
    if len(keys(labels)) != len(labels) or keys(select(frame)) != keys(labels):
        raise ValueError('Selection differs from frozen labels')
    results = []
    for row in labels:
        if row['expected_disposition'] not in ('publish', 'review', 'exclude'):
            raise ValueError('Incomplete independent review')
        detail = _json(f"https://api.smartrecruiters.com/v1/companies/{row['board']}/postings/{row['job_id']}", 20)
        digest = hashlib.sha256(json.dumps(detail, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if digest != row['detail_sha256']:
            raise ValueError(f"Posting changed: {row['source_id']}/{row['job_id']}; do not reuse the label silently")
        description = ' '.join(_plain(s.get('text')) for s in (detail.get('jobAd') or {}).get('sections', {}).values() if isinstance(s, dict)).strip()
        contract, _ = _employment(detail.get('typeOfEmployment'))
        for custom in detail.get('customField') or []:
            if str(custom.get('fieldLabel', '')).lower() in ('contract type', 'type de contrat'):
                contract = _employment(custom.get('valueLabel'))[0] or contract
        location = detail.get('location') or {}
        location = location.get('fullLocation') or ', '.join(str(location.get(k) or '') for k in ('city','region','country') if location.get(k))
        predicted = classify(detail['name'], description, location, contract)
        disposition = 'publish' if predicted['eligible'] else 'exclude' if predicted['seniority']=='excluded' or not predicted['categories'] else 'review'
        results.append({'source_id': row['source_id'], 'job_id': row['job_id'], 'detail_sha256': digest,
                        'expected': row['expected_disposition'], 'observed': disposition,
                        'expected_categories': row['expected_categories'], 'observed_categories': predicted['categories']})
        time.sleep(.2)
    output = {'review_provenance': 'Single assistant qualitative reviewer; labels frozen before predictions',
              'classifier_sha256': hashlib.sha256((ROOT / 'src/france_tech_jobs/classify.py').read_bytes()).hexdigest(),
              'limitations': '28 selected cases, one publish label; not market representative; category boundaries require second review',
              'results': results}
    (ROOT / 'evaluation/independent_audit_results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(dict(Counter((r['expected'],r['observed']) for r in results)))
    print('Category disagreements:', sum(set(r['expected_categories'])!=set(r['observed_categories']) for r in results))


if __name__ == '__main__':
    main()
