import { createReducer, on } from '@ngrx/store';
import { SuspiciousDoc } from '../interface/susp-doc';
import { SuspiciousStatItem } from '../interface/susp-stat.interface';
import * as actions from './actions';

export interface MainState {
  srcDocs: string[];
  stats: SuspiciousStatItem[];
  currentSrcSents: string[];
  currentSuspSents: string[];
  suspDocs: SuspiciousDoc[];
  suspDocDetail?: SuspiciousDoc;
  currentSrcIndex?: string;
  currentSuspIndex?: string;
}

const initialState: MainState = {
  srcDocs: [],
  stats: [],
  currentSrcSents: [],
  currentSuspSents: [],
  suspDocs: [],
  suspDocDetail: undefined,
  currentSrcIndex: undefined,
  currentSuspIndex: undefined,
};

export const mainReducer = createReducer(
  initialState,
  on(actions.GetStatOfSuspiciousFileSuccess, (state, { res }) => ({
    ...state,
    stats: res,
    srcDocs: res.map((item: any) => item.src_file),
    currentSrcIndex: formatSentenceIndex(
      res[0].src_index,
      res[0].paragraph_length
    ),
    currentSuspIndex: formatSentenceIndex(
      res[0].susp_index,
      res[0].paragraph_length
    )
  })),
  on(actions.GetSuspFileSentencesSuccess, (state, { res }) => ({
    ...state,
    currentSuspSents: res,
  })),
  on(actions.GetSourceFileSentencesSuccess, (state, { res }) => ({
    ...state,
    currentSrcSents: res,
  })),
  on(actions.GetSuspiciousDocDetailSuccess, (state, { res }) => ({
    ...state,
    suspDocDetail: res,
  })),
  on(actions.GetSuspiciousDocsSuccess, (state, { res }) => ({
    ...state,
    suspDocs: res,
  })),
  on(actions.SetCurrentSentencesIndex, (state, { index }) => ({
    ...state,
    currentSrcIndex: formatSentenceIndex(
      state.stats[index].src_index,
      state.stats[index].paragraph_length
    ),
    currentSuspIndex: formatSentenceIndex(
      state.stats[index].susp_index,
      state.stats[index].paragraph_length
    )
  }))
);

function formatSentenceIndex(index: number, length: number): string {
  return `Câu ${index} đến ${index + length - 1}`;
}
