"""Correction-analysis gates: malformed or incomplete evidence must not pass."""
import json
import pytest
from analysis.s0_13_analyze import read_row, summarize, SEEDS, LEVELS


def row():
    return dict(method='pat-both',seed=11,mismatch_scale=2,n_updates=31600,
                cell='C-2',binding_revision=2,source_commit='frozen-source',
                device_passes=252800,digital_passes=505600,final_ser=0.001,
                final_ser_fine=0.001,eval_trace=[[i*100,i*800,0.001] for i in range(1,317)])


@pytest.mark.parametrize('field,value',[
    ('source_commit','wrong-source'),('device_passes',800),
    ('final_ser_fine',float('nan')),('eval_trace',[])])
def test_reject_invalid_corrected_evidence(tmp_path,field,value):
    d=row();d[field]=value
    path=tmp_path/'row.json';path.write_text(json.dumps(d))
    with pytest.raises(ValueError):
        read_row(path,'pat-both',11,2,True,'frozen-source')


def test_missing_paired_seed_cannot_produce_verdict():
    rows={(method,m,s):{'final_ser_fine':0.001} for method in
          ('pat-both','offline-deploy') for m in LEVELS for s in SEEDS}
    del rows[('offline-deploy',1,151)]
    with pytest.raises(KeyError):summarize(rows,'final_ser_fine')
