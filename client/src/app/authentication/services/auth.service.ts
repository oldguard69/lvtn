import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface RegisterBodyObject {
  email: string;
  fullname: string;
  password: string;
}

export interface LoginBodyObject {
  email: string;
  password: string;
}

export interface ResponseMessage {
  type: 'success' | 'failure';
  content: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private http: HttpClient, @Inject('API_URL') private api_url: string) {}

  register(body: RegisterBodyObject) {
    return this.http
      .post(`${this.api_url}/register`, body)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          console.log(error.error)
          const messages: ResponseMessage[] = error.error.msg.map(
            (msg: any) => ({
              type: 'failure',
              content: msg,
            })
          );
          console.log(messages)
          return throwError(messages);
        })
      );
  }

  login(body: LoginBodyObject) {
    return this.http
      .post(`${this.api_url}/login`, body)
      .pipe(
        catchError((errorRes: HttpErrorResponse) => {
          console.log(errorRes.error);
          return throwError([
            { type: 'failure', content: errorRes.error.msg },
          ]);
        })
      );
  }
}
