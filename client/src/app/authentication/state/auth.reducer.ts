import { createReducer, on } from '@ngrx/store';
import { ResponseMessage } from '../services/auth.service';
import * as AuthActions from './auth.actions';

export interface AuthState {
  isLoggedIn: boolean;
  token?: string;
  messages?: ResponseMessage[];
}

const initialState: AuthState = {
  isLoggedIn: false,
  token: undefined,
  messages: undefined,
};

export const authLocalStorageKey = 'auth-token';

export const authReducer = createReducer(
  initialState,
  on(AuthActions.loadAuthTokenFromLocalStorageSuccess, (state, { token }) => ({
    ...state,
    isLoggedIn: true,
    token: token,
  })),
  on(AuthActions.loginSuccess, (state, { token }) => ({
    ...state,
    token: token,
    isLoggedIn: true,
  })),
  on(AuthActions.loginFailure, (state, { error }) => ({
    ...state,
    messages: error,
  })),
  on(AuthActions.registerSuccess, (state, { msg }) => ({
    ...state,
    messages: msg,
  })),
  on(AuthActions.registerFailure, (state, { error }) => ({
    ...state,
    messages: error,
  })),
  on(AuthActions.logout, (state) => ({
    ...state,
    token: undefined,
    isLoggedIn: false,
  })),
  on(AuthActions.setMesssages, (state, { messages }) => ({
    ...state,
    messages: messages,
  }))
);
