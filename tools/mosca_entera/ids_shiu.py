import pandas as pd
import pyarrow.parquet as pq
SUG = [720575940624963786, 720575940630233916, 720575940637568838, 720575940638202345, 720575940617000768, 720575940630797113, 720575940632889389, 720575940621754367, 720575940621502051, 720575940640649691, 720575940639332736, 720575940616885538, 720575940639198653, 720575940620900446, 720575940617937543, 720575940632425919, 720575940633143833, 720575940612670570, 720575940628853239, 720575940629176663, 720575940611875570]
MN9 = 720575940660219265
ann = pd.read_csv('/workspace/annotations.tsv', sep=chr(9), dtype={'root_id': 'int64'}, low_memory=False)
t = pq.read_table('/workspace/connectivity.parquet', columns=['Presynaptic_ID', 'Postsynaptic_ID'])
ids = set(t.column(0).to_numpy().tolist()) | set(t.column(1).to_numpy().tolist())
print('neuronas_en_parquet', len(ids))
sub = ann[ann.root_id.isin(SUG + [MN9])]
print('azucar_en_anotaciones', int(ann.root_id.isin(SUG).sum()), 'de', len(SUG))
print('azucar_en_parquet', sum(1 for s in SUG if s in ids), 'de', len(SUG))
print('mn9_en_anotaciones', int((ann.root_id == MN9).sum()), 'mn9_en_parquet', MN9 in ids)
cols = ['root_id', 'super_class', 'cell_class', 'cell_sub_class', 'cell_type', 'side', 'top_nt']
print(sub[cols].to_string(index=False))
