import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Store } from '@ngrx/store';
import { selectAuthToken } from '../state/auth.selectors';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(private store: Store) {}
  authToken$ = this.store.select(selectAuthToken);

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    this.authToken$.subscribe(token => {
      if (token) {
        request = request.clone({setHeaders: {
          Authorization: `Bear ${token}`
        }})
      }
    })
    return next.handle(request);
  }
}
