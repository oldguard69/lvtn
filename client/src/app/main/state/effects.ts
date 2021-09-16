import { Injectable } from '@angular/core';
import { Actions, ofType, createEffect } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { exhaustMap, map } from 'rxjs/operators';
import { ApiService } from '../services/api.service';
import * as actions from './actions';

@Injectable()
export class MainEffects {
  loadSuspiciousStats$ = createEffect(() =>
    this.action$.pipe(
      ofType(actions.GetStatOfSuspiciousFile),
      exhaustMap((action) =>
        this.apiService
          .fetchStatOfSuspiciousFile(action.filename)
          .pipe(map((res) => actions.GetStatOfSuspiciousFileSuccess({ res })))
      )
    )
  );

  loadSourceSentence$ = createEffect(() =>
    this.action$.pipe(
      ofType(actions.GetSourceFileSentences),
      exhaustMap((action) =>
        this.apiService
          .fetchSourceFileSentences(action.filename)
          .pipe(map((res) => actions.GetSourceFileSentencesSuccess({ res })))
      )
    )
  );

  loadSuspiciousSentence$ = createEffect(() =>
    this.action$.pipe(
      ofType(actions.GetSuspFileSentences),
      exhaustMap((action) =>
        this.apiService
          .fetchSuspiciousFileSentences(action.filename)
          .pipe(map((res) => actions.GetSuspFileSentencesSuccess({ res })))
      )
    )
  );

  constructor(
    private action$: Actions,
    private store: Store,
    private apiService: ApiService
  ) {}
}
