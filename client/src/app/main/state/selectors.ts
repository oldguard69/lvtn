import { createFeatureSelector, createSelector } from '@ngrx/store';
import { MainState } from './reducer';

const selectMainFeatureKey = createFeatureSelector<MainState>('main');

export const selectSuspiciousStats = createSelector(
    selectMainFeatureKey,
    state => state.stats
);

export const selectSuspiciousSentences = createSelector(
    selectMainFeatureKey,
    state => state.currentSuspSents
);

export const selectSourceSentences = createSelector(
    selectMainFeatureKey,
    state => state.currentSrcSents
);

export const selectSourceFileList = createSelector(
    selectMainFeatureKey,
    state => state.srcDocs
)