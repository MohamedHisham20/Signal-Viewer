from Signal import Signal
import pandas as pd
import numpy as np


def glue_signals(signal1: Signal, signal2: Signal, interpolation_degree=1):
    signal1_df = pd.DataFrame(signal1.data_pnts, columns=['x', 'y'])
    signal2_df = pd.DataFrame(signal2.data_pnts, columns=['x', 'y'])

    # Handle NaN values
    signal1_df.dropna(inplace=True)
    signal2_df.dropna(inplace=True)

    # Handle single point signals
    if len(signal1_df) <= 1 and len(signal2_df) <= 1:
        return pd.concat([signal1_df, signal2_df]).sort_values(by='x').reset_index(drop=True)

    if len(signal1_df) <= 1:
        return signal2_df.reset_index(drop=True)
    if len(signal2_df) <= 1:
        return signal1_df.reset_index(drop=True)

    overlap_start = max(signal1_df['x'].min(), signal2_df['x'].min())
    overlap_end = min(signal1_df['x'].max(), signal2_df['x'].max())

    if overlap_start < overlap_end:  # If there's an overlap
        return combine_overlap(signal1_df, signal2_df)
    else:
        return combine_gap(signal1_df, signal2_df, interpolation_degree)


def combine_overlap(signal1_df: pd.DataFrame, signal2_df: pd.DataFrame):
    overlap_start = max(signal1_df['x'].min(), signal2_df['x'].min())
    overlap_end = min(signal1_df['x'].max(), signal2_df['x'].max())

    number_of_points = max(10, int((overlap_end - overlap_start) * 100))  # change this to dynamically reflect the overlap duration

    interpolation_points = np.linspace(overlap_start, overlap_end, number_of_points)

    interpolated_signal1 = np.interp(interpolation_points, signal1_df['x'], signal1_df['y'], left=np.nan, right=np.nan)
    interpolated_signal2 = np.interp(interpolation_points, signal2_df['x'], signal2_df['y'], left=np.nan, right=np.nan)

    valid_mask = np.isfinite(interpolated_signal1) & np.isfinite(interpolated_signal2)
    average_y = np.full(interpolation_points.shape, np.nan)
    average_y[valid_mask] = (interpolated_signal1[valid_mask] + interpolated_signal2[valid_mask]) / 2

    before_overlap_signal1 = signal1_df[signal1_df['x'] < overlap_start]
    before_overlap_signal2 = signal2_df[signal2_df['x'] < overlap_start]

    after_overlap_signal1 = signal1_df[signal1_df['x'] > overlap_end]
    after_overlap_signal2 = signal2_df[signal2_df['x'] > overlap_end]

    result = pd.concat([
        before_overlap_signal1,
        before_overlap_signal2,
        pd.DataFrame({'x': interpolation_points, 'y': average_y}),
        after_overlap_signal1,
        after_overlap_signal2
    ])

    result = result.sort_values(by='x').reset_index(drop=True)
    return Signal.from_pd_df(result)


def combine_gap(signal1_df: pd.DataFrame, signal2_df: pd.DataFrame, interpolation_degree):
    if signal1_df['x'].max() > signal2_df['x'].min():
        return combine_gap(signal2_df, signal1_df, interpolation_degree)

    gap_start = signal1_df['x'].max()
    gap_end = signal2_df['x'].min()

    # Ensure there is a gap
    if gap_start >= gap_end:
        return pd.concat([signal1_df, signal2_df]).sort_values(by='x').reset_index(drop=True)

    coefficients_1 = np.polyfit(signal1_df['x'], signal1_df['y'], interpolation_degree)
    coefficients_2 = np.polyfit(signal2_df['x'], signal2_df['y'], interpolation_degree)

    number_of_points = max(10, int((gap_end - gap_start) * 100))  # change this to dynamically reflect the gap duration

    gap_x = np.linspace(gap_start, gap_end, number_of_points)

    poly_1_y = np.polyval(coefficients_1, gap_x)
    poly_2_y = np.polyval(coefficients_2, gap_x)
    gap_y = (poly_1_y + poly_2_y) / 2

    gap_df = pd.DataFrame({'x': gap_x, 'y': gap_y})
    result = pd.concat([signal1_df, gap_df, signal2_df]).sort_values(by='x').reset_index(drop=True)

    return Signal.from_pd_df(result)


