import { Injectable } from '@angular/core';
import { Actions, ofType, createEffect } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { exhaustMap, map, tap } from 'rxjs/operators';
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

  // after fetching the stat, load sentences of the first source doc
  loadFirstSourceSentence$ = createEffect(() =>
    this.action$.pipe(
      ofType(actions.GetStatOfSuspiciousFileSuccess),
      map((action) => action.res[0].srcFile),
      exhaustMap((srcFile) =>
        this.apiService
          .fetchSourceFileSentences(srcFile)
          .pipe(map((res) => actions.GetSourceFileSentencesSuccess({ res })))
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
      ofType(actions.GetSuspFileSentences, actions.GetStatOfSuspiciousFile),
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
