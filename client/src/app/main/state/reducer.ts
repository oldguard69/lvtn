import { createReducer, on } from '@ngrx/store';
import { SuspiciousStatItem } from '../interface/susp-stat.interface';
import * as actions from './actions';

export interface MainState {
    srcDocs: string[],
    stats: SuspiciousStatItem[],
    currentSrcSents: string[],
    currentSuspSents: string[]
}

const initialState: MainState = {
    srcDocs: [],
    stats: [],
    currentSrcSents: [],
    currentSuspSents: []
};

export const mainReducer = createReducer(
    initialState,
    on(actions.GetStatOfSuspiciousFileSuccess, (state, {res}) => ({...state, stats: res})),
    on(actions.GetSuspFileSentencesSuccess, (state, {res}) => ({...state, currentSuspSents: res})),
    on(actions.GetSourceFileSentencesSuccess, (state, {res}) => ({...state, currentSrcSents: res})),
)