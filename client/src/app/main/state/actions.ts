import { createAction, props} from '@ngrx/store';
import { SuspiciousDoc } from '../interface/susp-doc';
import { SuspiciousStatItem } from '../interface/susp-stat.interface';


export const GetStatOfSuspiciousFile = createAction(
    '[Result / API] Get Stat For Suspicious File',
    props<{filename: string}>()
);

export const GetStatOfSuspiciousFileSuccess = createAction(
    '[Result / API] Get Stat For Suspicious File Success',
    props<{res: SuspiciousStatItem[]}>()
);

export const GetSuspFileSentences = createAction(
    '[Result / API] Get Suspicious File Sentences',
    props<{filename: string}>()
);

export const GetSuspFileSentencesSuccess = createAction(
    '[Result / API] Get Suspicious File Sentences Success',
    props<{res: string[]}>()
);


export const GetSourceFileSentences = createAction(
    '[Result / API] Get Source File Sentences',
    props<{filename: string}>()
);

export const GetSourceFileSentencesSuccess = createAction(
    '[Result / API] Get Source File Sentences Success',
    props<{res: string[]}>()
);

export const GetSuspiciousDocs = createAction(
    '[Supicious Docs List] Get Suspicious Docs'
);

export const GetSuspiciousDocsSuccess = createAction(
    '[Supicious Docs List] Get Suspicious Docs Success',
    props<{res: SuspiciousDoc[]}>()
);

export const GetSuspiciousDocDetail = createAction(
    '[Supicious Doc Detail] Get Suspicious Doc',
    props<{id: number}>()

);

export const GetSuspiciousDocDetailSuccess = createAction(
    '[Supicious Doc Detail] Get Suspicious Doc Success',
    props<{res: SuspiciousDoc}>()
)