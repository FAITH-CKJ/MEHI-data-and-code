from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/validation'
OUTPUT = ROOT / 'reproduced/validation'
CLASSES = ['mangrove', 'tidal_flat', 'non_mangrove_vegetation', 'water', 'built_up', 'other']


def metrics(matrix):
    n = int(matrix.sum())
    observed = float(np.trace(matrix) / n)
    expected = float(matrix.sum(axis=0) @ matrix.sum(axis=1) / n ** 2)
    return {'n': n, 'overall_accuracy_percent': 100 * observed, 'kappa': (observed - expected) / (1 - expected)}


def main():
    points = pd.read_csv(SOURCE / 'map_validation_predictions.csv.gz')
    training = pd.read_csv(ROOT / 'data/classifier_inputs/train.csv.gz')
    assert points.sample_row.nunique() == len(points)
    assert points.groupby(['year', 'reference_coordinate']).reference_class.nunique().max() == 1
    duplicates = points.duplicated(['year', 'reference_coordinate'])
    np.testing.assert_array_equal(duplicates, points.duplicate_coordinate_year)
    valid = points.loc[points.evaluation_status.eq('valid')]
    assert not valid.duplicated(['year', 'reference_coordinate']).any()
    assert valid[['mapped_class', 'reference_class']].isin(range(1, 7)).all().all()
    annual = []
    matrices = []
    pooled = np.zeros((6, 6), dtype=np.int64)
    expected_annual = pd.read_csv(SOURCE / 'landcover_confusion_matrix_by_year.csv')
    for year, group in valid.groupby('year', sort=True):
        matrix = np.zeros((6, 6), dtype=np.int64)
        np.add.at(matrix, (group.mapped_class.to_numpy(dtype=int) - 1, group.reference_class.to_numpy(dtype=int) - 1), 1)
        reference = expected_annual.loc[expected_annual.year.eq(year)].pivot(index='mapped_class', columns='reference_class', values='count').loc[CLASSES, CLASSES].to_numpy()
        np.testing.assert_array_equal(matrix, reference)
        pooled += matrix
        annual.append({'year': int(year), **metrics(matrix)})
        matrices.extend({'year': int(year), 'mapped_class': mapped, 'reference_class': reference, 'count': int(matrix[i, j])} for i, mapped in enumerate(CLASSES) for j, reference in enumerate(CLASSES))
    expected = pd.read_csv(SOURCE / 'landcover_confusion_matrix.csv').set_index('mapped_class').loc[CLASSES, CLASSES].to_numpy()
    np.testing.assert_array_equal(pooled, expected)
    class_accuracy = pd.DataFrame({'class': CLASSES, 'user_accuracy_percent': 100 * np.diag(pooled) / pooled.sum(axis=1), 'producer_accuracy_percent': 100 * np.diag(pooled) / pooled.sum(axis=0)})
    reference = pd.read_csv(SOURCE / 'landcover_class_accuracy.csv').set_index('class').loc[CLASSES]
    for name in ['user_accuracy_percent', 'producer_accuracy_percent']:
        np.testing.assert_allclose(class_accuracy[name], reference[name], atol=1e-12, rtol=0)
    flow = [{'group': 'training', 'n': len(training)}, {'group': 'validation', 'n': len(points)}, {'group': 'duplicate_coordinate_year', 'n': int(duplicates.sum())}, {'group': 'outside_map', 'n': int(points.evaluation_status.eq('outside_map').sum())}, {'group': 'unique_covered', 'n': len(valid)}]
    assert len(points) == flow[2]['n'] + flow[3]['n'] + flow[4]['n']
    OUTPUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(annual).to_csv(OUTPUT / 'annual_metrics.csv', index=False)
    pd.DataFrame([metrics(pooled)]).to_csv(OUTPUT / 'pooled_metrics.csv', index=False)
    pd.DataFrame(matrices).to_csv(OUTPUT / 'annual_confusion_matrix.csv', index=False)
    pd.DataFrame(pooled, index=pd.Index(CLASSES, name='mapped_class'), columns=CLASSES).to_csv(OUTPUT / 'pooled_confusion_matrix.csv')
    class_accuracy.to_csv(OUTPUT / 'class_accuracy.csv', index=False)
    pd.DataFrame(flow).to_csv(OUTPUT / 'sample_flow.csv', index=False)
    print(f'Final-map validation: {len(valid):,} unique covered points; OA = {metrics(pooled)["overall_accuracy_percent"]:.6f}%.')


if __name__ == '__main__':
    main()
