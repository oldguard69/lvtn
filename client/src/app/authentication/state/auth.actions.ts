import { createAction, props } from '@ngrx/store';
import {
  LoginBodyObject,
  RegisterBodyObject,
  ResponseMessage
} from 'src/app/authentication/services/auth.service';

export const loadAuthTokenFromLocalStorage = createAction(
  '[Local Storage] Load Auth Token From LocalStorage'
);

// the token from localStorage is not sure if valid. Use get user profile to check it
// this action only set token property, isLoggedIn property is set from loadUserProfileSuccess/Failure
export const loadAuthTokenFromLocalStorageSuccess = createAction(
  '[Local Storage] Load Auth Token From LocalStorage Success',
  props<{ token: string }>()
);

export const localStorageEmpty = createAction(
  '[Local Storage] Auth Token From Local Storage Is Empty'
);

export const login = createAction(
  '[Login / Backend API] Login',
  props<{ body: LoginBodyObject }>()
);

export const loginSuccess = createAction(
  '[Login / LocalStorage] Login Success',
  props<{ token: string }>()
);

export const loginFailure = createAction(
  '[Login] Login Failure',
  props<{ error: ResponseMessage[] }>()
);


export const register = createAction(
  '[Register / Backend API] Register',
  props<{ body: RegisterBodyObject }>()
);

export const registerSuccess = createAction(
  '[Register] Register Success',
  props<{ msg: ResponseMessage[] }>()
);

export const registerFailure = createAction(
  '[Register] Register Failure',
  props<{ error: ResponseMessage[] }>()
);

export const setMesssages = createAction(
  '[Authentication] Set Messages',
  props<{messages: ResponseMessage[]}>()
);

export const resetMessages = createAction('[Login] Reset Messages');

export const logout = createAction('[Logout] Logout');
