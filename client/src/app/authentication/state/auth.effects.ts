import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions,  createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, exhaustMap, map } from 'rxjs/operators';
import {
  AuthService,
  ResponseMessage,
} from 'src/app/authentication/services/auth.service';
import { MessageService } from 'src/app/shared/services/message.service';
import * as AuthActions from './auth.actions';
import { authLocalStorageKey } from './auth.reducer';

@Injectable()
export class AuthEffects {
  loadAuthTokenFromLocalStorage$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loadAuthTokenFromLocalStorage),
      map(() => {
        const token = localStorage.getItem(authLocalStorageKey);
        if (token === null) {
          return AuthActions.localStorageEmpty();
        } else {
          const tokenPayload = JSON.parse(window.atob(token.split('.')[1]));
          console.log(tokenPayload)
          return AuthActions.loadAuthTokenFromLocalStorageSuccess({
            token: token,
          });
        }
      })
    )
  );

  register$ = createEffect(() =>
  this.actions$.pipe(
    ofType(AuthActions.register),
    exhaustMap((action) =>
      this.authService.register(action.body).pipe(
        map((res: any) => {
          this.router.navigateByUrl('/login');
          this.messageService.openSnackBar('Register successfully!');
          return AuthActions.registerSuccess({
            msg: [{ content: res.msg, type: 'success' }],
          });
        }),
        catchError((error: ResponseMessage[]) => {
          return of(
            AuthActions.registerFailure({
              error: error,
            })
          );
        })
      )
    )
  )
);

  login$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.login),
      exhaustMap((action) =>
        this.authService.login(action.body).pipe(
          map((res: any) => {
            this.router.navigateByUrl('/main/upload-file');
            this.messageService.openSnackBar('Log in successfully');
            console.log(res)
            return AuthActions.loginSuccess({ token: res.access_token });
          }),
          catchError((error: ResponseMessage[]) => {
            return of(AuthActions.loginFailure({ error: error }));
          })
        )
      )
    )
  );

  saveTokenToLocalStorage$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(AuthActions.loginSuccess),
        map((action) => {
          console.log(action.token)
          const token = action.token;
          localStorage.removeItem(authLocalStorageKey);
          localStorage.setItem(authLocalStorageKey, token);
        })
      ),
    { dispatch: false }
  );

  removeAuthTokenFromLocalStorage$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(AuthActions.logout),
        map(() => {
          localStorage.removeItem(authLocalStorageKey);
        })
      ),
    { dispatch: false }
  );

  logout$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(AuthActions.logout),
        map(() => {
          this.router.navigateByUrl('/');
          this.messageService.openSnackBar(
            'You have been logged out',
          );
        })
      ),
    { dispatch: false }
  );

  constructor(
    private authService: AuthService,
    private actions$: Actions,
    private router: Router,
    private store: Store,
    private messageService: MessageService
  ) {}
}
