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
}

const initialState: MainState = {
  srcDocs: [],
  stats: [],
  currentSrcSents: [],
  currentSuspSents: [],
  suspDocs: [],
  suspDocDetail: undefined,
};

export const mainReducer = createReducer(
  initialState,
  on(actions.GetStatOfSuspiciousFileSuccess, (state, { res }) => ({
    ...state,
    stats: res,
    srcDocs: res.map((item: any) => item.src_file),
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
  }))
);
