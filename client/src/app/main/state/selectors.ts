import { createFeatureSelector, createSelector } from '@ngrx/store';
import { MainState } from './reducer';

const selectMainFeatureKey = createFeatureSelector<MainState>('main');

export const selectSuspiciousStats = createSelector(
  selectMainFeatureKey,
  (state) => state.stats
);

export const selectSuspiciousSentences = createSelector(
  selectMainFeatureKey,
  (state) => state.currentSuspSents
);

export const selectSourceSentences = createSelector(
  selectMainFeatureKey,
  (state) => state.currentSrcSents
);

export const selectSourceFileList = createSelector(
  selectMainFeatureKey,
  (state) => state.srcDocs
);

export const selectSuspiciousDocs = createSelector(
  selectMainFeatureKey,
  (state) => state.suspDocs
);

export const selectSuspiciousDocDetail = createSelector(
  selectMainFeatureKey,
  (state) => state.suspDocDetail
);

export const selectSentenceIndex = createSelector(
  selectMainFeatureKey,
  (state) => ({ src: state.currentSrcIndex, susp: state.currentSuspIndex })
);

export const selectSupiciousDocDetailFilename = createSelector(
  selectMainFeatureKey,
  (state) => state.suspDocDetail?.filename
)

export const selectNumberOfParagraph = createSelector(
  selectMainFeatureKey,
  (state) => ({
    totalParagraph: state.stats.length, 
    currentParagraph: state.currentParaNumber
  })
)